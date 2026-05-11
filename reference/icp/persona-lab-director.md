# Persona — Lab Director / Manager

The operational head of the lab. Runs day-to-day. Owns the tech stack from a usability standpoint. Often a Medical Laboratory Scientist (MLS), Medical Technologist (MT), or someone with 10-20 years on the bench who got promoted. Highly technical about workflows, cautious about change.

> **Source**: Vivica ICP Google Sheet, captured during 2026-Q2 kick-off call.

## Profile

| Attribute | Value |
|---|---|
| Title | Lab Director / Lab Manager / Director of Operations / Operations Manager |
| Background | Often MLS/MT/CT(ASCP), 10+ years bench experience |
| Reports to | CEO/Owner or Medical Director |
| Lives in | Slack/Teams, lab huddle, occasional LIMS user-conferences |
| Tenure | 5-15 years at this lab; usually promoted internally |

## Top goals

What they're measured on:

1. **Hit turnaround time targets** — STAT, routine, send-out — every day, every shift
2. **Pass every inspection** — CLIA biennial, CAP yearly, surprise state visits
3. **Keep error rate near zero** — wrong-patient, wrong-test, wrong-result are career-ending events
4. **Train and retain staff** — turnover in clinical labs runs 15-25%/year, replacing an MT takes 3-6 months
5. **Make month-end QA reports** look clean — competency assessments, proficiency testing, instrument calibration logs

## KPIs they personally watch

- **Turnaround time (TAT)** — by test, by shift, by day, percentile not average
- **Reagent cost per test** — what's drifting up, what's drifting down
- **Specimen rejection rate** — how often samples come in wrong
- **Critical-value notification time** — minutes from result to physician acknowledgment
- **Proficiency testing scores** — CAP PT cycles, blinded survey results
- **Staff competency completion** — % of techs current on every method they perform

## Pain points

What they actually complain about:

- **Manual reagent inventory** — staff spends hours counting bottles every week
- **Instrument integration drift** — every analyzer firmware update breaks the LIS feed for 2 days
- **Reporting templates are inflexible** — every new client wants a different layout, IT charges $$ per change
- **Change controls are slow** — adding a new test code takes 3 weeks of vendor back-and-forth
- **Audit prep eats two weeks every quarter** — pulling logs, screenshots, certifications from five different systems
- **Training new staff** — current LIMS has 200+ screens, takes 6 weeks to onboard

## Buying triggers

When they start asking for a different system:

1. **Failed inspection citation** — specifically calling out documentation gaps or audit-trail issues
2. **Major instrument addition** that current LIMS can't integrate with
3. **Growth past their current LIMS's tier** — locked out of features, forced into expensive upgrade
4. **Lost a key technologist** who was the only one who knew how to fix things in the system
5. **Client demand** for faster turnaround or new report formats they can't deliver
6. **Competitor lab opens nearby** — pressure to modernize or lose business

## Common objections

The exact words we hear (from ICP sheet + kick-off call):

- "**Training staff will be too difficult.**"
- "**Our current system works.**"
- "**We just got everyone trained on the current LIMS.**"
- "**The migration will mess up our QA history.**"
- "**Our instruments are already integrated — we'd lose 6 months redoing that.**"
- "**My team is already overworked.**"
- "**I've heard horror stories about cloud LIMS being slow.**"

## Objection responses

| Objection | Response |
|---|---|
| "Training staff will be too difficult." | "We handle onboarding and training — most labs are fully up and running without disrupting operations. Average time to live: 4-6 weeks." |
| "Our current system works." | "Glad to hear it. The labs that switched to us said the same — until they hit a growth ceiling or an inspection finding. What does the next 12 months look like for you?" |
| "Migration will mess up QA history." | "We import your full QA + competency + PT history during the mirror phase. You keep the full audit trail. Want a sample data-mapping spec from a similar lab?" |
| "Instruments are already integrated." | "We support the same HL7/ASTM/POCT1-A interfaces — our integration team copies your existing mappings. Your instruments don't need to change." |
| "Team is overworked." | "Right — which is why we do the migration heavy lift, not your team. Mirror phase needs about 8 hours from your bench team total, spread over 2 weeks." |
| "Cloud LIMS is slow." | "Latency is sub-100ms for our worst-served regions. We can give you a benchmark login on Acure's environment so you can stress-test it yourself before any commitment." |

## How Vivica solves their problems

- **Familiar workflows**: configurable to mirror their existing LIMS day one — staff doesn't have to relearn everything
- **Migration team does the heavy lift**: their team contributes ~8 hours of bench knowledge total
- **Full audit trail preserved**: QA, PT, competency history imported, not abandoned
- **Cloud means no patches at 2am**: no more weekend maintenance windows breaking Monday operations
- **Reporting flex**: drag-drop report builder, no dev tickets for layout changes
- **Validated instrument integrations**: standard HL7/ASTM/POCT1-A interfaces, plus a library of pre-built analyzer profiles
- **Instant audit pack**: CLIA / CAP / state inspection prep generates from the system in <1 hour

## What works in the first email

- Subject referencing a **specific operational pain** (TAT, reagent inventory, inspection prep)
- Quote from a competitor's G2 review hitting that exact pain
- Hint at a peer lab (anonymized) that solved it
- CTA: "Want to see how [peer lab] cut audit prep from 2 weeks to 2 days?"

## What kills the email

- "Revolutionize your lab" / "Transform your operations" — they hate hyperbole
- Anything that sounds like it bypasses Lab Director and goes to CEO directly
- Promising features they know don't exist in any LIMS
- In-vitro case study verbatim (triggers HIPAA concern — see russian-segment playbook)
- Talking about cost (that's CEO's lane — Lab Director cares about workflow)

## Cross-references

- Battle card vs LabWare: `../battle-cards/labware_x_lab-director.md`
- Battle card vs Clinisys: `../battle-cards/clinisys_x_lab-director.md`
- Battle card vs lims.net (JTO): `../battle-cards/lims-net_x_lab-director.md`
- Three-phase migration framework: `../playbooks/three-phase-migration.md`
- Acure case study: `../case-studies/acure-reference-lab-nj.md`
