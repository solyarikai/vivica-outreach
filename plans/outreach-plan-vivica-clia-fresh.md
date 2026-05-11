# Outreach Plan — Vivica × Recently CLIA-Certified Labs

> Personas: [[persona-ceo-owner]] · [[persona-lab-director]] · [[persona-medical-director]]
> Playbook: [[three-phase-migration]]

**Status**: ready for `/launch` mode 1 (fresh project).
**Owner**: Yana — implementation; Chris (Vivica) — final copy approval; Andrew — russian-speaking subset.
**Target launch date**: as soon as Apollo enrichment + SmartLead account confirmed.
**Source**: this plan is modeled on gtm-mcp's `outreach-plan-fintech.md` reference structure.

---

## Why this is the first campaign

We are launching against the **strongest trigger in the project** — labs that recently received their CLIA certificate. Logic chain:

1. They just got the certificate → they're either operational or about to start operations
2. They likely don't have an entrenched LIMS yet → switching cost is near-zero
3. Sales cycle is short → the lab needs *some* LIMS within weeks, not years
4. Apollo isn't a useful source here — CLIA-status isn't an Apollo data field
5. We have the CMS POS file which IS the canonical source — already on disk, already filtered

**Per `extensions/.claude/skills/clia-source/SKILL.md`, we have a starting universe of 9,193 ICP-matched labs from the Q1 2026 file. After segmentation:**

| Bucket | Count | Plan position |
|---|---|---|
| **POL** (Physician Office Labs) | 5,745 | Primary segment for this plan |
| **REFERENCE** (Independent + Public Health) | 1,849 | Secondary segment for this plan |
| **PSC** (Patient Service Centers) | 499 | Secondary segment for this plan |
| OTHER (low-priority facility types) | 644 | Excluded from this plan |
| UNSUITABLE (hospital, prison, pharmacy, insurance) | 456 | Excluded |
| **Russian candidates (NJ/NY/PA, all buckets)** | 190 | Routed to Andrew via separate plan |

Total addressable for THIS plan: **8,093 labs** (POL + PSC + REFERENCE) minus the 190 russian candidates (handled separately) = **~7,900 labs**.

---

## Project setup (gtm-mcp `/launch` mode 1)

When this plan is fed to `/launch` for the first time, it creates:

```
~/.gtm-mcp/projects/vivica/
  project.yaml                # generated from this plan's "Project metadata" section
  state.yaml                  # initial state
  campaigns/clia-fresh-pol/   # the first sub-campaign (POL bucket)
  runs/run-001.json           # initial run record
  sources/clia_Q1_2026.json   # already exists from clia-source skill
```

### Project metadata

```yaml
slug: vivica
name: Vivica Outreach
offer:
  product: Vivica — cloud-based LIMS for clinical labs
  primary_segment: clinical-laboratories-us
  excluded_segments: [hospital_labs, waived_labs, pharma_rnd]
  target_geos: [us, pr]
  primary_contact: chris@vivica.us  # confirm with Chris
  russian_segment_owner: andrew@vivica.us  # confirm with Andrew

reference_dir: ~/code/vivica-outreach/reference
extensions_dir: ~/code/vivica-outreach/extensions
glossary: ~/code/vivica-outreach/glossary.md

source:
  type: clia_pos_file
  file: ~/code/vivica-outreach/input-data/POS_File_CLIA_Q1_2026.csv
  filter:
    since: '2025-01-01'
    certificate_types: [Compliance, Accreditation]
    exclude_hospital_labs: true
    min_phone_length: 10
  segments:
    primary: [POL, PSC, REFERENCE]
    excluded: [UNSUITABLE, OTHER]

team:
  - name: Yana
    role: pipeline_owner_and_operator
    languages: [ru, en]
  - name: Chris Hilinsky
    role: vivica_us_outreach
    languages: [en]
  - name: Andrew
    role: vivica_russian_segment
    languages: [ru, en]
```

---

## ICP definition

The audience for this plan is **decision-makers at recently CLIA-certified clinical labs that fit Vivica's ICP**.

### Geography
- Primary: USA (50 states)
- Secondary: Puerto Rico (532 labs in our Q1 2026 ICP set — significant)
- Excluded: outside US (we don't have product fit)

### Lab type (must be one of these `GNRL_FAC_TYPE_CD` values)
- `21` Physician Office Lab — primary
- `22` Other Practitioner — POL-like
- `15` Independent Lab → Reference Lab tier
- `24` Public Health Lab → Reference Lab tier
- `03` Ancillary Test Site → PSC tier
- `06` Community Clinic → PSC tier
- `09` FQHC → PSC tier
- `25` Rural Health Clinic → PSC tier

### Lab type EXCLUDED
- `14` Hospital Lab (Epic/Cerner lock-in)
- `23` Prison
- `20` Pharmacy
- `17` Insurance
- `08` ESRD Dialysis
- everything in OTHER bucket

### Certificate status
- **Active** (`PGM_TRMNTN_CD = 00`)
- **Compliance OR Accreditation** (`CRTFCT_TYPE_CD ∈ {1, 4}`) — Waived/PPMP/Registration excluded
- **Certified ≥ 2025-01-01** (the "recently" trigger)
- **Has phone number ≥ 10 digits** (basic contactability)
- **Not flagged as hospital exception** (`HOSP_LAB_EXCPTN_SW = N`)

### Personas to target

Order of priority within each lab:

| Priority | Title patterns | Why |
|---|---|---|
| 1 | CEO, President, Founder, Owner, Managing Partner | Decision authority, especially at small POL/PSC |
| 2 | Lab Director, Lab Manager, Director of Operations | Operational influence, often the first reply at smaller labs |
| 3 | Medical Director, CLIA Director, Pathologist | Veto authority, especially on compliance and clinical-quality questions |

**For PSC and POL** (smaller labs), Persona 1 (CEO/Owner) is often the same person as the operational manager. We send to whoever's listed.

**For Reference Labs**, the three personas are usually distinct people. We target all three with persona-specific sequences.

### People enrichment

This plan **requires Apollo people enrichment** to find emails/titles for the companies. Per gtm-mcp's cost-gating rule, this enrichment requires explicit user approval before each batch.

Estimated Apollo people-enrichment cost (3 personas × ~7,900 companies): **rough order-of-magnitude 24,000 person-lookups, but realistically Apollo will only return matches for ~30-50% of POL companies (small labs have low Apollo coverage)**. Expect 6,000-12,000 actual contact records produced.

---

## Three sequences

This plan generates **three distinct sequences** routed by sub-segment. They share the same overall structure (4 emails + LinkedIn touch) but differ in copy.

### Sequence A — POL (Physician Office Labs)

**Audience**: 5,745 labs in POL bucket, expected ~3,500-4,500 with discoverable contacts.

**Persona priority**: CEO/Owner (often same as everything else at this size).

**Hook**: cost-of-LIMS-decision; what they pick now they'll live with for 5+ years.

**Reference anchor**: keep Acure light — it's a Reference Lab story, may feel oversized for a small POL. Use Acure for credibility-building only ("we run the platform that Acure Reference Lab uses"), not as a peer comparison.

**Email 1 — trigger acknowledgment + framing**

```
Subject: just got your CLIA — quick thought
Hook: "Saw {{companyName}} got CLIA-certified in {{certMonth}}. Congrats."
Body:
  - The decision you make in the next 6-12 months on LIMS will compound for 5+ years
  - Most {{labType}} labs end up either with: (a) cobbled-together spreadsheets that
    break under audit, or (b) enterprise tools that cost more than the lab makes
  - There's a third path
Pivot: "Vivica is the cloud LIMS that runs Acure Reference Lab — $100M+ revenue,
  joint published research with [KOL]. Same platform, scaled for {{labType}}."
CTA: "Worth 15 min to walk through what your first year on a real LIMS looks like?"
```

**Email 2 — three-phase migration (T+4 days)**

```
Subject: how 4-6 weeks beats 6 months
Hook: continuation from Email 1, no reply
Body:
  - Most labs delay LIMS decisions because "switching is too risky"
  - But you're not switching — you're starting
  - We have a 3-phase migration framework for switchers; for new labs, mirror phase
    is just initial setup, ~2 weeks total
Pivot: link to three-phase migration explainer (or include 4-line summary)
CTA: "10 min to see the setup workflow?"
```

**Email 3 — case study angle (T+8 days)**

```
Subject: Acure Reference Lab in NJ
Hook: case study cold open
Body:
  - Joint published study with [KOL]
  - Full surgical pathology runs on Vivica
  - $100M+ Reference Lab — they had options, picked us
  - Why it's relevant to {{companyName}}: the same platform that handles Acure's
    complexity also handles {{labType}}'s simplicity — without enterprise-level cost
CTA: "Want me to share the published study link?" (low-friction CTA)
```

**Email 4 — breakup + ADLM hook (T+12 days)**

```
Subject: closing the loop
Hook: classic breakup
Body:
  - Sounds like timing's not right
  - Two things before I stop emailing:
    1. ADLM is in Anaheim July 26-30 — happy to grab 20 min there if you're attending
    2. If you're considering options on your own, here's the {{topPain}} angle to think
       through (specific 1-2 sentence advice, no pitch)
CTA: "If anything changes, I'm here."
```

**LinkedIn touch (T+15 days, sent via GetSales after Email 4 if no engagement)**

```
Short DM (3 sentences):
  - Reference Email 1 trigger ("congrats on CLIA")
  - One sentence specific to their lab name / specialty if visible
  - "Open to connecting?" — soft connect ask, not pitch
```

### Sequence B — PSC (Patient Service Centers)

**Audience**: 499 labs in PSC bucket; smaller, more tightly fit.

**Persona priority**: CEO/Owner first; Lab Director second.

**Hook**: walk-in / specimen-collection workflow specifics.

**Reference anchor**: PSC reference doesn't exist yet. Use Acure carefully ("the platform behind Acure handles thousands of patient-specimen routings per day"). Avoid promising PSC-specific case studies until Chris confirms one exists.

**Differences from Sequence A**:
- Email 1 hook focuses on **specimen-collection workflow** rather than LIMS-decision framing
- Email 2 emphasizes **client-facing report flexibility** (PSC labs serve multiple physician clients with different report needs)
- Email 3 keeps Acure but pivots to "for a {{labType}} sending {{volumeApprox}} samples/day, here's what changes"
- Email 4 same breakup pattern with ADLM hook

### Sequence C — Reference Labs

**Audience**: 1,849 labs in REFERENCE bucket; biggest deals, longest cycles.

**Persona priority**: split across all three — CEO/Owner, Lab Director, Medical Director — distinct sequences per persona.

**Hook**: depth-of-platform; multi-specialty support; audit-trail + compliance.

**Reference anchor**: Acure full strength. Reference Lab → Reference Lab is direct peer comparison.

**Differences from Sequence A**:
- **Three persona-specific variants** (vs single in Sequence A)
- Email 1 hook is persona-specific:
  - CEO/Owner: TCO vs LabWare-tier alternatives
  - Lab Director: instrument integration depth, audit-pack generation
  - Medical Director: audit-trail granularity, complex result types (narrative AP, structured molecular)
- Email 2 references the relevant playbook (three-phase migration) AND specific persona objection responses from `reference/icp/`
- Email 3 includes the Acure published-study link explicitly (highest-credibility audience, deserves the strongest reference)
- Email 4 ADLM hook is more concrete (Reference Labs more likely to attend with named decision-makers)

**Note on competitor-conquest within Reference Labs**: if `lims-detector` runs and identifies a competitor LIMS, the sequence pivots to a competitor-conquest variant using the appropriate `reference/battle-cards/` file. This is a Sequence C+ variant.

---

## Schedule and cadence

```
Week 0 (project setup):
  Apollo people enrichment for top 1,000 leads (highest-priority POL + REFERENCE)
  Lead approval review — Chris signs off on a 50-lead sample
  SmartLead campaign creation (mode 1: fresh)
  Test emails sent to internal team for QA

Week 1-2 (pilot):
  Send 1,000 leads through full sequence
  Monitor: open rate target >35%, reply rate target >2%, bounce rate <2%
  Daily reply triage (per gtm-mcp `reply-classification` skill)
  Pause / iterate if any metric is off-track

Week 3-4 (scale to next batch):
  If pilot metrics are healthy: expand to next 2,000 leads
  Begin Apollo enrichment for next 2,000 leads in parallel
  First handoff of qualified replies to Chris/Andrew for booked calls

Week 5+ (full scale):
  Continue rolling out batches of 2,000 leads/week until all addressable contacts reached
  Estimated total runway: 4-6 weeks for full ~7,900 lab universe
  Pivot focus to ADLM campaign (~T-6 weeks before conference) per `reference/playbooks/adlm-conference.md`
```

### Send schedule per lead

- Email 1: Tuesday or Wednesday morning (best open rates per industry data)
- Email 2: T+4 days
- Email 3: T+8 days
- Email 4: T+12 days
- LinkedIn DM: T+15 days (if no engagement)

Spacing reflects standard cold-outreach best practice; gtm-mcp's `email-sequence` skill applies these as defaults.

---

## KPIs and target metrics

| Metric | Target | Definition |
|---|---|---|
| **Open rate** | >35% | unique opens / delivered |
| **Reply rate** | >2% | unique replies / sent (any reply, including negative) |
| **Positive reply rate** | >0.7% | "yes interested" / sent |
| **Booked-meeting rate** | >0.3% | scheduled call / sent |
| **Bounce rate** | <2% | hard bounces / sent |
| **Unsubscribe rate** | <1% | unsubs / sent |

These targets are **rough industry-standard for cold B2B SaaS in healthcare-tech**. We'll calibrate to actuals after the first 1,000-lead batch.

### Decision rules at week 2

- All metrics on target → scale to full universe
- Open rate <30% → fix subject lines, hold scaling
- Reply rate <1% → fix Email 1 hook (most likely the issue), hold scaling
- Bounce rate >2.5% → improve email validation, pause sending until fixed
- Unsubscribe rate >1.5% → tone is wrong, full sequence review needed

---

## What to track in `tracking/hypotheses.csv`

This campaign tests several hypotheses:

| Hypothesis | How we measure |
|---|---|
| H1: "Recently CLIA-certified" trigger outperforms broad cold | Compare to baseline (no project baseline yet — establish from this plan) |
| H2: POL responds better to cost-framing than features | A/B subject lines on POL Sequence A: cost-frame vs feature-frame |
| H3: Reference Labs respond better to peer Acure reference | Compare reply rate between Sequences with vs without explicit Acure mention in Email 1 |
| H4: 4-email + LinkedIn beats 4-email alone | Compare engagement on LinkedIn-touched vs no-LinkedIn cohorts |
| H5: Russian candidates routed to Andrew get higher conversion | Compare RU-segment conversion vs non-RU cohort (separate plan, but same campaign timing) |

---

## What's NOT in this plan (out of scope)

- **Russian-speaking segment** → routed to separate plan `outreach-plan-vivica-russian-nj.md` (Andrew leads)
- **Competitor-conquest** sequences for prospects on a known competitor LIMS → separate plan `outreach-plan-vivica-using-labware.md`
- **ADLM 2026 pre-conference** outreach → separate plan `outreach-plan-vivica-adlm-2026.md`
- **Hospital labs**: out forever (Epic/Cerner)
- **Pharma R&D**: out forever (LabWare's market)

---

## Pre-launch checklist (must be checked before `/launch`)

- [ ] Apollo API key in `.env`, gtm-mcp confirms credit balance
- [ ] SmartLead account configured with sender email + warmup confirmed
- [ ] Chris approved Email 1 copy for Sequence A (POL)
- [ ] Chris approved Email 1 copy for Sequence B (PSC)
- [ ] Chris approved Email 1 copy for Sequence C (Reference)
- [ ] Andrew confirmed Russian candidates list goes to him, not this plan
- [ ] Test email sent to Yana, Chris — they all received and verified rendering
- [ ] gtm-mcp `pipeline-state` initialized for project `vivica`
- [ ] `clia-source` skill output (`clia_Q1_2026.json`) in place at `~/.gtm-mcp/projects/vivica/sources/`
- [ ] Russian candidates excluded from this plan's contact universe (held in russian_candidates_nj.csv only)
- [ ] First batch of 1,000 leads enriched by Apollo and reviewed by Chris on a 50-lead sample
- [ ] Reply mailbox monitored — Chris (or rotation) ready to respond within 4 hours during business days
- [ ] `tracking/hypotheses.csv` created with H1-H5 rows ready for population

When all 13 boxes are checked, run `/launch outreach-plan-vivica-clia-fresh.md` from inside the repo with Claude Code + gtm-mcp.

---

## Post-launch monitoring

Daily during weeks 1-2:

- Reply triage (per `reply-classification`): how many positive / neutral / negative / out-of-office
- Open rate by sub-segment (POL vs PSC vs REFERENCE)
- Bounce rate trend (should stabilize by day 3)
- Hand-offs to Chris/Andrew for booked meetings

Weekly during weeks 3+:

- Full KPI review (vs targets table above)
- Hypothesis tracking (`tracking/hypotheses.csv` updated)
- Decision: scale, iterate, or pivot
- Documented in `tracking/decisions-log.md`

---

## Enrichment Results — Reference Segment (2026-05-11)

Two-pass pipeline: Apollo people search → Apollo Reveal (by id) → FindyMail verify (SMTP double-check) → FindyMail search on misses.

### Funnel

| Stage | In → Out | % |
|-------|----------|---|
| Source CLIA records | 1849 | — |
| With valid domain | 1809 | 97.8% |
| Apollo found people | 1252 contacts / 383 domains | 37.6% of unique domains |
| Apollo Reveal verified | 1033 | 82.5% |
| FindyMail SMTP valid | 878 | 85.0% (14.4% bounce dropped) |
| FindyMail name-search on misses | 1 / 219 | 0.5% |
| **Final deduped** | **344 contacts / 270 companies** | |
| **CLIA records covered** | **698 / 1849** | **37.8%** |

### Persona split (344 final)

| Persona | Count | % |
|---------|-------|---|
| CEO / Owner / President | 219 | 63.7% |
| Medical Director / Pathologist | 67 | 19.5% |
| Lab Director / Operations | 58 | 16.9% |

### Coverage

- Avg contacts per enriched company: **1.27**
- 76% of enriched companies have only one persona reached
- Only 9 companies (3.3%) have all 3 personas

### Cost

| Item | $ |
|------|---|
| Apollo Reveal (1033 credits × $0.001) | 1.03 |
| FindyMail verify (1033 × $0.01) | 10.33 |
| FindyMail misses search (1 found) | 0.01 |
| FindyMail wasted (earlier, stopped) | 0.32 |
| **Total** | **~11.70** |

### Key findings

1. Apollo's `verified` flag is unreliable — **14.4% real bounce rate** via SMTP. Double-verify mandatory.
2. FindyMail name-search on Apollo misses is dead with obfuscated names (0.5% hit). Don't repeat.
3. Apollo coverage is the bottleneck — 636 unique domains (62%) had 0 contacts in Apollo.
4. Cost per verified contact: **$0.034**. Cost per enriched company: **$0.043**.

### Files

- `source-lists/enrichment-runs/2026-05-11_reference-1849_findymail-email/final_contacts_verified.csv` — 344 ready-for-SmartLead
- `companies_enriched.csv` — 281 lab rows
- `companies_not_enriched.csv` — 738 lab rows for LinkedIn/Clay/manual enrichment
- `analytics.md` — full funnel breakdown

### Next moves

1. Load 344 contacts → SmartLead campaign per persona-specific sequence
2. Re-enrich 738 unenriched via LinkedIn Sales Nav or Clay (have `company_linkedin_url` from `2026-05-10_all-2039_exa`)
3. Future Apollo enrichments: always save `id` in search, then use Reveal-by-id (not name+domain)

---

## Cross-references

- Sources skill: `../extensions/.claude/skills/clia-source/SKILL.md`
- Detector skill: `../extensions/.claude/skills/lims-detector/SKILL.md` (used in Sequence C+ variants)
- Pain extractor skill: `../extensions/.claude/skills/lims-pain-extractor/SKILL.md` (feeds Sequence C+ competitor-conquest)
- Personas: `../reference/icp/persona-*.md`
- Migration framework: `../reference/playbooks/three-phase-migration.md`
- Russian segment (separate, parallel plan): `../reference/playbooks/russian-segment.md`
- ADLM (separate, follow-on plan): `../reference/playbooks/adlm-conference.md`
- Acure case study: `../reference/case-studies/acure-reference-lab-nj.md`
- Vivica intel: `../reference/company/vivica-intel.md`
- Glossary: `../glossary.md`
