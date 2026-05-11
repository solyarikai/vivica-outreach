# Outreach Plan — Vivica × ADLM 2026 Conference

> Personas: [[persona-ceo-owner]] · [[persona-lab-director]] · [[persona-medical-director]]
> Playbook: [[adlm-conference]]
> Reference: [[acure-reference-lab-nj]]

**Status**: time-boxed campaign, hard deadline 26 July 2026.
**Owner**: Chris (English) + Andrew (Russian) lead at the booth; Yana operates campaigns day-to-day and coordinates pre-conference and post-conference flows.
**Source**: ADLM 2026 confirmed-attendee list (acquisition path TBD per [[adlm-conference]]).

> **Critical**: this plan is **time-bound**. It activates ~T-6 weeks (mid-June 2026) and concludes T+3 weeks post-conference (mid-August 2026). Outside that window, prospects roll back to evergreen segment campaigns.

---

## Conference fact sheet

- **Dates**: 26-30 July 2026
- **Location**: Anaheim Convention Center, CA
- **Attendance**: ~15,000 attendees, 850+ exhibitors
- **As of project start (10 May 2026)**: ~11 weeks until conference
- **Outreach window**:
  - Pre-conference: ~mid-June to 19 July (5-6 weeks)
  - Onsite: 26-30 July (5 days)
  - Post-conference: 31 July to 21 August (3 weeks)

Full operational detail in [[adlm-conference]]. This plan is the **execution layer** that uses that playbook.

---

## Project setup

Runs as a separate campaign inside `vivica` project. `/launch` mode 2.

```
~/.gtm-mcp/projects/vivica/
  campaigns/
    clia-fresh-pol/
    clia-fresh-psc/
    clia-fresh-reference/
    russian-nj/
    using-labware/
    adlm-2026-pre/      # ← THIS plan (pre-conference)
    adlm-2026-onsite/   # ← THIS plan (during conference, manual-driven)
    adlm-2026-post/     # ← THIS plan (post-conference)
```

Three sub-campaigns reflect the three operational phases. Each has different audience filters, sequences, and SmartLead/GetSales config.

### Campaign metadata

```yaml
campaign_slug: adlm-2026
parent_project: vivica
phases:
  pre_conference:
    sub_slug: adlm-2026-pre
    starts: 2026-06-15
    ends: 2026-07-19
  onsite:
    sub_slug: adlm-2026-onsite
    starts: 2026-07-26
    ends: 2026-07-30
    mode: manual_with_smartlead_assist  # not full automation
  post_conference:
    sub_slug: adlm-2026-post
    starts: 2026-07-31
    ends: 2026-08-21
booth: TBD  # confirm with Chris — does Vivica have a booth? Number?
team_onsite:
  - Chris Hilinsky
  - Andrew (russian-speaking conversations only)
  - Evgenia Farikh (optional support)
language_split:
  en: Chris
  ru: Andrew
```

---

## Audience pipeline

```
Step 1 (now): acquire ADLM 2026 attendee list
  Options:
    a. AACC official list (paid)
    b. Public registration scrape if available
    c. LinkedIn signal mining ("attending ADLM 2026" / "see you at ADLM" posts)
    d. Hybrid (start with public + LinkedIn, supplement from official if budget allows)

  Decision needed from Chris/Andrew: which option, what budget.

Step 2 (T-7 weeks): filter the attendee list against Vivica ICP
  Apply same filter as CLIA-fresh plan:
    - Exclude hospital lab attendees
    - Exclude pharma R&D attendees
    - Exclude vendor employees (peers, not prospects)
    - Keep POL / PSC / Reference Lab attendees
    - Keep relevant titles: CEO, Lab Director, Medical Director (and their variants)

Step 3 (T-6 weeks): Apollo enrichment
  Most ADLM attendees will already have public emails on the registration list.
  For those that don't, Apollo enrichment fills the gap.

Step 4 (T-6 weeks): split by language
  Russian-speaking owners → Andrew's parallel sequence (Russian-language)
  Everyone else → Chris's English-language sequence

Step 5 (T-6 weeks): split by current-LIMS knowledge
  If lims-detector ran on attendee's lab → competitor-anchor variant
  If unknown → generic-Vivica-anchor variant
```

Estimated funnel from raw attendee list:
- Raw list: 15,000 attendees (if using full registration)
- After ICP filter: ~3,000-5,000 (excludes hospital, pharma, vendors)
- After enrichment: ~2,500-4,000 with reachable contacts
- After language split: ~95% English / ~5% Russian (rough — Andrew refines)
- After current-LIMS split: ~5-10% identified as on a known competitor

---

## Phase 1 — Pre-conference sequence (T-6 to T-1 weeks)

**Goal**: book on-floor meetings BEFORE the conference.

### English sequence (Chris) — main flow

Cadence is faster than evergreen because the deadline is concrete. Spacing reflects ADLM-specific urgency.

**Email 1 (T-6 weeks, around June 15)**

```
Subject: catching up at ADLM in Anaheim?
Hook: "Saw you registered for ADLM 2026."
Body:
  - Acure Reference Lab credibility (1 sentence)
  - Persona-specific pain (CEO: TCO, Lab Director: workflow, Medical Director: audit)
  - "Vivica team will be on the floor July 26-30"
  - {{boothNumber if applicable}} or "happy to grab coffee at the show"
CTA: "Want to grab 20 min Tuesday or Wednesday at the show?"
```

**Email 2 (T-4 weeks, around July 1)**

```
Subject: 20 min at ADLM — slots filling
Hook: continuation, no apology
Body:
  - Specific times Chris has open (3 explicit slot options)
  - One Acure detail relevant to their lab type
CTA: pick a slot via reply
```

**Email 3 (T-2 weeks, around July 14)**

```
Subject: ADLM next week — still room?
Hook: urgency
Body:
  - Short — they're swamped right before conference
  - "10-min coffee at booth #XXXX?" (lower friction)
CTA: pick a 10-min window
```

**Email 4 (T-3 days, around July 23)**

```
Subject: see you at ADLM?
Hook: confirmation
Body:
  - 2 sentences only
  - "Stop by booth #XXXX anytime — I'll keep an open slot for {{firstName}}"
CTA: reply to confirm or just show up
```

### Russian sequence (Andrew) — parallel flow

For russian-speaking attendees identified during Step 4 of audience pipeline. Andrew owns copy. Cadence same as English (T-6, T-4, T-2, T-3d) but with longer body and Andrew's voice.

Key differences:
- Subject in Russian
- Invitro reference allowed (and useful — "стек как у Invitro")
- Andrew's personal availability at conference, not generic "Vivica team"
- $100 gift card interview NOT used pre-conference (use it post-conference for non-bookers)

### Competitor-anchor variants

For attendees where `lims-detector` identified current LIMS:

- **LabWare attendees**: Email 1 leads with LabWare pain quote from corpus + ADLM hook ("on the floor, happy to walk through how Acure migrated")
- **Clinisys attendees**: same pattern with Clinisys pain
- **lims.net (JTO)**: same with lims.net pain — but check russian-segment overlap first

Reuses copy patterns from `outreach-plan-vivica-using-labware.md` Sequences, with ADLM-specific CTAs replacing generic ones.

---

## Phase 2 — Onsite (July 26-30)

**Goal**: real-time follow-up, same-day responses, capture booth contacts.

### Operating rhythm (same as playbook)

- Morning (7-9am Pacific): yesterday's booth contacts → "thanks" emails sent within 12 hours
- Daytime (booth hours): face-to-face, business-card collection
- Evening (8-10pm Pacific): triage, queue next-day follow-ups, post on LinkedIn

### Onsite email pattern (within 12 hours of meeting)

```
Subject: great talking at ADLM today
Hook: 1-2 specific things from conversation (lab name, pain mentioned)
Body:
  - 3 sentences max
  - Send the specific resource promised on the floor
CTA: "Want a 30-min call after you're back?" (specific week)
```

This is not gtm-mcp-automated. Chris/Andrew handle these manually with SmartLead-assist for delivery, but copy is per-conversation. Keep templates handy:

- Generic "thanks for stopping by" template
- Acure-detail-share template
- TCO-model-share template
- Audit-trail-export-share template (for Medical Directors specifically)

Templates live in this repo under `tracking/adlm-2026/onsite-templates.md` (created during conference week).

### Onsite metrics

Different from cold outreach. Track:
- Total booth conversations
- Business cards collected
- Same-day emails sent
- Pre-conference meetings booked vs actually attended (no-show rate)
- Calendar bookings made on the spot

These go into `tracking/adlm-2026/daily-metrics.md` (created during conference week).

---

## Phase 3 — Post-conference (July 31 — August 21)

**Goal**: convert connections into pipeline.

Three weeks of structured follow-up. Cadence relaxes back toward evergreen pacing.

### Week 1 (July 31 — August 6) — primary follow-up

Two sub-flows:
1. **Booth contacts who haven't replied** to onsite "thanks" email
2. **Pre-conference contacts who didn't book a meeting**

```
Subject: follow-up from ADLM
Hook: anchor the conversation (or admit "wish we'd had time to talk at ADLM")
Body:
  - The conference theme that's relevant to them
  - Vivica pain-fit angle (varies by what we know)
  - Specific, not generic
CTA: "Want a 30-min walk-through next week?"
```

### Week 2 (August 7-13) — LinkedIn-connection follow-up

For people Chris/Andrew met but didn't get business cards from — connected on LinkedIn.

```
Subject: since we connected at ADLM
Hook: reference the connection moment
Body:
  - Persona-specific
  - Acure case study link if appropriate
CTA: "10-min call?"
```

### Week 3 (August 14-21) — final ADLM-themed touch

```
Subject: before ADLM context fades
Hook: explicit "last ADLM-themed email"
Body:
  - Recap any specific request from the conversation
  - Standalone value (Acure published study link, sample audit-trail export, etc.)
CTA: "If anything changes, here's how to reach me"
```

### After Week 3

Drop ADLM framing entirely. Roll prospects back into evergreen sequences by their segment:
- LabWare-detected → `outreach-plan-vivica-using-labware.md`
- Russian-speaking → `outreach-plan-vivica-russian-nj.md`
- Recently-CLIA-certified → `outreach-plan-vivica-clia-fresh.md`
- All others → mark as "no current campaign" until next conference or trigger

---

## KPIs across the three phases

| Phase | Metric | Target |
|---|---|---|
| Pre-conference | Pre-booked meetings as % of pre-conference contacts | >5% |
| Pre-conference | Email reply rate | >3% (higher than evergreen — concrete event drives engagement) |
| Onsite | Booth conversations / day | TBD (depends on booth presence) |
| Onsite | Same-day follow-up sent rate | >90% within 12h |
| Onsite | Pre-booked meeting attendance | >70% |
| Post-conference | Reply rate Week 1 | >5% (warm context) |
| Post-conference | Pipeline-stage conversion (lead → SQL) | >15% (significantly higher than cold) |
| Total | ADLM-attributed booked meetings | TBD per Vivica capacity |
| Total | ADLM-attributed pipeline value | TBD per Vivica deal-size assumptions |

---

## Hypothesis testing

Add to `tracking/hypotheses.csv`:

| Hypothesis | How we measure |
|---|---|
| H13: ADLM pre-conference sequence outperforms evergreen on same audience | Compare reply rate of attendees-in-pre-sequence vs same labs not in pre-sequence |
| H14: Booth-conversation follow-up converts at >15% to pipeline | Track booth contacts → SQL rate |
| H15: Competitor-anchor variant of pre-sequence outperforms generic | A/B on attendees with detected current LIMS |
| H16: Onsite same-day email beats next-day | Tag emails with delay; compare reply rates |

---

## Capacity constraints

Onsite phase has hard human limits. Plan accordingly:

- Chris on-floor: ~10-15 meaningful conversations/day × 5 days = 50-75 booth contacts
- Andrew on-floor: ~5-10 russian-speaking conversations/day × 5 days = 25-50
- Pre-booked meetings: ~12-15 max per person per day (20-min slots, 8-hour day)

If pre-conference outreach books >75 meetings for Chris alone, we have a capacity problem. Manage by:
- Spreading slots across pre-show / show / post-show calls
- Adding Evgenia as third meeting-runner
- Prioritizing Reference Labs (highest deal value) when capacity binds

---

## Pre-launch checklist (this plan only)

- [ ] ADLM 2026 attendee list acquired (option a/b/c/d decision made and executed)
- [ ] List filtered against Vivica ICP (hospital, pharma, vendor exclusions applied)
- [ ] Audience split: English (Chris) vs Russian (Andrew) confirmed
- [ ] `lims-detector` run on attendee labs to identify competitor-anchor cohort
- [ ] Vivica booth status confirmed (booth # OR "no booth, attending" decision)
- [ ] Chris's calendar confirmed for July 26-30 with bookable slots
- [ ] Andrew's calendar confirmed for July 26-30
- [ ] Calendly (or equivalent) link configured with team round-robin
- [ ] Pre-conference Email 1-4 copy approved by Chris (English) and Andrew (Russian)
- [ ] Onsite template library written (`tracking/adlm-2026/onsite-templates.md`)
- [ ] Post-conference Week 1-3 sequence approved
- [ ] LinkedIn DM templates ready for GetSales
- [ ] Reply-handling cadence confirmed: <4h during conference, <24h post-conference

When checked, run `/launch outreach-plan-vivica-adlm-2026.md` for the pre-conference sub-campaign first. Onsite and post-conference run as time-bound activations.

---

## Cross-references

- ADLM playbook (operational rules): `../reference/playbooks/adlm-conference.md`
- Three-phase migration framework: `../reference/playbooks/three-phase-migration.md`
- Russian segment playbook: `../reference/playbooks/russian-segment.md`
- All three persona files: `../reference/icp/persona-*.md`
- All three battle cards (LabWare, Clinisys, lims.net) for competitor variants: `../reference/battle-cards/`
- Acure case study: `../reference/case-studies/acure-reference-lab-nj.md`
- Detection skill: `../extensions/.claude/skills/lims-detector/SKILL.md`
- Pain extractor skill: `../extensions/.claude/skills/lims-pain-extractor/SKILL.md`
- Glossary: `../glossary.md` → "ADLM 2026", "Pre-conference outreach", "Onsite outreach", "Post-conference follow-up"
