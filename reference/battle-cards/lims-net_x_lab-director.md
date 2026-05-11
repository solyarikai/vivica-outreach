# Battle Card — lims.net (JTO) × Lab Director

> Competitor: [[lims-net]] | Persona: [[persona-lab-director]]

Prospect runs lims.net, writing to **Lab Director / Manager**.

## Setup

Same prospect signals as `lims-net_x_ceo-owner.md`. Persona: Lab Director, Lab Manager, Director of Operations.

**Russian-segment check first** — if owner is russian-speaking, route to Andrew (`../playbooks/russian-segment.md`).

## Lead with these pains

1. **US instrument integration gaps** — analyzers common in US clinical (especially specific to your specialty) may need custom work on lims.net
2. **CLIA/CAP-specific workflows** that the platform handles generically
3. **Reporting templates** for US payers / clients
4. **Time-zone support friction**

## Quote pool (≤15 words each)

After `lims-pain-extractor`:

- _"Support hours don't align with US lab schedules."_ — paraphrase scaffold
- _"US-specific workflows need custom configuration."_ — paraphrase scaffold

## CTA

- ✅ "Want to see how a {{specialization}} workflow looks on Vivica vs your current setup?"
- ✅ "Curious how the CAP Phase II checklist maps to Vivica controls vs lims.net?"

## Objections to expect

| Objection | Response |
|---|---|
| "Our team is trained on lims.net." | "Mirror phase replicates the workflows you know. Day 1 in Vivica looks similar to your team. Modernization happens incrementally." |
| "Instruments are integrated already." | "Standard HL7/ASTM/POCT1-A interfaces — we copy your existing mappings. Instruments don't get touched." |
| "Cloud LIMS feels less reliable than what we have on-prem." | "We can give you a benchmark login on Acure's environment. Stress-test it on your worst-case scenario before any commitment." |

## Email skeleton

> **Subject**: how Acure handles {{specialization}} on Vivica
>
> Hey {{firstName}},
>
> Saw {{companyName}} runs lims.net. A reviewer wrote: *"[≤15-word quote]"*
>
> Common pattern with US labs on EU-origin platforms — workflows fit, but with workarounds. Acure's bench team contributed about 8 hours to migrate; we did the rest. Live in {{X}} weeks.
>
> Worth 10 minutes to walk through {{specialization}} day-to-day?
>
> {{senderName}}

## What kills this email

- Bashing the platform's origin
- Russian in-vitro reference
- Going over their head

## Cross-references

- Persona: `../icp/persona-lab-director.md`
- Competitor: `../competitors/lims-net.md`
- Russian-segment overlap: `../playbooks/russian-segment.md`
- Migration: `../playbooks/three-phase-migration.md`
