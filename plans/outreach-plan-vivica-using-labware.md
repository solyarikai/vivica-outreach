# Outreach Plan — Vivica × Labs Currently Using LabWare

> Personas: [[persona-ceo-owner]] · [[persona-lab-director]]
> Competitor conquest: [[labware]] | Battle cards: [[labware_x_ceo-owner]] · [[labware_x_lab-director]]
> Playbook: [[three-phase-migration]]

**Status**: parallel plan to `outreach-plan-vivica-clia-fresh.md` and `outreach-plan-vivica-russian-nj.md`. Targets a different audience from a different angle.
**Owner**: Yana — implementation; Chris (Vivica) — copy approval.
**Source**: this plan handles labs identified by `lims-detector` skill as currently running LabWare.

> **Why this plan exists**: LabWare is the global LIMS market leader. Their installed base is large, mostly long-tenured, and well-documented in pain corpus. Targeting them with **specific pain quotes** from their own user reviews is the highest-precision conquest play we have. Per Rinat's note in kick-off: "we did this for a CRM project — figured out which CRM each company used, then wrote competitor-specific messages." This plan operationalizes that for LabWare.

---

## How this plan generates its audience

Unlike the CLIA-fresh plan (which starts from a CMS file), this plan starts from **detection**. The audience is built incrementally as `lims-detector` runs across companies that pass other filters:

```
1. Source → companies (could be CLIA file OR Apollo OR ADLM attendees)
   ↓
2. lims-detector skill → enrich each company with current_lims field
   ↓
3. Filter: where current_lims.vendor == 'labware' AND confidence >= 0.7
   ↓
4. THIS plan picks up the filtered set
```

Expected audience size depends on detector run scope:
- Run on full 8,093-lab CLIA-fresh universe → expect 50-200 LabWare users (LabWare skews larger labs, fewer in CLIA-fresh)
- Run on Reference-Lab subset only (1,849 labs) → expect higher density of LabWare hits, maybe 100-300
- Run on broader Apollo-sourced clinical-lab universe (if we expand sourcing) → expect 500-1,500 LabWare users

The sequence quality matters more than volume here. LabWare conquest is a **precision play**, not volume play.

---

## Project setup

This plan runs as a **separate campaign** inside the same `vivica` project:

```
~/.gtm-mcp/projects/vivica/
  campaigns/
    clia-fresh-pol/             # main plan
    clia-fresh-psc/
    clia-fresh-reference/
    russian-nj/                 # russian segment plan
    using-labware/              # ← THIS plan
```

Use `/launch` mode 2 (new campaign in existing project).

### Campaign metadata

```yaml
campaign_slug: using-labware
parent_project: vivica
detection_source: lims-detector
detection_filter:
  vendor: labware
  min_confidence: 0.7
audience_dynamic: true  # audience grows as lims-detector runs more
sender:
  name: Chris Hilinsky
  email: chris@vivica.us  # confirm
language: en
```

---

## Audience requirements

A lab is in scope for this plan ONLY if ALL of these are true:

- ✅ `lims-detector.current_lims.vendor == 'labware'`
- ✅ `lims-detector.current_lims.confidence >= 0.7` (high-confidence detection only)
- ✅ Already passed standard ICP filter (active CLIA, non-hospital, ≥10-digit phone)
- ✅ NOT in russian-speaking segment (those go to the Russian plan)
- ✅ Lab type ∈ {POL, PSC, REFERENCE} (no UNSUITABLE / OTHER)
- ✅ Has at least one Apollo-enriched contact in priority personas

If detection confidence is below 0.7, the lab is **NOT** added to this plan. Lower-confidence detections fall back to the generic CLIA-fresh sequence.

---

## Sequence pattern — built around the pain corpus

This is where `lims-pain-extractor` skill earns its keep. Every email in this sequence pulls from the LabWare entry in `~/.gtm-mcp/projects/vivica/competitor_pains/corpus.json`.

Required corpus state:
- Top 3 LabWare pain themes ranked by score
- One ≤15-word quote per theme (already enforced by the skill)
- Source URL per quote (already required)

If `lims-pain-extractor` hasn't been run yet on the LabWare URL set, **block this plan from launch** until it has. The whole point of the plan is the corpus.

### Email 1 — pain quote + Acure pivot

The strongest possible cold-email pattern: a real user complaint about LabWare from a public review, attributed, then the bridge.

```
Subject: that LabWare {{topThemeShort}} headache
  topThemeShort examples: "integration", "implementation timeline", "customization cost"

Body structure:

  Hook (2 sentences):
    "A Lab Director on G2 wrote about LabWare: '{{quote ≤15 words}}'
    Most clinical labs that switched from LabWare to Vivica say the same thing."

  Credibility (2 sentences):
    "Acure Reference Lab in NJ — $100M+ revenue, joint published study with [KOL] —
    runs surgical pathology and clinical chemistry on us today."

  Pain bridge (2 sentences):
    "Their team contributed about 8 bench-hours total to migration; we did the rest.
    Live in {{X}} weeks with full QA history preserved."

  CTA (1 sentence):
    Persona-specific (see below).

  Sign-off:
    First-name from Chris.
```

### CTA per persona

| Persona | CTA |
|---|---|
| CEO/Owner | "Worth 15 min to compare TCO including the LabWare customization spend you'd avoid?" |
| Lab Director | "Want to see how the {{topThemeShort}} pain looks day-to-day on Vivica vs your current setup?" |
| Medical Director | "Want a sample audit-trail export from a CAP-accredited Vivica customer to compare?" |

Source: `reference/battle-cards/labware_x_*.md` — every CTA in this plan must match what's in the battle card for that persona.

### Email 2 — second pain (T+4 days)

Different pain theme from the corpus, same structural pattern:

```
Subject: another pattern we've heard from LabWare migrations

Body:
  Acknowledge no reply ("noticed Email 1 didn't land — different angle...")
  Quote pain theme #2 from corpus (different theme than Email 1)
  Reference: a generic peer-lab pattern (without naming, since Acure's already in Email 1)
  CTA: invite to a specific 10-minute walk-through on this exact pain
```

### Email 3 — three-phase migration framework (T+8 days)

Pivots from "here's another pain" to "here's how the switch actually works":

```
Subject: the LabWare-to-Vivica migration timeline

Body:
  Acknowledge: "switching from LabWare is the part everyone underestimates"
  Three-phase framework explanation (mirror → proxy → decommission)
  Concrete timeline for their lab type:
    - POL: ~8 weeks
    - PSC: ~10 weeks
    - Reference: ~16 weeks
  Compare to LabWare migrations of 12-24 months (industry-standard for that vendor)
  CTA: "10 min to walk through the timeline for {{labType}} specifically?"
```

### Email 4 — breakup with ADLM hook (T+12 days)

```
Subject: closing the loop on LabWare comparison

Body:
  Classic breakup acknowledgment
  Two parting offers:
    1. ADLM in Anaheim July 26-30 — we'll be on the floor, happy to grab 20 min
    2. If you're considering anyway, here's the {{topPain}} angle worth thinking through
       (specific 1-2 sentences, no pitch)
  Sign-off: "If anything changes, I'm here."
```

### LinkedIn touch (T+15 days)

Sent via GetSales if no engagement on emails. Same competitor-anchor:

```
3 sentences:
  - "Saw {{companyName}} runs LabWare — common pattern in our migration conversations"
  - One sentence specific to detected lab specialty
  - "Open to connecting?"
```

---

## What kills this plan's emails

- ❌ Quoting >15 words from any LabWare review — copyright violation
- ❌ Using more than ONE quote per source URL across all 4 emails to one prospect
- ❌ Mentioning LabWare in a way that sounds bashing rather than pattern-recognition
- ❌ Russian-origin in-vitro reference (this audience is US-mainstream)
- ❌ Promising migration faster than the timeline table (POL <6 weeks, PSC <8, Reference <12)
- ❌ Inventing customer counts ("hundreds of labs migrated from LabWare" — we have one prominent customer)
- ❌ Generic "transform" / "revolutionize" language

---

## Schedule and KPIs

This is a precision play; volume is lower but per-lead quality should be higher than CLIA-fresh.

```
Week 0:
  Verify lims-pain-extractor has run on LabWare and produced corpus
  Apollo enrichment for first batch (~50 leads) of detected LabWare users
  Chris approves Email 1 copy with the actual top quote inserted

Week 1-2:
  Send first batch (~50 leads)
  Monitor metrics
  Iterate Email 1 copy if reply rate <2%

Week 3+:
  Continue rolling out batches as lims-detector identifies more LabWare users
```

| Metric | Target (vs CLIA-fresh main plan) |
|---|---|
| Open rate | >40% (vs >35% main) — competitor-anchor subject lines outperform |
| Reply rate | >3% (vs >2%) — pain-anchored emails get replies |
| Positive reply rate | >1% (vs >0.7%) |
| Booked-meeting rate | >0.5% (vs >0.3%) |
| Bounce rate | <2% (same) |

---

## Hypothesis testing

Add to `tracking/hypotheses.csv`:

| Hypothesis | How we measure |
|---|---|
| H10: LabWare-pain-quote in Email 1 outperforms generic Email 1 | Compare reply rate vs main CLIA-fresh Sequence A on similar lab types |
| H11: Email 3 migration-timeline pivot drives meeting bookings | Track meeting bookings attributed to Email 3 vs other emails in sequence |
| H12: This conquest plan outperforms CLIA-fresh on Reference-Lab segment | Same lab types in both plans; compare conversion |

---

## Pre-launch checklist (this plan only)

- [ ] `lims-pain-extractor` run on LabWare URL set — corpus exists at `~/.gtm-mcp/projects/vivica/competitor_pains/corpus.json`
- [ ] Top 3 LabWare pain themes have actual ≤15-word quotes (not scaffold placeholders)
- [ ] `lims-detector` run on at least one batch of CLIA-fresh leads — has produced LabWare hits with ≥0.7 confidence
- [ ] Battle cards (`labware_x_*.md`) reviewed and aligned with email copy
- [ ] Chris approved Email 1 copy with the actual top LabWare pain quote inserted
- [ ] Chris approved Email 2-4 copy
- [ ] Reply-handling cadence: Chris commits to <4h response on positive replies during business days
- [ ] Apollo enrichment for the first 50 detected leads completed
- [ ] Russian candidates excluded from this plan's audience (held in russian-nj plan only)

---

## Variants for other competitors

The same pattern can be cloned for other competitors. Suggested order:

1. **labware** ← this plan (largest installed base)
2. **clinisys** — second-priority conquest, large legacy installed base
3. **lims-net** (JTO) — smaller US footprint, but high overlap with russian segment
4. labvantage, ligolab — Tier 2, do later

When cloning this plan for another competitor, replace:
- `vendor: labware` → `vendor: <slug>`
- All references to "LabWare" → competitor display name
- Pain quotes from LabWare corpus → competitor's corpus
- Battle cards `labware_x_*.md` → `<competitor>_x_*.md`

Don't run more than 2-3 conquest plans in parallel. Burn-in capacity on the SmartLead side and Chris's reply-handling capacity are real constraints.

---

## Cross-references

- Detection skill: `../extensions/.claude/skills/lims-detector/SKILL.md`
- Pain extraction skill: `../extensions/.claude/skills/lims-pain-extractor/SKILL.md`
- LabWare competitor profile: `../reference/competitors/labware.md`
- Battle cards: `../reference/battle-cards/labware_x_ceo-owner.md`, `_x_lab-director.md`, `_x_medical-director.md`
- Three-phase migration framework: `../reference/playbooks/three-phase-migration.md`
- Acure case study: `../reference/case-studies/acure-reference-lab-nj.md`
- Main plan (broader audience): `outreach-plan-vivica-clia-fresh.md`
- Glossary: `../glossary.md` → "LabWare", "Competitor-conquest"
