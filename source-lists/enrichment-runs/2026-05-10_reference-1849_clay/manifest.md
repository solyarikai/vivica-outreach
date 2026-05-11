# Run: 2026-05-10_reference-1849_clay

**Date**: 2026-05-10
**Tool**: Clay (Find Company)
**Operator**: Yana

## Source

`source-lists/clia-q1-2026/clia_Q1_2026_segmented/bucket_REFERENCE.csv` — 1849 CLIA reference labs, full US (CMS POS extract).

## Input

- File: `input.csv`
- Rows: 1849
- Columns sent to Clay: `name, address, city, state, zip, phone, clia_number, lab_type, cms_facility_type_name, test_volume, site_count`
- All rows had **0 domains** in CMS POS.

## Output

- File: `output.csv`
- Rows: 1849
- Added columns: `domain`, `company_linkedin_url`

## Status

**done** — output ready for downstream merge.

## Cost

~1849 Clay credits.

## Next

Per `plans/outreach-plan-vivica-clia-fresh.md`, full 3-persona enrichment downstream:
1. Lab Director / Medical Director / Owner per company
2. Apollo MCP first → FindyMail MCP for missing emails → Clay waterfall for residuals

Merged into `source-lists/segments/` for downstream people enrichment.
