# Run: 2026-05-11_reference-1849_findymail-email

**Date**: 2026-05-11
**Tool**: Apollo Reveal (bulk_match by id) + FindyMail (verify + name search)
**Operator**: Sales Engineer + Claude

## Source

- Apollo people output (re-run with IDs): `../2026-05-11_reference-1849_apollo-people/output_with_ids.csv` (1252 contacts across 383 domains)

## Purpose

Hydrate verified emails for Apollo-found contacts at reference labs.
Two-pass: (1) Apollo Reveal by `id` → (2) FindyMail SMTP verify on Apollo emails + name search on Apollo misses.

## Status

**completed** — 2026-05-11

See `analytics.md` for full funnel breakdown.

| Metric | Value |
|--------|-------|
| Contacts in (Apollo found) | 1252 |
| Apollo Reveal verified | 1033 (82.5%) |
| FindyMail re-verified valid | 878 (14.4% bounce dropped) |
| FindyMail misses → found | 1 / 219 |
| **Final unique contacts (deduped)** | **344** |
| Unique companies enriched | 270 |
| CLIA records covered | 698 / 1849 (37.8%) |
| **Total cost** | **~$11.70** |

## Execution

```bash
# 1. Apollo Reveal (full)
python3 apollo_reveal.py ../2026-05-11_reference-1849_apollo-people/output_with_ids.csv reveal_full.csv

# 2. FindyMail double-verify (Apollo verified emails)
python3 findymail_verify.py reveal_full.csv verify_full.csv

# 3. FindyMail name search on Apollo misses
python3 findymail_misses.py reveal_full.csv misses_searched.csv

# 4. Merge + dedup + build final lists
python3 build_final_lists.py
```

Requires:
- `GTM_MCP_APOLLO_API_KEY` (from `~/.gtm-mcp/.env`)
- `FINDYMAIL_API_KEY` (hardcoded fallback in scripts; GetSally key)

## Outputs

| File | Rows | What |
|------|------|------|
| `companies_enriched.csv` | 281 | Lab companies with ≥1 verified contact |
| `companies_not_enriched.csv` | 738 | Lab companies needing other enrichment methods |
| `final_contacts_verified.csv` | 344 | Deduped contacts ready for SmartLead |
| `reveal_full.csv` | 1252 | Raw Apollo Reveal output |
| `verify_full.csv` | 1033 | FindyMail verify on Apollo emails |
| `misses_searched.csv` | 219 | FindyMail name search on Apollo misses |

## Key Findings

1. **Apollo `email_status=verified` is unreliable** — 14.4% bounce rate when double-checked via FindyMail SMTP. Double verification is mandatory.
2. **FindyMail name-search on Apollo misses is dead** — 1/219 (0.5%) found. Obfuscated first_name + bad domains kill it.
3. **Apollo coverage is the bottleneck** — 636 domains had 0 contacts in Apollo (59% of unique domains). Need LinkedIn/Clay/manual for these.
4. **3-persona ICP coverage rare** — only 9 of 270 enriched companies have all 3 personas. 76% have just one contact.

## Next steps

1. Load `final_contacts_verified.csv` (344) → SmartLead campaign
2. Re-run unenriched 738 via LinkedIn Sales Nav / Clay (have `company_linkedin_url` from `2026-05-10_all-2039_exa` run)
3. Don't reuse FindyMail name-search on obfuscated names — Apollo Reveal by ID is the right path
