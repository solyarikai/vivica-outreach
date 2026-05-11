# Persona — CEO / Owner

The decision-maker at small POL/PSC labs and the ultimate buyer at Reference Labs. This persona controls budget and signs contracts. They typically didn't come from a lab background — they're entrepreneurs, physicians who own the practice, or executives running a multi-site operation.

> **Source**: Vivica ICP Google Sheet, captured from Sally Hypothesis dashboard during 2026-Q2 kick-off call. This file mirrors that source verbatim — when the Sheet updates, this file updates.

## Profile

| Attribute | Value |
|---|---|
| Title | CEO / Founder / Owner / President |
| Org size | 1-50 employees (POL/PSC); 50-500 (Reference) |
| Reports to | Board / themselves / private equity |
| Lives in | LinkedIn DMs, email, occasional industry conferences |
| Tenure | Often founder, 5+ years at the lab |

## Top goals

What they're trying to achieve (in order of how often they bring it up):

1. **Grow revenue** — more tests/month, more billable services, expand test menu
2. **Reduce operational cost** — labor, software, compliance overhead
3. **De-risk the business** — pass CLIA inspections, pass CAP audits, avoid HIPAA fines
4. **Scale without proportional headcount** — automation that lets the same team handle 2× volume
5. **Exit-readiness** — clean books, clean tech, clean processes (for eventual sale or PE rollup)

## KPIs they personally watch

- **Revenue per test** — gross margin trend by service line
- **Days to result** — turnaround time, billing-cycle length
- **Inspection score** — most recent CLIA / CAP / state inspection deficiencies
- **Cost per sample** — fully-loaded cost including software, labor, reagents
- **Tech-stack TCO** — total annual spend on LIS+LIMS+billing+integrations

## Pain points

What keeps them up at night:

- **Manual data entry between systems** — every keystroke is a billing error waiting to happen, and labor is 60%+ of operating cost
- **Compliance is one missed update from a fine** — a single failed CAP audit can shut them down for 90 days
- **Current LIMS is a black box** — they pay six figures and have no visibility into what staff actually does with it
- **Switching cost feels prohibitive** — they've heard horror stories of 12-month migrations that broke labs
- **Vendor lock-in** — feature roadmaps controlled by the vendor, custom requests cost thousands per change order

## Buying triggers

When they actively start shopping:

1. **Just received CLIA certificate** — they need a LIMS now, before they start running tests, or they're cobbling together spreadsheets
2. **Lost a major contract** because their reporting was too slow
3. **Failed a recent inspection** — usually drives 6-12 months of platform reconsideration
4. **Acquired by PE** — new investors push for tech consolidation
5. **Lab Director just quit** — they're rethinking the whole stack
6. **Renewal of legacy LIMS** — annual contract, sticker shock on price increase

## Common objections

The exact language we hear (verbatim from kick-off call + ICP sheet):

- "**We're fine with what we have.**" (default position)
- "**This will disrupt operations.**"
- "**Cost vs ROI is unclear.**"
- "**We'd rather wait until our current contract ends.**"
- "**Our staff is already trained on the current system.**"
- "**Switching is a 12-month nightmare.**"

## Objection responses

How we answer each (these come straight from the ICP sheet — use them verbatim or close):

| Objection | Response |
|---|---|
| "We're fine with what we have." | "Most of our customers said the same six months before they switched. Worth 15 minutes to compare cost-per-test side by side?" |
| "This will disrupt operations." | "That's exactly why we run our 3-phase migration: we mirror your current LIMS in Vivica first, then proxy live workflows in parallel. Your team doesn't switch until you're confident." |
| "Cost vs ROI is unclear." | "We'll build you a TCO model with your actual test volume and labor numbers. If Vivica doesn't pay for itself in year one, we don't expect you to sign." |
| "Wait until contract ends." | "Most customers wait — and then realize migration takes longer than the renewal window. Starting the mirror phase now means you're ready to flip on the renewal date with zero downtime." |
| "Staff is already trained." | "Our onboarding takes most labs from kickoff to live in 4-6 weeks. We do the heavy lifting on training; your team focuses on tests." |
| "Migration is a nightmare." | "It is — for vendors that throw you a manual and run. Acure Reference Lab in NJ went live with us in 6 weeks. Want their CIO's number?" |

## How Vivica solves their problems

The product story we tell (frame: "you'll grow faster, sleep better, exit cleaner"):

- **Cloud-native — no IT overhead**: no servers, no patching, no DBA. They redirect that headcount to revenue-generating work.
- **3-phase migration framework**: mirror → proxy → decommission. Their existing LIMS keeps running until Vivica is fully validated. (See `../playbooks/three-phase-migration.md`.)
- **Audit-ready by default**: CLIA, CAP, HIPAA controls baked in. Every action is logged, every change is versioned, every audit ready in hours not weeks.
- **Predictable cloud pricing**: per-sample tiered, no per-user surprises, no mandatory consulting fees on every change.
- **One stack**: LIS + LIMS + reporting + billing integration in one platform. They retire 2-3 vendors when they switch to us.
- **Public reference**: Acure Reference Lab (NJ, $100M+) is live, joint published study with KOL.

## What works in the first email

The hook patterns that get this persona to reply (per gtm-mcp's email-sequence rules and Vivica-specific tuning):

- Subject reference to a **recent inspection** or **growth event** (acquisition, new test menu)
- Open with a **quote from a public competitor review** that names their pain
- One sentence of credibility (Acure customer, joint study with KOL)
- A **single, narrow CTA** — never "book a call", always "have you considered X?" or "worth a TCO comparison?"

## What kills the email

- "Schedule a 30-min demo" in the first email
- Long lists of features
- Anything that sounds like a vendor pitch
- Mentioning the Russian origin of the in-vitro case study (triggers HIPAA/data-security panic — see `../playbooks/russian-segment.md`)

## Cross-references

- Battle card vs LabWare: `../battle-cards/labware_x_ceo-owner.md`
- Battle card vs Clinisys: `../battle-cards/clinisys_x_ceo-owner.md`
- Battle card vs lims.net (JTO): `../battle-cards/lims-net_x_ceo-owner.md`
- Three-phase migration framework: `../playbooks/three-phase-migration.md`
- Acure case study: `../case-studies/acure-reference-lab-nj.md`
