# Battle Card — Clinisys × Medical Director

> Competitor: [[clinisys]] | Persona: [[persona-medical-director]]

Prospect runs Clinisys/Sunquest/Horizon, writing to **Medical Director**.

## Setup

**Persona signals**: Medical Director, CLIA Director, Pathologist.

## Lead with these pains

1. **Audit trail in legacy modules** — gaps when inspectors ask granular questions
2. **Reflex testing logic hardcoded** — every change is a vendor ticket
3. **AP module age** — surgical pathology workflows in legacy modules feel dated
4. **SOP version control** — proving which SOP was active on a given date

## Quote pool (≤15 words each)

After `lims-pain-extractor`:

- _"Audit-trail exports require manual stitching for inspections."_ — paraphrase scaffold
- _"Reflex rule changes go through vendor change-control queues."_ — paraphrase scaffold

## CTA

- ✅ "Want a sample audit-trail export from a CAP-accredited Vivica customer?"
- ✅ "Curious how reflex rules are user-editable in Vivica vs vendor ticket in Clinisys?"

## Objections to expect

| Objection | Response |
|---|---|
| "We've validated our methodology on Sunquest for years." | "Mirror phase imports validation docs and links them to methods. You're re-confirming, not re-validating. ~50 method transitions documented." |
| "Audit trail must be defensible." | "Every action logged with user, timestamp, prior value, new value, reason. Export-ready for CAP Phase II checklist. Acure passed 2025 inspection with zero system-related deficiencies." |
| "Reflex testing rules are too critical to edit ourselves." | "Configurable with role-based controls — Medical Director or designee modifies, with mandatory reason codes and supervisor approval where you set them. No vendor tickets." |

## Email skeleton

> **Subject**: audit-trail granularity vs Sunquest / Clinisys
>
> Dr. {{lastName}},
>
> A pathologist on G2 about Clinisys: *"[≤15-word quote]"*
>
> Pattern we've heard from CAP-accredited reference labs that switched. Acure Reference Lab — full surgical pathology, joint published study with [KOL] — uses Vivica's audit-trail export directly for CAP Phase II prep.
>
> Worth 10 min to walk through how the checklist maps to Vivica controls?
>
> {{senderName}}

## What kills this email

- Treating Medical Director as buyer
- Cost talk
- Generic "AI" claims
- Russian in-vitro reference

## Cross-references

- Persona: `../icp/persona-medical-director.md`
- Competitor: `../competitors/clinisys.md`
- Migration: `../playbooks/three-phase-migration.md`
- Customer: `../case-studies/acure-reference-lab-nj.md`
