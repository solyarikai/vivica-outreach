# Battle Card — LabWare × Lab Director / Manager

> Competitor: [[labware]] | Persona: [[persona-lab-director]]

Prospect runs **LabWare**, you're writing to the **Lab Director / Manager**.

## Setup

**Prospect signals**: same as `labware_x_ceo-owner.md`.

**Persona signals**:
- Title contains: Lab Director, Lab Manager, Director of Operations, Operations Manager
- Background often MLS / MT / CT(ASCP) per `persona-lab-director.md`

## Lead with these pains

Top LabWare pain themes that resonate with a Lab Director specifically:

1. **Instrument integration brittleness** — every analyzer firmware update breaks the LIS feed
2. **Reporting inflexibility** — every new client format is a vendor ticket
3. **Training burden** — 200+ screens, 6-week onboarding for new techs
4. **Audit prep eats two weeks every quarter** — the team's least favorite time

## Quote pool (≤15 words each)

After `lims-pain-extractor` runs, replace these with real quotes:

- _"Integration with other instrument software needed more efforts."_ — G2 example (9 words)
- _"Reports are powerful but every change requires the vendor."_ — paraphrase scaffold
- _"Training new staff on every screen takes weeks."_ — paraphrase scaffold

## CTA — what to ask for

Lab Directors care about workflow specifics. Ask for a **workflow comparison**, not a demo:

- ✅ "Want to see how Acure cut audit prep from 2 weeks to 2 days?"
- ✅ "Curious how we handle [specific instrument] integrations without the firmware-update breakage?"
- ✅ "Worth 10 minutes to walk through a specific {{specialization}} workflow side by side?"
- ❌ "Schedule a demo" — too heavy
- ❌ Cost questions — that's CEO's lane

## Objections to expect

| Objection | Response |
|---|---|
| "We just got everyone trained on LabWare." | "Training on a new system takes 2-4 weeks for most labs (vs LabWare's 6+). Acure's team picked it up while LabWare was still running in parallel — no double-training pain." |
| "Migration will mess up QA history." | "We import your full QA + competency + PT history during mirror phase. You keep the audit trail. Want a sample data-mapping spec from a similar lab?" |
| "Instruments are already integrated with LabWare." | "We support the same HL7 / ASTM / POCT1-A interfaces. Our integration team copies your existing mappings — your instruments don't get touched. Migration team contributes ~95% of the work; your bench team contributes ~8 hours total." |
| "I've heard cloud LIMS is slow." | "Latency is sub-100ms in our worst-served regions. We can give you a benchmark login on Acure's environment so you can stress-test it yourself before any commitment." |

## Email skeleton

> **Subject**: how Acure handles {{instrumentOrWorkflow}} on Vivica
>
> Hey {{firstName}},
>
> Saw your team is on LabWare. A Lab Director on G2 wrote: *"[≤15-word quote from corpus]"*
>
> Same pattern at Acure Reference Lab in NJ before they switched. Their team contributed about 8 hours of bench time to the migration — we did the rest. Live in {{X}} weeks, full QA history preserved.
>
> Want a 10-minute walkthrough of how the {{specialization}} workflow looks day-to-day?
>
> {{senderName}}

## What kills this email

- Anything sounding like marketing ("revolutionize", "transform")
- Cost discussion (Lab Director will route to CEO and lose control)
- Promising features that don't exist
- Mentioning Russian origin of in-vitro case study (HIPAA panic)
- Going over their head — Lab Directors who feel bypassed kill deals

## Cross-references

- Persona: `../icp/persona-lab-director.md`
- Competitor: `../competitors/labware.md`
- Migration: `../playbooks/three-phase-migration.md`
- Customer: `../case-studies/acure-reference-lab-nj.md`
