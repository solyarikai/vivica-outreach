# CMS POS File — Schema Reference

The CMS POS (Provider of Services) CLIA file is published quarterly at <https://qcor.cms.gov> bulk export. Q1 2026 file: 676,051 rows, 100+ columns.

This document covers ONLY the columns `clia-source` skill uses. Full layout PDF: <https://data.cms.gov/sites/default/files/2022-10/eb7b11f8-f79b-4229-a365-a69cd27f69a3/Layout%20Sep%2022%20CLIA.pdf>

## Identification fields

| Column | Type | Notes |
|---|---|---|
| `PRVDR_NUM` | string | CLIA number, unique per lab. Format: `<state>D<8 digits>` (e.g. `31D2123456` for NJ) |
| `FAC_NAME` | string | Lab display name |

## Address fields

| Column | Type | Notes |
|---|---|---|
| `ST_ADR` | string | Street address |
| `CITY_NAME` | string | City |
| `STATE_CD` | string (2) | State / territory code (US states + PR, VI, etc.) |
| `ZIP_CD` | string | ZIP — usually 5 digits, sometimes 9 |
| `PHNE_NUM` | string | Phone, usually digits only, length varies |

Labs always have a physical address (they handle biomaterials). Phone is the contactability gate in `clia-source` filter.

## Certificate status

| Column | Type | Notes |
|---|---|---|
| `CRTFCT_TYPE_CD` | string (1-2) | `1`=Compliance, `2`=Waiver, `3`=PPMP, `4`=Accreditation, `9`=Registration. **Filter to `1` or `4`** |
| `CRTFCTN_DT` | YYYYMMDD | Initial certification date. **"Recently certified" trigger compares this to `--since`** |
| `EFCTV_DT` | YYYYMMDD | Effective date (often = `CRTFCTN_DT` for initial, differs for renewals) |
| `TRMNTN_EXPRTN_DT` | YYYYMMDD | Expected termination/expiration |
| `PGM_TRMNTN_CD` | string (2) | `00`=active, anything else = terminated. **Filter to `00`** |

## Facility-type fields (segmentation primary signal)

| Column | Type | Notes |
|---|---|---|
| `GNRL_FAC_TYPE_CD` | string (2) | **AUTHORITATIVE FACILITY TYPE.** 29 distinct values mapped to Vivica buckets. Full mapping below |
| `HOSP_LAB_EXCPTN_SW` | Y/N | Hospital exception switch. **Filter to `N`** to exclude Epic/Cerner-locked hospital labs |
| `LAB_SITE_CNT` | integer | Number of sites in this lab's network. >1 means multi-site |
| `FORM_116_TEST_VOL_CNT` | integer | Annual test volume (Form 116 reported). Proxy for lab size |

### `GNRL_FAC_TYPE_CD` values

Mapped to Vivica targeting buckets by `classify_facility_type()` in `scripts/classify_by_clia_code.py`:

| Code | CMS facility type | Vivica bucket |
|---|---|---|
| `01` | Ambulance | OTHER |
| `02` | Ambulatory Surgery Center | OTHER |
| `03` | Ancillary Test Site | **PSC** |
| `04` | Assisted Living | OTHER |
| `05` | Blood Bank | OTHER |
| `06` | Community Clinic | **PSC** |
| `07` | Comprehensive Outpatient Rehab | OTHER |
| `08` | ESRD Dialysis | UNSUITABLE |
| `09` | FQHC (Federally Qualified Health Center) | **PSC** |
| `10` | Health Fair | OTHER |
| `11` | HMO | OTHER |
| `12` | Home Health | OTHER |
| `13` | Hospice | OTHER |
| `14` | Hospital Lab | **UNSUITABLE** (Epic/Cerner) |
| `15` | Independent Lab | **REFERENCE** |
| `16` | Industrial | OTHER |
| `17` | Insurance | UNSUITABLE |
| `18` | ICF/IID | OTHER |
| `19` | Mobile Lab | OTHER |
| `20` | Pharmacy | UNSUITABLE |
| `21` | Physician Office Lab | **POL** (largest target bucket) |
| `22` | Other Practitioner | **POL** (POL-like) |
| `23` | Prison | UNSUITABLE |
| `24` | Public Health Lab | **REFERENCE** |
| `25` | Rural Health Clinic | **PSC** |
| `26` | School / Student Health | OTHER |
| `27` | SNF / Nursing | OTHER |
| `28` | Tissue Bank | OTHER |
| `29` | Other | OTHER |

## Specialty / classification codes

| Column | Type | Notes |
|---|---|---|
| `CLIA_LAB_CLASSIFICATION_CD_1` through `_10` | string (3) | Up to 10 specialty codes. **In practice almost always `00`** — see `classification_codes.md` |
| `CURRENT_CLIA_LAB_CLSFCTN_CD` | string (2) | Current CLIA lab classification. Q1 2026 file: 99% are `00`, 1% are `05` |

**Critical caveat repeated**: do not rely on these for primary segmentation. They're sparse. Use `GNRL_FAC_TYPE_CD` for facility type; pull specialty downstream via website scraping.

## Accreditation flags

| Column | Type | Notes |
|---|---|---|
| `A2LA_ACRDTD_CD` | Y/N | American Association for Laboratory Accreditation |
| `AABB_ACRDTD_CD` | Y/N | American Association of Blood Banks |
| `AOA_ACRDTD_CD` | Y/N | American Osteopathic Association |
| `ASHI_ACRDTD_CD` | Y/N | American Society for Histocompatibility & Immunogenetics |
| `CAP_ACRDTD_CD` | Y/N | College of American Pathologists |
| `COLA_ACRDTD_CD` | Y/N | COLA |
| `JCAHO_ACRDTD_CD` | Y/N | Joint Commission |

> **Caveat**: in Q1 2026 ICP set, all 7 accreditation flags showed `Y=0`. Either the data isn't populated in this file, or the flag semantics differ from what the column name suggests. Treat with skepticism until verified against another data source.

## Sub-type field

| Column | Type | Notes |
|---|---|---|
| `PRVDR_CTGRY_SBTYP_CD` | string | Provider category subtype. In Q1 2026 ICP set: 100% are `01`. Not useful for sub-segmentation |

## Filter logic in `clia-source` skill

The standard ICP filter applied by `apply_icp_filter()` in `scripts/filter_pos_file.py`:

```python
icp = df[
    (df['PGM_TRMNTN_CD'] == '00') &           # active
    (df['CRTFCT_TYPE_CD'].isin(['1', '4'])) & # Compliance or Accreditation
    (df['HOSP_LAB_EXCPTN_SW'] == 'N') &       # not hospital lab
    (df['PHNE_NUM'].notna()) &
    (df['PHNE_NUM'].str.len() >= 10) &        # contactable
    (pd.to_datetime(df['CRTFCTN_DT'], format='%Y%m%d', errors='coerce')
     >= pd.Timestamp(args.since))             # recency trigger
]
```

Q1 2026 file with `--since 2025-01-01`: **9,193 ICP labs** pass.

After bucketing by `GNRL_FAC_TYPE_CD`:

| Bucket | Count | Vivica strategy |
|---|---|---|
| POL (codes 21, 22) | ~5,745 | Primary target — largest bucket |
| REFERENCE (codes 15, 24) | ~1,849 | Premium target |
| PSC (codes 03, 06, 09, 25) | ~499 | Secondary target |
| UNSUITABLE (codes 08, 14, 17, 20, 23) | ~456 | **Excluded** |
| OTHER (everything else) | ~644 | Low-priority, separate plan |

## Cross-references

- Skill: `../SKILL.md`
- Code: `../scripts/filter_pos_file.py`, `../scripts/classify_by_clia_code.py`
- Specialty codes (sparse but documented): `classification_codes.md`
- Glossary: `../../../../../glossary.md` → "POS file", "CLIA", "GNRL_FAC_TYPE_CD"
