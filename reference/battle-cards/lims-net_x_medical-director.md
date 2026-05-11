# Battle Card — lims.net (JTO) × Medical Director

> Competitor: [[lims-net]] | Persona: [[persona-medical-director]]

Prospect runs lims.net, writing to **Medical Director**.

## Setup

Persona: Medical Director, CLIA Director, Pathologist. **Russian-segment check first.**

## Lead with these pains

1. **CAP/CLIA-specific audit trail expectations** — generic platform may not match Phase II checklist directly
2. **US-clinical complex result types** — narrative AP, structured molecular — handled generically
3. **E-signature with US compliance reasoning** — workflows may need configuration
4. **HIPAA / BAA posture** for US data handling

## Quote pool (≤15 words each)

After `lims-pain-extractor`:

- _"US compliance workflows require additional configuration."_ — paraphrase scaffold

## CTA

- ✅ "Want a sample audit-trail export from a CAP-accredited Vivica customer?"
- ✅ "Curious how Vivica maps to CAP Phase II checklist vs your current setup?"

## Objections to expect

| Objection | Response |
|---|---|
| "How do I know Vivica meets US compliance standards?" | "Built around CLIA/CAP/HIPAA controls. SOC 2 Type II. BAA standard. Every action logged with user, timestamp, prior value, new value, reason. Sample audit-trail export available." |
| "We've validated our methods on lims.net." | "Mirror phase imports validation docs and links them to methods. Re-confirming, not re-validating." |
| "Where does our data live?" | "US-region AWS, encrypted at rest and in transit. BAA standard. You control retention, access, audit." |

## Email skeleton

> **Subject**: CAP Phase II mapping in Vivica vs lims.net
>
> Dr. {{lastName}},
>
> A pathologist wrote about lims.net: *"[≤15-word quote from corpus]"*
>
> Common with US clinical labs on EU-origin platforms — generic compliance posture rather than US-clinical-native. Acure Reference Lab — full surgical pathology, joint published study with [KOL] — uses Vivica's audit-trail export directly for CAP Phase II prep.
>
> Worth 10 min to walk through the mapping?
>
> {{senderName}}

## What kills this email

- Bashing the platform's origin
- Russian in-vitro reference (especially sensitive for Medical Director)
- Treating them as buyer
- Cost talk

## Cross-references

- Persona: `../icp/persona-medical-director.md`
- Competitor: `../competitors/lims-net.md`
- Russian-segment overlap: `../playbooks/russian-segment.md`
- Migration: `../playbooks/three-phase-migration.md`
