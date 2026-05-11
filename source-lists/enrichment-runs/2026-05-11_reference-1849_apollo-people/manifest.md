# Run: 2026-05-11_reference-1849_apollo-people

**Date**: 2026-05-11
**Tool**: Apollo.io (people search)
**Operator**: Yana (setup); awaiting Apollo credentials

## Source

Reference labs segment (1849 companies):
- Input: `source-lists/segments/bucket_REFERENCE_domains.csv` (1849 rows with domains)

## Purpose

Find CEO/Owner and Lab Director contacts for reference labs (independent + public health lab networks, typically 100-1000 person organizations).

Per [[outreach-plan-vivica-clia-fresh]], target 3 personas per company in order of priority:

| Priority | Persona | Titles to match |
|----------|---------|-----------------|
| 1 | CEO / Owner | CEO, President, Founder, Owner, Managing Partner |
| 2 | Lab Director | Lab Director, Lab Manager, Director of Operations, Operations Manager |
| 3 | Medical Director | Medical Director, CLIA Director, Pathologist, Director of Pathology |

## Input

Sample: 20 companies (`input.csv`) for testing Apollo query pattern
Full run: 1849 companies

Columns: `name`, `domain`, `city`, `state`, `clia_number`

## Expected Output

Per company:
- CEO/Owner: email, name, title, LinkedIn URL, phone
- Lab Director: email, name, title, LinkedIn URL, phone
- Medical Director: email, name, title, LinkedIn URL, phone

Format: `output.csv` with columns:
```
src_name, src_domain, src_clia, persona, contact_name, contact_email, contact_title, contact_linkedin, contact_phone
```

## Status

**completed** — 2026-05-11

| Metric | Value |
|--------|-------|
| Companies in | 1849 |
| No domain (skipped) | 40 |
| Hit (people found) | ~966 (~52%) |
| Miss (no people) | ~843 (~46%) |
| Contacts out | **1097** |
| ceo_owner | 535 |
| lab_director | 292 |
| medical_director | 270 |

Notes: emails are `(require direct fetch)` — Apollo people search returns `has_email` flag only, not actual email. Need Apollo bulk_match or FindyMail to hydrate. Large chains (LabCorp, Quest, cdph.ca.gov) appear multiple times → dedup before loading to campaign.

## Execution

Script created: `apollo_people_search.py` — batch queries Apollo for all 3 personas per company.

```bash
# Test on sample 20
python3 apollo_people_search.py input.csv output.csv --test 20

# Full run on 1849
python3 apollo_people_search.py input.csv output.csv
```

Requires: `GTM_MCP_APOLLO_API_KEY` environment variable set (from `~/.gtm-mcp/.env`)

## Next steps

1. **Verify Apollo API access** — test endpoint directly, check account permissions
2. **Run test on sample 20 companies** — validate persona matching logic
3. **Scale to full 1849** — batch process with rate limiting
4. **For Russian segment (190)** — await Andrew's confirmation of russian-speaking labs before enriching
5. **Merge results** → create `sources/contacts/` in `~/.gtm-mcp/projects/vivica/` for downstream campaign launch

## Notes

- Apollo search via domain lookup + title/role filtering for 3 personas per company
- Expected success rate: ~60-70% (not all labs have public LinkedIn presence, especially smaller POLs)
- Cost: Apollo charges per contact found — budget TBD after test run
- Some fields (email, direct phone) may require additional API calls or paid tier access
