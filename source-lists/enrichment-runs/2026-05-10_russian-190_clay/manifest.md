# Run: 2026-05-10_russian-190_clay

**Date**: 2026-05-10
**Tool**: Clay (Find Company)
**Operator**: Yana

## Source

`source-lists/clia-q1-2026/russian_candidates_nj.csv` — 190 NJ labs flagged as potential Russian-speaking ownership (CMS POS extract).

## Input

- File: `input.csv`
- Rows: 190
- Columns sent to Clay: `name, address, city, state, zip, phone, clia_number, lab_type, cms_facility_type_name, test_volume, site_count`
- All rows had **0 domains** in CMS POS — every row needed enrichment.

## Output

- File: `output.csv`
- Rows: 190
- Added columns: `domain`, `company_linkedin_url`

## Status

**done** — output ready for downstream merge.

## Cost

~190 Clay credits (Find Company at ~1 credit/row).

## Next

Per `plans/outreach-plan-vivica-russian-nj.md`:
1. Andrew confirms which labs are actually Russian-speaking (~60–100 of 190)
2. Apollo MCP people search ONLY on confirmed labs
3. Andrew specifies target person per lab (often the owner directly)

Merged into `source-lists/segments/` after Andrew's confirmation pass.
