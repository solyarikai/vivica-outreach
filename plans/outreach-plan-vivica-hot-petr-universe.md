# Outreach Plan — Vivica × Petr's HOT Universe (S+/S Tier)

> Personas: [[persona-ceo-owner]] · [[persona-lab-director]] · [[persona-medical-director]]
> Source: [[lab-universe-2026-05]] (Petr, 2026-05-12)

**Status**: planning — enrichment pipeline not yet started
**Owner**: TBD
**Priority**: HIGHEST — this is the freshest, most intent-rich segment in the project

---

## Why this is the next campaign

This is a completely different population from the reference-lab segment we ran in May:
- Reference labs (old campaign): **established labs** by facility type — many have LIMS already
- HOT universe (this campaign): **recently opened labs** — CLIA/NPI issued ≤12 months ago, likely no LIMS yet

The trigger here is **operational freshness**, not lab type. A lab that got its CLIA 90 days ago is still buying every piece of infrastructure — LIMS, LIS, billing, EHR. We're calling at exactly the right moment.

---

## Universe

| Tier | Count | Signal |
|------|-------|--------|
| **S+** | 21 | CLIA + NPI both ≤6mo, standalone, verified domain |
| **S** | 173 | CLIA-licensed ≤12mo, Compliance or Accreditation cert |
| **Total HOT** | **194** | Start here this week |

> Note: manifest says 204, sheet has 194 rows — 10 likely reclassified or removed during QA.

### What Petr's data already gives us (no enrichment needed)

| Signal | Coverage |
|--------|----------|
| Verified website | 95 / 194 (49%) |
| Contact name from CLIA POS | 85 / 194 (44%) |
| Phone from CLIA/NPPES | ~180 / 194 (~93%) |
| CLIA cert type | 100% |
| State + city + address | 100% |

**Top states**: TX (29), FL (21), WA (21), NY (20), CA (18)

### Source breakdown

| Sources | Count | Meaning |
|---------|-------|---------|
| C only (CLIA) | 109 | Licensed but no NPI yet — earliest stage |
| CN (CLIA + NPI) | 66 | Fully ready: licensed + billing NPI |
| CNM (CLIA + NPI + Medicare) | 9 | Moving fast — all three in ≤6mo |
| N only (NPI) | 10 | Pre-license or dataset miss |

---

## What we need before we can send

### Step 1 — Domain enrichment (for the 99 without verified website)

**Tool**: Clay (Find Company) or Exa company_research
**Input**: 99 labs without `Website (verified)` from HOT tab
**Output**: domain, company_linkedin_url
**Estimate**: 99 Clay credits, ~1 hour

### Step 2 — People enrichment (3 personas per lab)

Same pipeline as reference-lab run:

```
Apollo people search by domain
→ Apollo Reveal (email by ID)
→ FindyMail SMTP verify
→ deduplicate by email
```

**Personas**: CEO/Owner · Lab Director · Medical Director
**Expected hit rate**: ~38% domain coverage (per reference-lab analytics)
**Expected output**: ~75 contacts (194 × 38% × 1.02 contacts/company)

> Hit rate may be higher than reference-lab run: these are fresher companies,
> less likely to have people info in Apollo. LinkedIn may be more important here.

### Step 3 — LinkedIn fallback for Apollo misses

For labs where Apollo returns 0 people (expected: ~60% of domains):
- Use `company_linkedin_url` from Clay → Clay waterfall to pull employees
- Priority: HOT labs (S+) get manual check if all automated methods fail

### Step 4 — CLIA contact as backup

85 labs have a contact name + phone from CLIA POS (`Contact first`, `Contact last`, `Contact phone`).
For labs where email enrichment fails completely → use CLIA contact for cold call.
This is a direct ownership-level contact, often the Authorized Official.

---

## Email copy angle

**Core angle**: "You just opened. You're about to figure out your lab workflow. Here's why LIMS matters now, not later."

This is fundamentally different from the reference-lab campaign angle (migration/switch). Here we're talking to people who haven't bought anything yet.

Key points for copy:
- No "switch from your current system" — they don't have one
- Focus on: setup speed, compliance out of the box, cloud = no IT needed
- Urgency: getting LIMS right from day 1 is 10x easier than retrofitting later
- Social proof: other labs at your stage (≤6 months) use Vivica

Sequence structure (carry over from `outreach-plan-vivica-clia-fresh.md`):
- Email 1: Trigger-based open ("I saw you recently got your CLIA in [State]")
- Email 2: Product angle (specific to their cert type — Compliance/Accreditation)
- Email 3: Social proof + CTA
- Optional step 4: CLIA contact phone if no reply

---

## Execution order

| Phase | What | Count | Tool | When |
|-------|------|-------|------|------|
| 1 | Export HOT tab to CSV | 194 | Python/xlsx | Now |
| 2 | Domain enrichment (missing websites) | ~99 | Clay | Day 1 |
| 3 | Apollo people search | all 194 domains | Apollo MCP | Day 1–2 |
| 4 | FindyMail SMTP verify | Apollo output | FindyMail MCP | Day 2 |
| 5 | LinkedIn fallback (Apollo misses) | ~120 domains | Clay | Day 2–3 |
| 6 | Build final_contacts_hot.csv | all verified | Python | Day 3 |
| 7 | SmartLead sequence upload | contacts | SmartLead | Day 3–4 |
| 8 | Launch | — | SmartLead | Day 4 |

---

## After HOT — MEDIUM wave (1,675 labs)

Once HOT is in sequence, start MEDIUM (Tier A/B):
- **A** (1,124 labs): CLIA ≤12mo, Registration/PPM cert — one tier below S
- **B** (541 labs): NPI-only, no CLIA match yet — pre-license or data miss

MEDIUM needs same enrichment pipeline but at higher volume. Budget ~3x the cost of HOT run.

---

## Files

| File | Location | Status |
|------|----------|--------|
| Source xlsx | `source-lists/lab-universe-petr-2026-05/lab-universe-2026-05.xlsx` | ready |
| HOT export CSV | `source-lists/lab-universe-petr-2026-05/hot_204.csv` | **TODO** |
| Enrichment run | `source-lists/enrichment-runs/YYYY-MM-DD_hot-194_*` | not started |
| Final contacts | `source-lists/segments/final_contacts_hot.csv` | not started |

---

## Open questions before launch

1. **Cert type filter**: include PPM (28 labs in HOT)? PPM = limited complexity, smaller ops. Chris to decide.
2. **SmartLead sender**: use same domain as reference-lab campaign or separate inbox for HOT?
3. **CLIA contact as channel**: do we want to run phone outreach in parallel for S+ (21 labs)?
4. **MEDIUM timing**: start immediately after HOT upload, or wait for HOT reply data first?

---

## Related

- [[lab-universe-2026-05]] — full tier definitions and methodology
- [[outreach-plan-vivica-clia-fresh]] — reference-lab campaign (separate population)
- `source-lists/segments/tier_summary.md` — tier distribution of existing enriched leads
