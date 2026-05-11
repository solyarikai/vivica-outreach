# Outreach Plan — Vivica × Russian-Speaking Lab Owners (NJ/NY/PA)

> Personas: [[persona-ceo-owner]] · [[persona-lab-director]]
> Playbook: [[russian-segment]]

**Status**: parallel plan to `outreach-plan-vivica-clia-fresh.md`. Runs simultaneously, separate execution.
**Owner**: Andrew (Vivica) leads execution; Yana operates the pipeline and hands off candidate lists.
**Source**: this plan handles the 190 candidates produced by `clia-source` skill into `russian_candidates_nj.csv`.

> **Critical**: this plan is intentionally **separate** from the main CLIA-fresh plan. The audience, language, references, and decision authority are all different. Do not merge these flows.

---

## Why this segment is separate

Per `reference/playbooks/russian-segment.md`, the russian-speaking lab-owner segment in the US (concentrated in NJ/NY/PA) requires:

- Russian-language outreach from a Russian-speaking sender (Andrew)
- Different reference choices (Invitro by name → ✅, vs anonymized for everyone else)
- Different cultural register (less formal, longer paragraphs, more direct)
- Andrew's personal confirmation that a candidate is actually russian-speaking before any outreach goes out

Running this through the same SmartLead campaign as English-language sequences would produce real damage:
- Wrong language → wasted outreach
- Wrong references → trust damage if Invitro mentioned to non-russian-speaking US-mainstream
- Wrong sender → reduced reply rate
- Andrew loses control of his segment

So we run a **second SmartLead campaign** (or GetSales LinkedIn flow) with Andrew as sender, Russian-language sequences, and a curated subset of the candidate pool.

---

## Project setup

This plan does NOT use `/launch` mode 1 — it runs inside the same gtm-mcp project (`vivica`) as the CLIA-fresh plan, but creates a **separate campaign**:

```
~/.gtm-mcp/projects/vivica/
  campaigns/
    clia-fresh-pol/         # from main plan
    clia-fresh-psc/
    clia-fresh-reference/
    russian-nj/             # ← THIS plan creates this
```

Use `/launch` mode 2 (new campaign in existing project) when this plan is fed.

### Campaign metadata

```yaml
campaign_slug: russian-nj
parent_project: vivica
language: ru
sender:
  name: Andrew
  email: andrew@vivica.us  # confirm with Andrew
  linkedin: andrew-vivica   # confirm
audience_source: ~/.gtm-mcp/projects/vivica/sources/clia_Q1_2026_segmented/russian_candidates_nj.csv
audience_size: 190  # before Andrew's manual confirmation step
```

---

## Audience pipeline

```
1. clia-source skill produces russian_candidates_nj.csv (190 candidates)
   ↓
2. Yana hands list to Andrew with the standard data package
   (name, address, phone, CLIA #, cert date, lab type, GNRL_FAC_TYPE_CD,
    test volume, detected current LIMS if available)
   ↓
3. Andrew reviews candidate-by-candidate, marks each:
   - confirmed russian-speaking (proceed to step 4)
   - not russian-speaking (return to main CLIA-fresh plan)
   - unknown / needs investigation (hold)
   ↓
4. Confirmed candidates → Apollo people enrichment for Andrew's contact targets
   - Andrew specifies which person to enrich per lab
     (often the owner directly, vs the 3-persona spread on the main plan)
   ↓
5. Russian-language sequence sent from Andrew's account
   ↓
6. Replies: Andrew handles personally, classifies engagement,
   offers $100 Amazon gift card for 30-min interview where appropriate
```

The 190 candidates is **ceiling**, not starting point. Realistic post-confirmation count: 60-100 actually russian-speaking, per Andrew's experience.

---

## Sequence pattern

Andrew owns the actual copy. Below is the **pattern**, not the wording — Andrew adjusts to his voice.

> **All copy in Russian.** Translation/transliteration here is for internal reference only.

### Email 1 — first contact

```
Subject pattern: "[city/state]-related opening" — short, specific, no clickbait
  Examples (Russian):
    "Ваша CLIA сертификация — пара мыслей"
    "Лаба в [city] — похожий случай"

Body structure:
  Open: personal greeting, owner's name if known
  Trigger: "Заметил что вы недавно получили CLIA — поздравляю"
  Quick credibility: "Я работаю с Vivica — облачная LIMS для клин-лаб в США"
  Russian-specific anchor: "Стек, который мы используем, — он же стоит за Invitro
    (2000 локаций, 1М тестов в день). Похожая логика, но под US compliance."
  Pain hint: "Большинство лаб в первый год выбирают между табличками или Enterprise
    LIMS — не то и не другое не подходит для лаб как ваша"
  CTA: "10 минут поговорить?"
```

The Invitro mention is the killer feature for this segment. Russian-speaking owners know Invitro firsthand, so the credibility leap is instant.

### Email 2 — three-phase migration (T+5 days, longer spacing than English)

Russian-language readers expect longer between-email gaps and don't react well to high-frequency follow-up. 5 days, not 4.

```
Subject: "о миграции"
Body:
  Hook: continuation, no apology for previous email
  Three-phase migration framework — translated and explained
    (mirror → proxy → decommission)
  Specific: typical timeline 4-6 weeks for POL, 8-10 weeks for Reference
  Acure mention: "У нас есть клиент — крупный референс-лаб в NJ. $100M+ оборот,
    совместная публикация с KOL. Перешли с предыдущей системы за 6 недель."
  CTA: "Если интересно посмотреть, как это будет выглядеть для [companyName] —
    напишите, скину детали"
```

### Email 3 — case study or competitor angle (T+10 days)

If Andrew knows the lab uses lims.net/JTO (very common in this segment per Petr's chat), pivot to competitor-conquest:

```
Subject: "о JTO / lims.net"
Body:
  Open: "Если ваша лаба сейчас на JTO / lims.net..."
  Specific pain pattern (US-fit gaps, support time-zone, language artifacts)
  Vivica fit: built US-clinical-native, US support hours, English-first interface
  Acure reference (anonymized at first, full if asked)
  CTA: "Готов показать, как это выглядит сравнительно"
```

If competitor unknown, use Acure-anchor sequence similar to Sequence A in main plan but in Russian.

### Email 4 — breakup with $100 gift card pivot (T+15 days)

```
Subject: "последнее сообщение"
Body:
  Acknowledgment: "Понимаю, может быть не до этого сейчас"
  Soft reset: "Готов ещё к одному совсем другому формату"
  $100 gift card offer: "30 минут вашего времени за $100 Amazon gift card —
    я хочу понять, что в LIMS-рынке для русскоязычных лаб не работает,
    чтобы сделать продукт лучше. Это не про продажу."
  CTA: "Если интересно, напишите. Если нет — не буду больше отвлекать."
```

The $100 interview offer is the **research investment** Andrew described in kick-off. It's not a sales tactic — it's relationship-building with a community.

### LinkedIn DM (alternative or follow-up to email)

Andrew often gets better engagement on LinkedIn than email for this segment. Same content, condensed:

```
3 sentences maximum:
  - Personal connection / specific signal
  - "Работаю с Vivica — стек как у Invitro, но под US compliance"
  - "Открыты на разговор?"
```

---

## What's different from the main plan

| Dimension | Main CLIA-fresh plan | This plan |
|---|---|---|
| Sender | Chris (Vivica US) via SmartLead | Andrew via SmartLead AND/OR LinkedIn |
| Language | English | Russian |
| Cadence | T+4 / T+8 / T+12 / T+15 | T+5 / T+10 / T+15 (longer gaps) |
| Invitro reference | Anonymized only | Named openly |
| Acure reference | Full strength | Used carefully, secondary to Invitro for credibility |
| Personas | 3 spread (CEO, Lab Director, Med Director) | Often just owner — smaller labs concentrate decision authority |
| Approval gate | Chris on copy | Andrew on copy AND on candidate confirmation |
| Reply handling | gtm-mcp `reply-classification` then Chris | Andrew personally, no automated triage |
| $100 gift card offer | not used | used in Email 4 as soft reset |
| Volume | ~7,900 leads | 60-100 confirmed leads |

---

## KPIs for this plan

Smaller audience, deeper engagement. Targets are **higher per-lead** than main plan:

| Metric | Target | Why higher than main plan |
|---|---|---|
| Open rate | >50% | Andrew sends from his real account, name recognition in community |
| Reply rate | >5% | Russian-speaking owners reply to Andrew personally; tight community |
| Positive reply rate | >2% | Higher trust, Invitro anchor |
| Booked-meeting rate | >1.5% | Smaller pool, but more inclined to take meetings with Andrew |
| Booked-interview rate ($100 GC) | >0.5% | Email 4 alternative path |
| Bounce rate | <2% | Andrew validates emails personally before adding |

---

## Hypothesis testing

Add to `tracking/hypotheses.csv`:

| Hypothesis | How we measure |
|---|---|
| H6: Russian-language sequence outperforms translated English | Compare reply rate vs main plan baseline (controlling for segment) |
| H7: Invitro reference (named) drives engagement | A/B test: half cohort gets Invitro mention, half gets anonymized |
| H8: $100 gift card offer in Email 4 produces interviews | Track Email-4-to-interview conversion |
| H9: lims.net/JTO conquest copy outperforms generic on this segment | A/B in Email 3: competitor-specific vs generic Acure-anchor |

---

## What we capture in interviews

Andrew's $100 interviews produce structured output that goes back into the system:

- Which competitors are actually used in this segment (beyond lims.net/JTO?)
- Real pain language in Russian (feeds Russian-language copy iteration)
- "Самопис" patterns — who's running custom-built, what does it cost them, what would make them switch
- Referral graph — who knows whom, can we get warm intros

Capture format: short markdown notes per interview in `tracking/russian-segment-interviews.md` (created on first interview).

---

## Pre-launch checklist (this plan only)

- [ ] Andrew confirmed on senior copy approval
- [ ] Andrew's SmartLead account configured (or GetSales LinkedIn)
- [ ] Russian-language Email 1 drafted and reviewed by Andrew
- [ ] Russian-language Email 2-4 drafted and reviewed
- [ ] Apollo people enrichment quota allocated for confirmed candidates only (not all 190)
- [ ] `russian_candidates_nj.csv` excluded from main CLIA-fresh plan's contact universe
- [ ] $100 Amazon gift card delivery process confirmed with Vivica finance
- [ ] Interview question template prepared for $100 sessions
- [ ] Reply-handling cadence: Andrew commits to <24h response on positive replies during business days

When checked, run `/launch outreach-plan-vivica-russian-nj.md` from the repo with Claude Code + gtm-mcp.

---

## Cross-references

- Russian segment playbook (the rules): `../reference/playbooks/russian-segment.md`
- Main CLIA-fresh plan (the parallel/larger flow): `outreach-plan-vivica-clia-fresh.md`
- lims.net competitor profile (frequent overlap): `../reference/competitors/lims-net.md`
- Three-phase migration framework (translated for Russian sequences): `../reference/playbooks/three-phase-migration.md`
- `clia-source` skill (produces candidate list): `../extensions/.claude/skills/clia-source/SKILL.md`
- Glossary: `../glossary.md` → "Russian-speaking segment", "Andrew", "Самопис"
