# CLIA Classification Codes — Reference

The CMS POS file contains 10 columns `CLIA_LAB_CLASSIFICATION_CD_1` through `_10` per lab. Each can hold a specialty code per **42 CFR Part 493**.

> **Important caveat**: in practice, these fields are **almost entirely empty** in CMS POS data. Q1 2026 file analysis showed only ~1% of ICP labs (102 of 9,193) carry meaningful specialty codes — the rest are populated with `00` (no specialty declared) for newly-certified labs. **Do not rely on this for primary segmentation.** Use `GNRL_FAC_TYPE_CD` instead (see `pos_file_schema.md`).
>
> This file documents the codes for completeness and for the rare 1% of labs that DO have populated specialty data.

## Code → Vivica segment mapping

The mapping driving `classify_segments()` in `scripts/classify_by_clia_code.py`:

### Anatomic pathology cluster

| Code | CMS specialty | Vivica segment(s) |
|---|---|---|
| 100 | Histopathology | `anatomic_pathology` |
| 110 | Oral pathology | `anatomic_pathology` |
| 120 | Cytology | `anatomic_pathology`, `cytology` |
| 130 | Cytogenetics | `anatomic_pathology` |

### Molecular & genetics

| Code | CMS specialty | Vivica segment(s) |
|---|---|---|
| 250 | Molecular biology / molecular pathology | `molecular_diagnostics` |
| 260 | Molecular oncology | `molecular_diagnostics` |

### Clinical chemistry

| Code | CMS specialty | Vivica segment(s) |
|---|---|---|
| 310 | Routine chemistry | `clinical_chemistry` |
| 320 | Automated chemistry / endocrinology | `clinical_chemistry` |
| 330 | Urinalysis | `clinical_chemistry`, `urinalysis` |
| 340 | General chemistry | `clinical_chemistry` |

### Hematology

| Code | CMS specialty | Vivica segment(s) |
|---|---|---|
| 400 | Hematology | `hematology` |

### Microbiology cluster

| Code | CMS specialty | Vivica segment(s) |
|---|---|---|
| 500 | Bacteriology | `microbiology` |
| 510 | Mycobacteriology | `microbiology` |
| 520 | Mycology | `microbiology` |
| 530 | Parasitology | `microbiology` |
| 540 | Virology | `microbiology`, `virology` |

### Immunology / serology

| Code | CMS specialty | Vivica segment(s) |
|---|---|---|
| 600 | Diagnostic immunology / general immunology | `immunology` |
| 610 | Syphilis serology | `immunology` |

### Toxicology

| Code | CMS specialty | Vivica segment(s) |
|---|---|---|
| 800 | Toxicology (general) | `toxicology` |
| 810 | Forensic toxicology | `toxicology`, `forensic` |

### Other

| Code | CMS specialty | Vivica segment(s) |
|---|---|---|
| 900 | Radiobioassay | `radiobioassay` |

## Multi-code labs

A single lab can carry multiple classification codes (up to 10). The `classify_segments()` function deduplicates segments across codes.

Example: lab with codes `100` (histopathology) and `120` (cytology) → segments `['anatomic_pathology', 'cytology']`.

## Practical guidance

- Per ICP analysis, top expected segments by absolute count (when codes are populated):
  1. `clinical_chemistry` — broadest CMS coverage
  2. `hematology`
  3. `microbiology`
  4. `anatomic_pathology`
  5. `molecular_diagnostics`
  6. `toxicology`
  7. `immunology`
- Per Andrew's note in kick-off, **toxicology** is Vivica's premium segment but represents a small minority of labs

## Source

CMS regulation 42 CFR Part 493. Full layout: <https://data.cms.gov/sites/default/files/2022-10/eb7b11f8-f79b-4229-a365-a69cd27f69a3/Layout%20Sep%2022%20CLIA.pdf>

## Cross-references

- Code: `../scripts/classify_by_clia_code.py` (`CODE_TO_SEGMENTS` dict)
- Schema reference: `pos_file_schema.md`
- Skill: `../SKILL.md`
