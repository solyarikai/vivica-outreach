# Analytics — Reference Labs Email Enrichment Funnel

**Run**: 2026-05-11_reference-1849_findymail-email
**Date**: 2026-05-11
**Segment**: Reference labs (CLIA Q1 2026)
**Goal**: Verified email addresses for CEO/Owner + Lab Director + Medical Director personas

---

## Funnel (Top → Bottom)

| # | Stage | Input | Output | Conversion | Loss |
|---|-------|-------|--------|------------|------|
| 1 | Source CLIA records | — | 1849 | — | — |
| 2 | After domain enrichment (Clay+Exa) | 1849 | 1809 (1019 unique) | 97.8% | 40 no-domain |
| 3 | Apollo people search | 1019 domains | 1252 contacts (383 domains) | 37.6% domain hit | 636 domains had 0 contacts |
| 4 | Apollo Reveal (email by ID) | 1252 | 1033 verified | 82.5% | 219 misses |
| 5 | FindyMail verify (SMTP check) | 1033 | 878 valid | 85.0% | 149 invalid (14.4% bounce) + 6 other |
| 6 | FindyMail search on misses | 219 | 1 found | 0.5% | 218 dead |
| 7 | Dedup by email | 879 | **344 unique contacts** | 39.1% | 535 duplicates (chain locations) |
| 8 | Unique companies enriched | 270 | — | — | — |
| 9 | CLIA records covered | 698 / 1849 | — | **37.8%** | 1151 not enriched |

---

## Persona Breakdown (final 344 contacts)

| Persona (Apollo classification) | Count | % |
|---------------------------------|-------|---|
| ceo_owner | 219 | 63.7% |
| medical_director | 67 | 19.5% |
| lab_director | 58 | 16.9% |

### Actual title buckets (parsed from `contact_title`)

| Title group | Count | % |
|-------------|-------|---|
| CEO / President / Founder / Owner | 221 | 64.2% |
| Medical Director / Pathologist | 63 | 18.3% |
| Lab Director / Operations | 59 | 17.2% |
| Other | 1 | 0.3% |

CEO/Owner persona is overrepresented (label matches title closely — Apollo classifier reliable).

---

## Contacts Per Company

| Contacts | Companies | % |
|----------|-----------|---|
| 1 | 205 | 75.9% |
| 2 | 56 | 20.7% |
| 3 | 9 | 3.3% |

**Average**: 1.27 contacts per enriched company. 76% of enriched companies have only one persona reached — full ICP coverage (3 personas) is rare.

---

## Email Quality

- Apollo `email_status=verified` flag has **14.4% real bounce rate** (per FindyMail SMTP check)
- → Double verification saved ~149 dirty emails from SmartLead. Sender reputation protected.
- 1 email from FindyMail misses pass came back as `verified=false` (so dropped during dedup if invalid).

---

## Cost Per Outcome

| Metric | Value |
|--------|-------|
| Total cost (Apollo + FindyMail) | ~$22.70 |
| Cost per verified contact | $0.034 |
| Cost per enriched company | $0.043 |
| Cost per CLIA record covered | $0.017 |

Breakdown:
- Apollo Reveal: $10.33 (1033 credits × $0.01)
- FindyMail verify: ~$10.33 (1033 × $0.01)
- FindyMail misses (wasted): ~$0.01 (1 credit) + 32 credits wasted in earlier run (~$0.32)
- Apollo search endpoints: $0 (free)

---

## Where We Lost Coverage (1151 of 1849 CLIA records not enriched)

| Reason | Count | % of source |
|--------|-------|-------------|
| Apollo had 0 people for domain | 636 domains (~1100 CLIA records) | ~59% |
| Apollo found people, all email misses | 219 / 270 lost contacts | ~12% |
| Source had no domain | 40 records | 2.2% |

**Apollo coverage is the bottleneck**, not email verification.

---

## Next Steps for 738 Unenriched Companies

1. **LinkedIn Sales Navigator**: 636 domains missing from Apollo likely have profiles on LinkedIn (especially small POL/reference labs)
2. **Clay enrichment** on `company_linkedin_url` (already have from earlier run) — pull employees directly
3. **Manual scraping** of small lab About pages — typical for POL/reference labs where Apollo lags
4. **Skip very low-value** segment (no domain + no LinkedIn) — unlikely worth the cost

---

## Files

- `companies_enriched.csv` — 281 lab rows with verified emails attached (270 unique by deduped contact)
- `companies_not_enriched.csv` — 738 lab rows needing other methods
- `final_contacts_verified.csv` — 344 ready-for-SmartLead contacts
- `reveal_full.csv` — raw Apollo Reveal output (1252 rows)
- `verify_full.csv` — FindyMail verify output (1033 rows)
- `misses_searched.csv` — FindyMail name-search on Apollo misses (219 rows)
