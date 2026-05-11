# Battle Card — LabWare × CEO / Owner

> Competitor: [[labware]] | Persona: [[persona-ceo-owner]]

When you've detected the prospect runs **LabWare** and you're writing to the **CEO / Owner**, this is the playbook.

## Setup

**Prospect signals** (from `lims-detector`):
- Patient portal iframe matches `*.labware.com` or `*.labware-online.com`
- Job postings reference "LabWare LIMS administration"
- DNS CNAME on `results.<domain>` points to LabWare hosting

**Persona signals** (from Apollo enrichment):
- Title contains: CEO, President, Founder, Owner, Managing Partner

## Lead with these pains

Top LabWare pain themes that resonate with a CEO/Owner specifically:

1. **Cost of ownership** — base license is just the start; customizations and professional services accumulate
2. **Implementation risk** — a 12-24 month implementation is a known LabWare pattern; CEOs lose sleep over project risk that big
3. **Vendor lock-in** — every config change is a billable change order

## Quote pool (≤15 words each, from public reviews)

When `lims-pain-extractor` runs, replace these with real quotes from the corpus. Until then, these are scaffolds:

- _"Integration with other instrument software needed more efforts."_ — G2 review (≤15 words example)
- _"Customization is powerful but every change is expensive and slow."_ — paraphrase scaffold
- _"Implementation took longer than planned and cost more than budgeted."_ — paraphrase scaffold

**Rule**: only ONE quote per email. Once used in an email, that quote is closed for that prospect.

## CTA — what to ask for

This persona doesn't book demos in cold email. Ask for **comparison**, not commitment:

- ✅ "Worth 15 minutes to compare cost-per-test side by side?"
- ✅ "Want a TCO model with your actual volume numbers?"
- ✅ "Curious how Acure cut [specific metric] without the typical 12-month migration?"
- ❌ "Schedule a demo" — too heavy a lift for cold
- ❌ "Reply to this email" — too vague, no value exchange

## Objections to expect

| Objection (CEO version) | Response |
|---|---|
| "We already invested heavily in LabWare." | "I get it — sunk cost is real. The labs that switch usually do it because forward cost (annual customization + license + services) is higher than switching cost. Worth a side-by-side?" |
| "LabWare is the safe choice — we can't risk a smaller vendor." | "Acure Reference Lab in NJ — \$100M+ revenue — runs on Vivica with a published study. They evaluated the same vendor-stability question. Want to talk to their CIO?" |
| "Switching is a 12-month nightmare." | "Switching from LabWare done badly is a 12-month nightmare. Done with our 3-phase mirror → proxy → decommission, it's typically 4-6 weeks at the lab side. We do the heavy lift." |

## Email skeleton (sequence-ready)

> **Subject**: that LabWare integration headache
>
> Hey {{firstName}},
>
> A Lab Director on G2 wrote about LabWare: *"[≤15-word quote from corpus]"*
>
> Most clinical labs that migrated to Vivica from LabWare tell us the same. Acure Reference Lab in NJ — \$100M+ revenue, full surgical pathology — went live with us in [X] weeks without that pain.
>
> Worth 15 minutes to walk through how the migration actually works for a {{labType}} like {{companyName}}?
>
> {{senderName}}

## What kills this email

- Mentioning Vivica's customer count (we have one — don't lead with it)
- Quoting LabWare reviews >15 words
- Trying to sell features (CEO doesn't care; route through TCO / risk / migration)
- Hyperbole ("revolutionary", "game-changing", "transform")
- Russian-origin in-vitro reference (HIPAA panic — see `../playbooks/russian-segment.md`)

## Cross-references

- Persona detail: `../icp/persona-ceo-owner.md`
- Competitor detail: `../competitors/labware.md`
- Migration framework: `../playbooks/three-phase-migration.md`
- Customer reference: `../case-studies/acure-reference-lab-nj.md`
