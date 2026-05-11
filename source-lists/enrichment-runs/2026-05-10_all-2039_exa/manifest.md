# Run: 2026-05-10_all-2039_exa

**Date**: 2026-05-10
**Tool**: Exa (web search-based domain lookup)
**Operator**: Yana

## Source

Combined input from the same two CMS POS extracts used in the Clay runs:
- `russian_candidates_nj.csv` (190 rows)
- `bucket_REFERENCE.csv` (1849 rows)
- Total: 2039 rows

## Purpose

Alternative / supplement to the parallel Clay runs (`2026-05-10_russian-190_clay`, `2026-05-10_reference-1849_clay`) — Exa-based domain enrichment to compare coverage and accuracy.

## Stages

Run was executed in 4 progressive batches (see `stages/`):

| Stage | File | Rows | Notes |
|-------|------|------|-------|
| Test | `stages/test_50_input.json` + `stages/test_50_results.{csv,json}` | 50 | Sanity check on a sample |
| Full | `stages/full_690_results.{csv,json}` | 690 | First production batch |
| Reference tail | `stages/ref_500-1849_results.{csv,json}` | 1349 | Companies 500–1849 of reference list |
| **Final merged** | `output.csv` + `output.json` | **2039** | Deduped union of all batches |

## Output

- Files: `output.csv` (final merged result), `output.json` (full structured response)
- Rows: 2039
- Final artifact for this run.

## Status

**done** — `output.csv` is the canonical Exa enrichment for these 2039 companies. Stage files retained for traceability.

## Next

- Compare domain coverage vs the two Clay runs (`russian_190_clay/output.csv`, `reference_1849_clay/output.csv`)
- Decide which source wins per row (Clay vs Exa) when domains differ
- Merge winning domains into `source-lists/segments/`
