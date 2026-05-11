# Playbook — Russian-speaking segment

How we handle russian-speaking lab owners differently from the English-language US-clinical mainstream. **The cost of getting this wrong is high** — both because the segment is sensitive (HIPAA / data-security panic if mishandled) and because Andrew personally owns it.

> **Source**: 2026-Q2 kick-off call, Andrew's notes; Petr's Telegram chat about lims.net/JTO overlap.

## Why this segment is separate

The russian-speaking lab-owner segment in the US (concentrated in NJ, NY, PA per Andrew) operates with a different cultural and language stack than the broader US clinical market. Three things matter:

1. **Trust dynamics**: Russian-speaking owners often prefer Russian-language outreach from a Russian-speaking contact. A perfectly written English email from "John from Vivica" doesn't land the same as a casual Russian message from Andrew.
2. **Reference relevance**: the **Invitro case study** (2,000 locations, 1M tests/day) is an enormous credibility anchor for russian-speaking owners — they know Invitro firsthand. **For US-mainstream labs, the same reference triggers HIPAA / data-security concern** about Russian origins.
3. **Decision speed**: smaller russian-speaking POL/PSC labs often have the owner directly making the call. Sales cycles can be much shorter when Andrew is on the call.

## Who runs this segment

**Andrew** (Vivica) leads. All russian-speaking outreach goes through him.

- Russian-language sequences: Andrew drafts/approves
- LinkedIn DMs in Russian: Andrew sends from his profile
- 30-min interviews: Andrew runs them, offers $100 Amazon gift cards as incentive (per kick-off call)
- Final attribution of "is this lab actually russian-speaking-owned": Andrew confirms

**Yana role**: identify *candidates* via the `clia-source` skill output, hand the list to Andrew. **Don't outreach until Andrew confirms.**

**Chris role**: stays out of this segment. English LinkedIn for the US-mainstream segment.

## How candidates are identified

The `clia-source` skill produces `russian_candidates_nj.csv` per its filter logic:

```
Candidates are ICP-qualified labs (active, Compliance/Accreditation, non-hospital,
recently-certified, has phone) that ALSO match:
  - State in {NJ, NY, PA}
  - Name contains common medical-practice patterns
    (medical, diagnostic, laboratories, associates, family health, wellness)
```

This is **deliberately noisy** — it casts a wide net. Q1 2026 file produced 190 candidates.

**This is not a final answer.** It's a starting list for Andrew. He cross-references against:
- His existing relationships (Russian-speaking lab community in NJ is fairly tight)
- Owner names visible in CMS data (the lab director name field, if populated)
- Lab websites (Russian-language site copy, Russian-speaking staff bios)
- Personal network signals

**Final classification = Andrew's call. Period.**

## The Invitro reference: the single most important rule

There is exactly one rule about the Invitro case study, and it is **absolute**:

| Audience | Use Invitro? | How |
|---|---|---|
| Russian-speaking owner (Andrew confirmed) | ✅ Yes, fully | Name it: "Invitro, 2000 locations, 1M tests/day, runs on stack we built." Builds instant credibility. |
| US-mainstream lab | ✅ Anonymized only | "A large international reference laboratory with thousands of locations and ~1M tests daily" |
| US-mainstream Medical Director | ⚠️ Avoid entirely | Stick to Acure. Medical Directors are most sensitive — even anonymized, the volume hint can trigger curiosity → discovery → HIPAA panic. |

**The reason**: Russian-origin tech in healthcare context triggers data-security and geopolitical concerns from US-mainstream buyers, especially anyone in a compliance-sensitive role. We won't fight that battle in cold outreach.

## Russian-language sequence patterns

These differ from the English-language playbook in tone, length, and reference choice. Andrew is the source of truth for actual copy; below is the pattern guide.

### Tone
- Less formal than US-business-English standard
- Direct ("вот цифры", "вот как это работает") rather than indirect
- Comfortable with longer paragraphs than US best practice (Russian readers expect more context per email)
- Personal — Andrew's own voice, not "Vivica team"

### Subject lines
- Short, specific
- Often a question rather than a statement
- Common patterns:
  - "Ваша CLIA — мы можем помочь с LIMS"
  - "Похожий случай с лабораторией в [city]"
  - "Invitro делает 1М тестов в день — на похожей логике"

### Body structure
- Open with personal connection or specific signal (recently certified, NJ presence, owner's name if visible)
- Mention Invitro early when russian-speaking is confirmed
- Three-phase migration framework still applies (translated into Russian) — same logic, different language
- CTA: "10 минут поговорить?" (lower friction than English-style "worth a TCO model")

### What we don't do in Russian sequences
- Don't translate the English sequence verbatim — it reads stilted
- Don't use marketing-speak ("трансформируем", "революционизируем") — even more painful in Russian than English
- Don't oversell — Russian-speaking owners are skeptical of pitch volume

## What gets shared with Andrew

For each candidate Andrew is reviewing, the data package contains:

```
- Name
- Address (city, state)
- Phone
- CLIA number
- Certification date
- Certificate type (Compliance / Accreditation)
- Lab type (POL / PSC / Reference)
- Test volume (if available)
- Detected current LIMS (if `lims-detector` ran)
- Pattern matches that flagged this as a candidate
```

Andrew adds: russian-speaking? confirmed-or-rejected, owner contact (if known), engagement preference (LinkedIn / email / phone / introduction-via-mutual).

## Lifecycle of a russian-segment lead

```
1. clia-source skill → russian_candidates_nj.csv (190 candidates per Q1 2026 file)
2. Yana → hand list to Andrew
3. Andrew reviews, confirms or rejects each
4. Confirmed russian-speaking → Andrew runs Russian sequence
5. Confirmed NOT russian-speaking → returns to general US-mainstream pipeline
6. Andrew offers $100 Amazon gift card for 30-min interview to engaged candidates
7. Interview output → fills in our knowledge of "samopis" labs, real pains, etc.
```

## Self-hosted / "samopis" labs

Per Andrew's note, 3-5 known russian-speaking labs run a custom-built LIMS that a contractor maintains for ~$800/month. These are special.

**Value prop is different**: "professional cloud LIMS without the maintenance burden, without depending on one developer who could leave any day."

**Hooks that work**:
- "Что если ваш разработчик уйдёт?"
- "У нас 24/7 поддержка вместо одного человека"
- "Profession LIMS со всеми сертификациями за похожий месячный бюджет"

**What doesn't work**: any pitch implying their current setup is amateur. It's not — it's pragmatic. We respect the choice and offer an alternative.

## Andrew's $100 gift card interviews

Andrew offers $100 Amazon gift cards for 30-min interviews. This is **not standard sales practice** — it's a research investment, not a transaction.

**Goals of the interviews**:
- Understand the russian-speaking lab market that's invisible to G2/Capterra
- Identify which competitors are actually used (lims.net/JTO has overlap, but other Russia-adjacent products may exist)
- Build relationships even with non-buyers — the community is small, referrals matter
- Capture pain language we can't get from English-language reviews

**Interview output goes into**:
- `tracking/russian-segment-interviews.md` (created later when first interviews happen)
- `lims-pain-extractor` corpus (manual additions from interview material)
- `russian-segment` overlap notes for `lims.net` competitor file

## Escalation paths

| Situation | Who decides |
|---|---|
| Lab borderline russian-speaking — go or no-go? | Andrew |
| Someone says "are you really Russian?" in a reply | Andrew |
| Russian-speaking lab asks about HIPAA / data residency | Andrew + Chris together |
| Translation question on a sensitive sentence | Andrew |
| "Should we run this US-mainstream candidate through Russian sequence?" | Andrew. Default answer is no. |

## What kills this segment

- ❌ Sending Russian-language email from someone other than Andrew
- ❌ Mentioning Invitro by name to a US-mainstream lab
- ❌ Treating Russian-speaking owners as a "growth hack" / lower-tier segment — they're a high-trust niche, treat accordingly
- ❌ Cross-pollinating: using English-sequence verbatim translated; using US case studies in Russian sequences without Andrew's review
- ❌ Bypassing Andrew's confirmation step on a candidate

## Cross-references

- Skill: `../../extensions/.claude/skills/clia-source/SKILL.md` — produces the candidates list
- Skill: `../../extensions/.claude/skills/lims-detector/SKILL.md` — overlap with lims.net detection
- Competitor: `../competitors/lims-net.md` — frequent overlap with russian-speaking segment
- Plan: `../../plans/outreach-plan-vivica-russian-nj.md` — full campaign plan for this segment (Response 4)
- Glossary: `../../glossary.md` → "Russian-speaking segment", "Самопис", "Andrew"
