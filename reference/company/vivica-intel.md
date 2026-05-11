# Vivica — company intel

The single product reference that every skill, plan, and email sequence pulls from when it needs to talk about Vivica. If a fact about the product gets used in outreach, it lives here first.

> **Status**: working draft based on kick-off call + ICP sheet + public site (vivica.us). Verified facts are marked ✓; assumptions are marked ?. Update when Chris/Andrew share new material.

## What Vivica is

✓ Cloud-based LIMS for clinical laboratories in the United States.
✓ Combined LIS + LIMS functionality (lab info system + management system in one platform).
✓ Targets POL, PSC, and Reference labs — explicitly **not** hospital labs (Epic/Cerner lock-in is well understood).
✓ Headquartered in the US.

## Customers

| Status | Lab | Notes |
|---|---|---|
| ✓ Active | **Acure Reference Lab** (NJ) | $100M+ revenue. Full case study at `case-studies/acure-reference-lab-nj.md`. Joint published study with KOL — usable in cold emails. |
| ✓ Churned | _name not public_ | Lab closed, not a product issue. Per kick-off call. |

That's it. **One active customer at the start of this project.** This is reality, not a weakness — the Acure proof point is unusually strong (Reference Lab + $100M+ revenue + published research). Don't oversell breadth; lean hard on Acure depth.

## Product capabilities (what we say in emails)

These are the headline capabilities we'll reference in sequences. Confirm with Chris before any new feature appears in sent copy.

| Capability | Detail |
|---|---|
| ✓ Cloud-native | Multi-tenant SaaS on AWS US-region |
| ✓ HIPAA-compliant | BAA standard with every customer |
| ? SOC 2 | Type II claimed in messaging — confirm cert active and date |
| ✓ HL7 / ASTM / POCT1-A interfaces | Standard for instrument integration |
| ✓ Configurable workflows | Mirror existing LIMS workflows during migration |
| ✓ Audit trail | Every action logged with user/timestamp/before/after/reason |
| ✓ E-signature | Integrated into validation, amendment, release workflows |
| ✓ Multi-result types | Numeric, qualitative, narrative, imaging, structured molecular |
| ✓ Reporting | Drag-drop report builder, no dev tickets for layout changes |
| ? Billing integration | Confirm which billing systems are pre-integrated |
| ? Patient portal | Web portal for patients to access results — confirm available + branded |

## Core differentiation (what makes us not LabWare/Clinisys/QBench)

In rough order of emphasis:

1. **Three-phase migration framework** — `mirror → proxy → decommission`. The big incumbents force a rip-and-replace, which terrifies labs. We don't. (Full detail: `playbooks/three-phase-migration.md`.)
2. **Cloud-native, no on-prem option** — LabWare/Clinisys default to on-prem, which means IT overhead. We don't have that legacy.
3. **Predictable pricing** — per-sample tiered, no per-user surprises, no mandatory consulting fees on every change request.
4. **Anatomic + clinical pathology in one platform** — many cloud LIMS skip AP because slide imaging is hard. We don't (Acure runs surgical pathology on it).
5. **One-platform consolidation** — labs typically retire 2-3 vendors when they move to Vivica (separate billing, separate reporting, separate AP system).

## Competitive positioning per persona

| Persona | What we lead with |
|---|---|
| CEO/Owner | TCO, ease of switching, exit-readiness |
| Lab Director | Migration heavy lift on us, audit-pack generation, instrument integrations |
| Medical Director | Audit trail depth, e-sig, complex result types (narrative, structured molecular) |

## Pricing (rough)

✓ Per-sample tiered pricing.
? Specific tiers and discounts not yet confirmed for this project — Chris to share.
✓ No mandatory consulting fees for typical configuration changes.

**Rule for cold outreach**: never quote a price in an email. Always route price discussion to a call where Chris (English) or Andrew (Russian) can scope it properly.

## Tone of voice

Based on the existing site and kick-off call:

- **Direct**, not flowery. "We mirror your existing LIMS in 4-6 weeks" beats "We deliver transformative migration experiences."
- **Specific**, not vague. Use numbers (4-6 weeks, $100M+ Acure revenue, sub-100ms latency) wherever possible.
- **Technical**, not marketing. Lab Directors and Medical Directors detect marketing-speak immediately and write the email off.
- **Confident, not boastful**. We have one customer; we don't pretend to have fifty.

Russian-language outreach has a different tone — see `playbooks/russian-segment.md`.

## What we DON'T claim (hard rules)

- ❌ Don't claim a customer count Vivica doesn't have. Say "Acure plus a growing customer base" — never invent numbers.
- ❌ Don't claim FDA clearance unless explicitly confirmed for a specific module.
- ❌ Don't claim CAP "certified" — CAP doesn't certify LIMS, they certify labs (see Medical Director objection responses).
- ❌ Don't claim AI features that aren't in production. If a feature is roadmap, it's not for cold outreach.
- ❌ Don't reference the Russian origin of the in-vitro case study to non-Russian-speaking US labs (HIPAA / data-security panic). See `playbooks/russian-segment.md`.

## Public assets we can link

- vivica.us — main site
- ? Joint publication with KOL via Acure — link TBD (Chris to share)
- ? Demo video — confirm if shareable in cold outreach

## Internal contacts (for plan author + email reviewer)

| Person | Role | When to involve |
|---|---|---|
| Chris Hilinsky | Co-founder, US market | Approves any new English-language sequence; provides product detail |
| Andrew | Russian-speaking segment lead | Approves any Russian-language sequence; vets russian-speaking candidates from `clia-source` |
| Evgenia Farikh | LinkedIn (optional) | Available as third LinkedIn sender if SmartLead/GetSales rotation needs it |

## Cross-references

- Personas: `icp/persona-ceo-owner.md`, `icp/persona-lab-director.md`, `icp/persona-medical-director.md`
- Three-phase migration: `playbooks/three-phase-migration.md`
- Russian segment rules: `playbooks/russian-segment.md`
- Flagship customer: `case-studies/acure-reference-lab-nj.md`
- Glossary: `../../glossary.md`
