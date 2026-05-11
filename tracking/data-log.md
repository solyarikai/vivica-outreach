# Data Log — Vivica Outreach

Append-only chronological record of **data operations**: enrichment runs, scrapes, batch lookups, merges, exports. Separate from [[log]] (session-level) and [[decisions-log]] (strategic).

One entry per operation. Points to the run folder under `source-lists/enrichment-runs/` for full detail.

Format:
```
## [YYYY-MM-DD] <run-id> — one-line summary
- tool: <name>
- input: <count> rows from <source>
- output: <count> rows, <count> errors
- status: done / superseded-by-<run-id> / failed
- manifest: source-lists/enrichment-runs/<run-id>/manifest.md
```

---

## [2026-05-10] 2026-05-10_russian-190_clay — Clay Find Company on 190 NJ Russian-speaking owner candidates

- tool: Clay Find Company
- input: 190 rows from `source-lists/clia-q1-2026/russian_candidates_nj.csv`
- output: 190 rows enriched (domain + company_linkedin_url added)
- status: done
- manifest: `source-lists/enrichment-runs/2026-05-10_russian-190_clay/manifest.md`

## [2026-05-10] 2026-05-10_reference-1849_clay — Clay Find Company on 1849 CLIA reference labs

- tool: Clay Find Company
- input: 1849 rows from `source-lists/clia-q1-2026/clia_Q1_2026_segmented/bucket_REFERENCE.csv`
- output: 1849 rows enriched (domain + company_linkedin_url added)
- status: done
- manifest: `source-lists/enrichment-runs/2026-05-10_reference-1849_clay/manifest.md`

## [2026-05-10] 2026-05-10_all-2039_exa — Exa-based domain enrichment on combined 2039 (190 russian + 1849 reference)

- tool: Exa web search
- input: 2039 rows (russian-190 + reference-1849 combined)
- output: 2039 rows merged final (`exa_FINAL_all_2039.csv`); ran in stages: test_50 → full_690 → ref_500-1849 → FINAL
- status: done — alternative/supplement to Clay enrichment
- manifest: `source-lists/enrichment-runs/2026-05-10_all-2039_exa/manifest.md`

## [2026-05-11] 2026-05-11_reference-1849_apollo-people — Apollo people search for CEO/Owner/Lab Director contacts

- tool: Apollo.io (people search, `mixed_people/api_search`)
- input: 1849 rows from reference segment (`source-lists/segments/bucket_REFERENCE_domains.csv`)
- output: **1097 contacts** (535 ceo_owner, 292 lab_director, 270 medical_director); 40 skipped (no domain); ~52% hit rate. Re-run saved Apollo `id` per contact → `output_with_ids.csv` (1252 contacts) for downstream Reveal.
- status: done — emails require hydration (Apollo returns has_email flag only, not actual email)
- manifest: `source-lists/enrichment-runs/2026-05-11_reference-1849_apollo-people/manifest.md`

## [2026-05-11] 2026-05-11_reference-1849_findymail-email — Email hydration + double-verify for Apollo contacts

- tool: Apollo Reveal (`/people/bulk_match` by id) + FindyMail (`/api/verify` + `/api/search/name`)
- input: 1252 Apollo contacts (from re-run with IDs)
- output: **344 verified contacts** across 270 unique companies (698/1849 CLIA records = 37.8%). 281 enriched / 738 not-enriched company splits.
- credits: Apollo Reveal 1033 ($1.03) + FindyMail verify 1033 (~$10.33) + FindyMail misses 1 ($0.01) + earlier wasted 32 (~$0.32) = **~$11.70**
- key finding: Apollo `verified` flag has 14.4% real bounce rate — double-verify mandatory before SmartLead
- status: done — feeds SmartLead via `final_contacts_verified.csv`
- manifest: `source-lists/enrichment-runs/2026-05-11_reference-1849_findymail-email/manifest.md`
- analytics: `source-lists/enrichment-runs/2026-05-11_reference-1849_findymail-email/analytics.md`
