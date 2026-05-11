# Battle Card — Clinisys × CEO / Owner

> Competitor: [[clinisys]] | Persona: [[persona-ceo-owner]]

Prospect runs **Clinisys** (or one of its acquired brands: Sunquest, Horizon), you're writing to the **CEO / Owner**.

## Setup

**Prospect signals** (from `lims-detector`):
- Patient portal iframe matches `*.clinisys.com` or `*.sunquestinfo.com`
- Job postings reference Sunquest, Horizon, or Clinisys

**Persona signals**: title contains CEO, President, Founder, Owner, Managing Partner.

## Lead with these pains

Top Clinisys pain themes for CEO/Owner:

1. **Modernization roadmap is slow** — they've been promised cloud for years; install base still on aging on-prem
2. **Vendor lock-in** — accumulated customizations make exits painful
3. **Multi-product portfolio confusion** — was it Sunquest? Horizon? CoPath? — every one has a different roadmap
4. **TCO drift** — license renewals come with surprises

## Quote pool (≤15 words each)

After `lims-pain-extractor` runs, replace with real quotes. Scaffolds:

- _"Modernization timeline keeps slipping; we keep paying for legacy."_ — paraphrase scaffold
- _"Customizations from years ago make any change a project."_ — paraphrase scaffold

## CTA

- ✅ "Worth 15 min to compare TCO including the modernization investment you'd avoid?"
- ✅ "Curious how Acure modernized incrementally without waiting for vendor's cloud roadmap?"
- ❌ Demos, generic "let's chat"

## Objections to expect

| Objection | Response |
|---|---|
| "We've used [Sunquest / Clinisys / Horizon] for 15 years." | "That's exactly why incremental matters. You don't lose the institutional knowledge — three-phase migration mirrors your current config first, validates in parallel, then decommissions service-line by service-line." |
| "Switching costs more than waiting for their cloud upgrade." | "Worth modeling. Most customers find that the cumulative annual cost of waiting (legacy maintenance + customization fees + delayed feature gains) crosses the migration cost in 18-24 months." |
| "Clinisys is too big to fail." | "Vendor stability is a real concern. Acure Reference Lab — \$100M+ revenue, joint published study — bet on Vivica after evaluating exactly that question. Want their CIO's number?" |

## Email skeleton

> **Subject**: incremental migration off Sunquest / Clinisys
>
> Hey {{firstName}},
>
> A Lab Director on G2 wrote about Clinisys: *"[≤15-word quote from corpus]"*
>
> Most labs that switched to Vivica from a Sunquest/Horizon/Clinisys deployment said the same. Acure Reference Lab in NJ — \$100M+ revenue — went live with us in [X] weeks via a 3-phase migration that didn't disrupt operations.
>
> Worth 15 minutes to walk through how that incremental approach worked?
>
> {{senderName}}

## What kills this email

- Naming the wrong Clinisys brand (saying "Sunquest" to a Horizon customer feels sloppy)
- Hyperbole
- Cost-only pitch (CEOs care, but they care more about risk and continuity)

## Cross-references

- Persona: `../icp/persona-ceo-owner.md`
- Competitor: `../competitors/clinisys.md`
- Migration: `../playbooks/three-phase-migration.md`
- Customer: `../case-studies/acure-reference-lab-nj.md`
