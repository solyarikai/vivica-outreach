# Battle Card — LabWare × Medical Director

> Competitor: [[labware]] | Persona: [[persona-medical-director]]

Prospect runs **LabWare**, you're writing to the **Medical Director**.

## Setup

**Prospect signals**: same as `labware_x_ceo-owner.md`.

**Persona signals**:
- Title contains: Medical Director, CLIA Director, Pathologist
- MD/DO with pathology training

## Lead with these pains

Top LabWare pain themes that resonate with a Medical Director specifically:

1. **Audit-trail granularity** — gaps that get cited in CAP inspections
2. **E-signature workflows** — clunky, multi-click for routine validation/release
3. **Result modification controls** — too easy for techs to edit without flag
4. **Complex result types** (narrative AP, structured molecular) — represented as plain text rather than first-class

## Quote pool (≤15 words each)

After `lims-pain-extractor` runs, replace with real quotes. Scaffolds:

- _"Audit logs require manual export and stitching for inspections."_ — paraphrase scaffold
- _"Result modifications don't always trigger the expected supervisor flag."_ — paraphrase scaffold
- _"Narrative reporting workflow is awkward for surgical pathology."_ — paraphrase scaffold

## CTA — what to ask for

Medical Directors are **vetoers**, not buyers. They want to assess clinical quality risk:

- ✅ "Want a sample audit-trail export from a CAP-accredited Vivica customer?"
- ✅ "Curious how we represent narrative AP reports vs LabWare's text fields?"
- ✅ "Worth 10 min to walk through CAP Phase II checklist mapping?"
- ❌ "Schedule a demo" — they don't book demos cold
- ❌ Anything that sounds like sales

## Objections to expect

| Objection | Response |
|---|---|
| "How do I know Vivica meets compliance standards?" | "Built around CLIA/CAP/HIPAA controls. Every action logged with user, timestamp, prior value, new value, reason. Want a sample audit-trail export from a CAP-accredited customer?" |
| "These cloud systems oversimplify clinical data." | "We support narrative reporting, structured fields, attached images, version-controlled interpretation templates. Acure runs full surgical pathology on it — narrative reports, not just CBCs." |
| "We've validated all our methods on LabWare." | "Mirror phase imports your existing validation docs and links them to methods. You're re-confirming, not re-validating. We've done this for ~50 method transitions." |
| "Has CAP looked at your platform?" | "CAP doesn't certify LIMS — they certify your lab. We help you map our controls to the CAP checklist. Acure passed inspection in 2025 with zero deficiencies tied to the system." |

## Email skeleton

> **Subject**: audit-trail granularity in Vivica vs LabWare
>
> Dr. {{lastName}},
>
> A pathologist on G2 wrote about LabWare: *"[≤15-word quote from corpus]"*
>
> A pattern we've heard from CAP-accredited reference labs that switched to Vivica. Acure Reference Lab — full surgical pathology, joint published study with [KOL] — uses our audit-trail export for inspection prep.
>
> Worth 10 minutes to walk through how CAP Phase II checklist maps to Vivica controls?
>
> {{senderName}}

## What kills this email

- Treating Medical Director as a buyer (route around at your peril)
- Cost talk (CEO's lane)
- Marketing language
- "AI" without specifying what it does and how it's validated
- Russian-origin in-vitro reference (HIPAA panic — and Medical Directors are most sensitive of the three personas)

## Cross-references

- Persona: `../icp/persona-medical-director.md`
- Competitor: `../competitors/labware.md`
- Migration: `../playbooks/three-phase-migration.md`
- Customer: `../case-studies/acure-reference-lab-nj.md`
