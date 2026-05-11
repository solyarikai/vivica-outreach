---
name: clia-source
description: Convert the CMS POS (Provider of Services) CLIA file into a stream of qualified ICP companies for the Vivica LIMS pipeline. Use this skill INSTEAD OF the standard gtm-mcp Apollo company search whenever the target audience is US clinical laboratories. Triggers include any mention of CLIA, recently certified labs, lab certifications, POS file, CMS file, "freshly licensed labs", or laboratory segmentation by toxicology/anatomic pathology/molecular/etc. The output format matches what `pipeline_save_contacts` and downstream gtm-mcp tools expect, so the rest of the pipeline (scraping, classification, people enrichment, sequence push) runs unchanged.
---

# clia-source — CMS POS file as Vivica's primary lead source

## When to use this

The default gtm-mcp pipeline searches Apollo for companies. For Vivica's clinical laboratory market, Apollo is not the optimal first source because:

1. Clinical labs are a regulated industry where the **canonical registry is CMS QCOR**, not Apollo's crawl
2. The most valuable trigger ("recently CLIA-certified") is **not available in Apollo at all** — it lives in CMS data
3. Apollo's industry tag "Hospitals & Healthcare" is too broad — most matches are not labs
4. Apollo charges credits per company; the POS file is free

So for Vivica, the source-of-truth pipeline is:

```
CMS POS file (676k rows)
   │
   │  this skill: filter + segment + format
   ▼
ICP companies (~9k rows after filter)
   │
   │  standard gtm-mcp: scrape websites
   ▼
Verified targets (~3-4k rows after qualification)
   │
   │  standard gtm-mcp: people enrichment via Apollo
   ▼
Contacts with verified emails
```

This skill replaces ONLY the first step. Once companies are emitted, hand off to standard gtm-mcp tools.

## Input

A POS file CSV from CMS, typically named `POS_File_CLIA_<quarter>.csv`. Download from <https://qcor.cms.gov> → bulk data export. The file has 100+ columns; this skill only uses a handful.

**Critical fields:**

| Field | Type | Use |
|---|---|---|
| `FAC_NAME` | string | Lab name |
| `ST_ADR`, `CITY_NAME`, `STATE_CD`, `ZIP_CD` | string | Physical address (labs MUST have one — biomaterials) |
| `PHNE_NUM` | string | Phone — required for contactability |
| `CRTFCT_TYPE_CD` | int | 1=Compliance, 2=Waiver, 3=PPM, 4=Accreditation, 9=Registration |
| `CRTFCTN_DT` | YYYYMMDD | Initial certification date — main trigger |
| `PGM_TRMNTN_CD` | string | "00" = active; anything else means terminated/inactive |
| `HOSP_LAB_EXCPTN_SW` | Y/N | Y = inside a hospital — EXCLUDE (Epic/Cerner lock-in) |
| `CLIA_LAB_CLASSIFICATION_CD_1..10` | int | Specialization codes — see `references/classification_codes.md` |
| `FORM_116_TEST_VOL_CNT` | int | Test volume — proxy for lab size |
| `LAB_SITE_CNT` | int | Number of sites — branch detection |

## ICP filter logic — what counts as "Vivica target"

Apply ALL of these filters in order:

```python
icp = df[
    # 1. Must be active
    (df['PGM_TRMNTN_CD'] == '00') &

    # 2. Compliance OR Accreditation only (Waiver labs don't need a LIMS)
    (df['CRTFCT_TYPE_CD'].isin(['1', '4'])) &

    # 3. NOT a hospital lab (skip Epic/Cerner-locked institutions)
    (df['HOSP_LAB_EXCPTN_SW'] == 'N') &

    # 4. Must have a phone (basic contactability check)
    (df['PHNE_NUM'].notna()) &
    (df['PHNE_NUM'].str.len() >= 10) &

    # 5. Default: certified after 2025-01-01 (configurable via --since)
    (pd.to_datetime(df['CRTFCTN_DT'], format='%Y%m%d', errors='coerce')
        >= pd.Timestamp(args.since))
]
```

On the Q1 2026 file with `--since 2025-01-01` this yields **~9,288 labs**.

To narrow further by `--since`:
- `2026-01-01` → ~4,800 labs (last 4 months)
- `2025-06-01` → ~19,600 labs (last 11 months)
- `2025-01-01` → ~30,800 labs (last 16 months — full default)

## Segment classification

After filtering, each row gets tagged with one or more **Vivica segments** based on `CLIA_LAB_CLASSIFICATION_CD_1` through `_10`. The mapping is in `scripts/classify_by_clia_code.py`:

| Vivica segment | CLIA classification codes |
|---|---|
| `toxicology` | 800 (toxicology), 810 (forensic toxicology) |
| `anatomic_pathology` | 100, 110, 120 (histopathology, cytology, oral) |
| `molecular_diagnostics` | 250 (molecular biology) |
| `clinical_chemistry` | 310, 320 (routine + automated chemistry) |
| `hematology` | 400 (hematology) |
| `microbiology` | 500, 510, 520 (bacteriology, mycobacteriology, mycology) |
| `immunology` | 600 (immunology) |

A lab can belong to multiple segments. The `segments` field in the output is a list.

POL/PSC/Reference distinction is harder — CMS doesn't directly encode this. Heuristics in `format_for_pipeline.py`:
- `POL` (Physician Office Lab): `LAB_SITE_CNT == 1` AND `FAC_NAME` contains physician name patterns ("MD", "M.D.", "DR ", "P.C.", "PLLC")
- `PSC` (Patient Service Center): name contains "lab", "diagnostic", "patient service", and `LAB_SITE_CNT == 1`
- `REFERENCE`: `LAB_SITE_CNT > 1` OR test volume > 50,000/year

## Russian-speaking lab heuristic

Per Andrew's note in the kick-off call, the russian-speaking owner segment lives mostly in NJ. Use this as a pre-filter ONLY (final classification still needs human review):

```python
russian_speaking_candidates = icp[
    (icp['STATE_CD'].isin(['NJ', 'NY', 'PA'])) &
    (icp['FAC_NAME'].str.contains(
        r'\b(?:medical|diagnostic|laboratories|associates)\b',
        case=False, na=False, regex=True
    ))
]
```

This finds candidates only. Final russian-speaking attribution requires:
1. Looking up the lab director name in the CMS database
2. Cross-referencing with Andrew's known list
3. Manual confirmation from Andrew

The skill produces a `candidates_russian_nj.csv` for Andrew to review.

## Output format

The skill writes its results into the gtm-mcp project workspace in the format that `pipeline_save_contacts` and downstream tools expect:

**File 1**: `~/.gtm-mcp/projects/vivica/sources/clia_<quarter>.json`

```json
{
  "source": "clia_pos_file",
  "source_version": "Q1_2026",
  "filter_params": {
    "since": "2025-01-01",
    "certificate_types": ["1", "4"],
    "exclude_hospital_labs": true,
    "min_phone_length": 10
  },
  "generated_at": "2026-05-10T12:00:00Z",
  "company_count": 9288,
  "companies": [
    {
      "name": "ACME Diagnostic Lab",
      "domain": null,
      "phone": "9735551234",
      "address": "123 Main St",
      "city": "Newark",
      "state": "NJ",
      "zip": "07102",
      "clia_number": "31D2123456",
      "certified_at": "2025-08-15",
      "certificate_type": "Compliance",
      "site_count": 1,
      "test_volume": 1500,
      "segments": ["clinical_chemistry"],
      "lab_type": "POL",
      "russian_candidate": true
    }
  ]
}
```

**File 2**: `~/.gtm-mcp/projects/vivica/sources/clia_<quarter>_segmented/`

One CSV per Vivica segment:
- `toxicology.csv`
- `anatomic_pathology.csv`
- `molecular_diagnostics.csv`
- `russian_candidates_nj.csv`
- ...etc

These can be fed individually into `/launch` as separate campaigns.

## Domain enrichment

CMS doesn't have website domains. Before scraping, we need to find each lab's website. The skill emits companies with `domain: null`; downstream a separate enrichment step (Apollo `enrich_companies` by name+address, or Google search for `<lab_name> <city> <state> CLIA`) populates the domain.

This is intentionally NOT done inside this skill — domain enrichment costs Apollo credits and should be gated by user approval (per gtm-mcp's "never spend credits without confirmation" rule).

## Usage

```bash
# Full filter, default segments
python scripts/filter_pos_file.py \
  --input ~/code/vivica-outreach/input-data/POS_File_CLIA_Q1_2026.csv \
  --since 2025-01-01 \
  --output ~/.gtm-mcp/projects/vivica/sources/

# Last 4 months only
python scripts/filter_pos_file.py \
  --input <file> --since 2026-01-01 --output <dir>

# Single segment, e.g. toxicology only
python scripts/filter_pos_file.py \
  --input <file> --segment toxicology --output <dir>
```

The script prints a summary table and exits. No API calls. No costs.

## What this skill does NOT do

- Does NOT contact Apollo (the source IS the POS file, by design)
- Does NOT scrape websites (downstream gtm-mcp scraping skill does that)
- Does NOT enrich people (downstream gtm-mcp Apollo people enrichment does that)
- Does NOT create campaigns (downstream gtm-mcp `campaign_push` does that)

It is a pure data-prep step that drops into the standard pipeline at the "companies discovered" point.

## See also

- `references/classification_codes.md` — full mapping of CLIA codes to specializations
- `references/pos_file_schema.md` — every column in the CMS POS file
- `../../../../reference/playbooks/russian-segment.md` — how to handle russian-speaking candidates
