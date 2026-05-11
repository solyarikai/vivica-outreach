# Final Checklist — Vivica Outreach Project Launch

What's complete in this repo, what's still needed from each stakeholder, and how to actually run the first campaign. Read this top-to-bottom before doing anything operational.

> **Last updated**: 10 May 2026 (project start). **Update this file as items are checked.**

---

## What's done in this repo

### Skills (all 3 production-ready)

- ✅ `extensions/.claude/skills/clia-source/` — filters CMS POS file → 9,193 ICP labs in 5 buckets (POL/PSC/REFERENCE/UNSUITABLE/OTHER) + 190 russian candidates. Live-tested on Q1 2026 file.
- ✅ `extensions/.claude/skills/lims-pain-extractor/` — competitor pain corpus skeleton; ready to run against G2/Capterra/SourceForge/ITQlick/TrustRadius for all 8 vendors.
- ✅ `extensions/.claude/skills/lims-detector/` — iframe + JS + DNS + jobs-posting fingerprinting; ready to enrich any lab domain with `current_lims` field.

Each skill has:
- `SKILL.md` (English, Anthropic standard)
- `README.ru.md` (Russian companion for Yana)
- Working Python scripts
- Reference data (vendor URLs, classification codes)

### Reference / domain knowledge (22 files)

- ✅ 3 persona files with verbatim ICP-table content (`reference/icp/`)
- ✅ 8 competitor profile stubs (`reference/competitors/`) — to be enriched by `lims-pain-extractor` first run
- ✅ 9 battle cards: 3 priority competitors × 3 personas (`reference/battle-cards/`)
- ✅ 3 playbooks: three-phase migration, russian-segment, ADLM (`reference/playbooks/`)
- ✅ Vivica intel file with hard rules ("never claim FDA, never invent customer counts...") (`reference/company/`)
- ✅ Acure case study with 4 story scaffolds + open questions for Chris (`reference/case-studies/`)

### Outreach plans (4 plans, ~1,400 lines total)

- ✅ `plans/outreach-plan-vivica-clia-fresh.md` (404 lines) — main plan, 3 sequences, 7,900-lab universe
- ✅ `plans/outreach-plan-vivica-russian-nj.md` — Andrew's segment, separate execution
- ✅ `plans/outreach-plan-vivica-using-labware.md` — competitor-conquest, depends on detector + pain corpus
- ✅ `plans/outreach-plan-vivica-adlm-2026.md` — time-boxed conference campaign, July 26-30

### Documentation

- ✅ `README.md` (English entry point)
- ✅ `README.ru.md` (Russian entry point for Yana)
- ✅ `glossary.md` + `glossary.ru.md` (513 lines each, every term defined, agent autonomy rules)
- ✅ `.gitignore` (Python, Obsidian, Anthropic-aware)

### Source data (delivered)

- ✅ CMS POS file Q1 2026 → 9,193 ICP labs filtered, segmented, ready in CSV/JSON

**Total**: 46 files, ~9,000 lines of code + content.

---

## What's NOT done (intentionally)

These are explicitly out of scope for the initial scaffold and require human decisions before they're filled in:

### Open questions for Chris (Vivica)

These are tracked in `reference/case-studies/acure-reference-lab-nj.md` and `reference/company/vivica-intel.md`:

1. Acure go-live date and time-from-kickoff (used for "live in X weeks" claims)
2. Joint publication: title, journal, KOL name, link
3. Acure quantitative outcomes (TAT delta, audit-prep time, error rate, vendor consolidation)
4. Approved direct quotes from Acure CEO / Lab Director / Medical Director
5. SOC 2 Type II certification active date (referenced in Medical Director battle cards)
6. Billing integrations pre-built (referenced in vivica-intel.md)
7. Patient portal availability (referenced in vivica-intel.md)
8. Vivica's preferred email for outbound (chris@vivica.us assumed)
9. ADLM 2026 booth status: yes/no, booth number if yes
10. Vivica team availability July 26-30 with calendar

### Open questions for Andrew (Vivica)

1. Email address for Russian-segment SmartLead account
2. LinkedIn profile for GetSales Russian flow
3. Russian-language Email 1-4 copy (final wording — patterns are documented, voice is Andrew's)
4. $100 Amazon gift card delivery process with Vivica finance
5. Initial review of `russian_candidates_nj.csv` (190 candidates → confirmed russian-speaking subset, expected 60-100)
6. Interview question template for $100 sessions

### Open decisions for the team (Sally + Vivica)

1. **Git remote**: GitHub private personal / GitHub org / GitLab / local-only-for-now
2. **Repo access roster**: who gets push access, who gets PR review only
3. **Apollo budget cap**: how many people-enrichment calls authorized for first 30 days
4. **SmartLead account**: existing Vivica account or new one for this project
5. **GetSales account**: existing or new
6. **Claude.ai / Claude Code subscription**: who runs `/launch`, on what machine
7. **ADLM attendee list source**: AACC paid / public scrape / LinkedIn signal mining / hybrid
8. **Pilot segment**: which sequence runs first — POL (largest), Reference (highest value), or russian-NJ (Andrew leads)?

---

## How to launch, end to end

These are the steps in order. Marked who does what.

### Step 0 — Distribute the repo to the team (day 0)

```bash
# Pick a git host based on team decision
cd ~/code  # or wherever
unzip ~/Downloads/vivica-outreach-skeleton.zip
cd vivica-outreach
git init
git add .
git commit -m "initial: skills, plans, reference, glossary"
git remote add origin <decided-remote>
git push -u origin main
```

Send the repo URL to Yana. Send the `glossary.ru.md` link to Andrew (he won't read English-only docs).

### Step 1 — Stakeholder kick-off (1 hour, week 1)

A single 60-minute call with Chris, Andrew, Petr, Yana. Agenda:

1. (10 min) Walk through the repo structure (`README.md` → `glossary.md` → one example: `reference/icp/persona-ceo-owner.md`)
2. (15 min) Chris closes Acure open questions (items 1-7 above) — type into `reference/case-studies/acure-reference-lab-nj.md` live
3. (10 min) Andrew commits to russian-segment review of 190 candidates by end of week 1
4. (10 min) Petr / Yana decide on pilot segment (recommendation: start with **POL** — largest universe, lowest-stakes errors)
5. (10 min) Confirm tooling — Apollo, SmartLead, GetSales, Claude.ai
6. (5 min) Schedule weekly sync (30 min, Wednesdays — long enough to review metrics + decide actions)

### Step 2 — Environment setup (Yana, week 1)


```bash
# 1. Place skills where Claude Code finds them
ln -s $(pwd)/extensions/.claude/skills/clia-source ~/.claude/skills/clia-source
ln -s $(pwd)/extensions/.claude/skills/lims-pain-extractor ~/.claude/skills/lims-pain-extractor
ln -s $(pwd)/extensions/.claude/skills/lims-detector ~/.claude/skills/lims-detector

# 2. Place POS file
cp /path/to/POS_File_CLIA_Q1_2026.csv input-data/

# 3. Run clia-source filter
python3 extensions/.claude/skills/clia-source/scripts/filter_pos_file.py \
  --input input-data/POS_File_CLIA_Q1_2026.csv \
  --since 2025-01-01 \
  --output ~/.gtm-mcp/projects/vivica/sources/

# 4. Set up gtm-mcp project shell
cat > ~/.gtm-mcp/projects/vivica/project.yaml <<EOF
slug: vivica
name: Vivica Outreach
plans_dir: ~/code/vivica-outreach/plans
reference_dir: ~/code/vivica-outreach/reference
extensions_dir: ~/code/vivica-outreach/extensions
EOF

# 5. .env with API keys (NOT committed)
cat > .env <<EOF
APOLLO_API_KEY=...
SMARTLEAD_API_KEY=...
GETSALES_API_KEY=...
GETSALES_USER_TOKEN=...
ANTHROPIC_API_KEY=...
EOF
chmod 600 .env
```

### Step 3 — Run lims-pain-extractor on competitors (Yana, week 1-2)

```bash
# Inside Claude Code, in the repo root
claude
# Then in Claude:
> Run the lims-pain-extractor skill on all 8 vendors using the URL list at
  extensions/.claude/skills/lims-pain-extractor/references/vendor_review_urls.yaml.
  Output to ~/.gtm-mcp/projects/vivica/competitor_pains/ and mirror to
  reference/competitors/.
```

Claude (in Claude Code) will fetch G2/Capterra/SourceForge pages, classify reviews into 8 themes, score them, pick top 3 per vendor, and write `corpus.json` plus per-vendor markdown.

After this runs, `reference/competitors/labware.md` (and the other 7) get filled with real ≤15-word quotes replacing the scaffold placeholders.

**This is required before `outreach-plan-vivica-using-labware.md` can launch.**

### Step 4 — Pilot kick-off: CLIA-fresh, POL bucket (Yana + Chris, week 2)

```bash
# Inside Claude Code, in the repo
claude
> /launch plans/outreach-plan-vivica-clia-fresh.md
```

What gtm-mcp does:
1. Reads `outreach-plan-vivica-clia-fresh.md`
2. Initializes `~/.gtm-mcp/projects/vivica/` if not present
3. Reads `~/.gtm-mcp/projects/vivica/sources/clia_Q1_2026_segmented/bucket_POL.csv`
4. Asks the operator to confirm Apollo enrichment for the first batch (per cost-gating rule)
5. Enriches contacts via Apollo
6. Asks the operator to confirm SmartLead campaign creation
7. Creates the campaign with sequences from the plan
8. Sends test email to internal team
9. Awaits final go-ahead before live sending

Each `?` confirmation is a deliberate stop. Don't skip these — they're the safety rails.

### Step 5 — Monitor pilot (Yana, week 2-3)

Daily checks (Yana):
- Open SmartLead dashboard
- Check open / reply / bounce trend
- Triage replies via gtm-mcp `reply-classification` skill
- Hand off positive replies to Chris with full context

Weekly check (Petr + Yana):
- 30-min sync, Wednesdays
- Review metrics vs. KPI table from CLIA-fresh plan
- Decide: scale to next batch / iterate copy / pivot

### Step 6 — Andrew launches russian-NJ campaign (Andrew + Yana, parallel to step 5)


When Andrew has confirmed his subset of the 190 candidates and committed Russian-language copy:

```bash
> /launch plans/outreach-plan-vivica-russian-nj.md
```

Runs in parallel to the main pilot. Smaller volume, Andrew personal involvement.

### Step 7 — When Step 5 metrics are healthy, scale (Yana, week 4)

Scale to next batch (POL bucket continued, or move to PSC/REFERENCE buckets per pilot signal).

### Step 8 — ADLM pre-conference activates (Chris + Yana, mid-June)

```bash
> /launch plans/outreach-plan-vivica-adlm-2026.md
```

Once the attendee list is acquired and filtered.

### Step 9 — LabWare conquest plan activates (Yana, week 4-5)

When `lims-pain-extractor` corpus exists AND `lims-detector` has run on enough leads to surface a meaningful LabWare cohort:

```bash
> /launch plans/outreach-plan-vivica-using-labware.md
```

---

## Who does what — RACI summary

| Activity | Responsible | Approves | Consulted | Informed |
|---|---|---|---|---|
| Repo maintenance | Yana | Petr | — | All |
| Plan copy approval — English | Chris | Chris | Yana | All |
| Plan copy approval — Russian | Andrew | Andrew | Yana | All |
| Apollo enrichment runs | Yana | Petr | — | Chris |
| SmartLead campaign launch | Yana | Chris (English) / Andrew (Russian) | — | All |
| Reply triage | Yana | Chris (English) / Andrew (Russian) | — | Petr |
| Booth meeting calls | Chris (English) / Andrew (Russian) | — | — | All |
| Hypothesis tracking updates | Yana | Petr | — | All |
| KPI review at weekly sync | Yana | Petr | All | All |
| Decision: scale / iterate / pause | Petr | Chris | Yana | Andrew |

---

## What Yana owns day-to-day

Per Petr's $500/month scope plan, Yana operates the day-to-day pipeline.

**Yana does alone**:
- Run `clia-source` filter against new POS file (quarterly CMS update)
- Re-segment by different `--since` date for different campaigns
- Hand-off russian-segment candidates to Andrew
- Trigger Apollo enrichment via Claude Code (subject to cost-gating confirmation)
- Launch SmartLead/GetSales campaigns from approved plans
- Do reply triage daily
- Update `tracking/hypotheses.csv` with run results
- Update `tracking/decisions-log.md` with weekly decisions
- Review competitor pain corpus when `lims-pain-extractor` re-runs
- Maintain skills, add new ones, modify existing
- Adjust plan structure when needed
- Add new competitors to the tracked-8

**Yana needs Chris/Andrew for**:
- Any new email copy approval
- Any deviation from approved sequences
- Reply handling on positive replies (quick handoff)
- Booth meeting scheduling

---

## Hard rules (everyone follows, no exceptions)

These come from gtm-mcp and our own copyright/safety practices:

1. **Cost gating**: never spend Apollo / SmartLead / GetSales credits without explicit confirmation. This applies to Yana, Petr, AND Claude Code agents.

2. **Copyright limit**: no quote exceeds 15 words. No source provides more than one quote in a single email. Brevity ≠ exception.

3. **Russian-segment isolation**:
   - Invitro by name → only to confirmed russian-speaking owners
   - Invitro anonymized → other contexts (rarely needed)
   - Andrew confirms russian-speaking attribution; never Yana, never Claude alone

4. **Hospital exclusion**: hospital labs (`GNRL_FAC_TYPE_CD = 14` or `HOSP_LAB_EXCPTN_SW = Y`) never receive Vivica outreach. Epic/Cerner lock-in is real, the conversation is unwinnable.

5. **No invented facts**: customer count, FDA clearance, specific TAT improvements — none are claimed without Chris's confirmation. Acure metrics specifically need Chris approval before being quoted.

6. **No automation of reply sending**: gtm-mcp's `reply-classification` triages, but humans (Chris/Andrew/Yana) write the replies. Cold outreach automated; reply conversations are not.

7. **Glossary as truth**: when terminology disputes arise, `glossary.md` wins. Update the glossary FIRST, then propagate to skills and plans.

---

## Repo navigation cheat-sheet

If you're new to the repo:

| You want to | Read |
|---|---|
| Understand the project at all | `README.md` (English) or `README.ru.md` (Russian) |
| Look up a term | `glossary.md` or `glossary.ru.md` |
| Understand a persona | `reference/icp/persona-{ceo-owner,lab-director,medical-director}.md` |
| See competitor positioning | `reference/competitors/<vendor>.md` |
| Get talking points for an outreach call | `reference/battle-cards/<vendor>_x_<persona>.md` |
| Understand the migration story | `reference/playbooks/three-phase-migration.md` |
| Run a campaign | `plans/outreach-plan-vivica-*.md` (pick the right one) |
| Modify lead extraction | `extensions/.claude/skills/clia-source/SKILL.md` |
| Refresh competitor pains | `extensions/.claude/skills/lims-pain-extractor/SKILL.md` |
| Detect a lab's current LIMS | `extensions/.claude/skills/lims-detector/SKILL.md` |
| Know what an agent can/can't do alone | `glossary.md` → "Agent autonomy" section |

---

## Definition of "project successfully launched"

The pilot is live when ALL of these are true:

- [ ] Step 0-4 above executed
- [ ] First 50 emails delivered via SmartLead, ≥40% open rate observed
- [ ] First reply received and triaged within 4 business hours
- [ ] First positive reply handed to Chris with full context
- [ ] First booked meeting scheduled (target: within 2 weeks of launch)
- [ ] `tracking/hypotheses.csv` populated with H1-H5 baselines
- [ ] First weekly sync held with all stakeholders

When all 7 are checked, project status moves from "scaffolding" to "operational." Yana signals "live" in the team channel; the project transitions to day-to-day operation with weekly sync support.

---

## Further work (not in this initial scaffold)

These are recognized gaps, deferred for later iteration:

- **Q2 2026 POS file** — when CMS publishes Q2 (typically July), re-run `clia-source` to add ~3 months of fresher CLIA certifications
- **Additional conquest plans** for Clinisys, lims.net, QBench (clone `outreach-plan-vivica-using-labware.md` template)
- **Post-ADLM evergreen flow** — reactivating booth contacts as ongoing pipeline once conference window closes
- **Dashboard integration** — pulling gtm-mcp run metrics into a simple dashboard for Petr's weekly review
- **Russian-segment interview corpus** — accumulating notes from Andrew's $100 sessions into structured pain insight
- **Cross-segment analytics** — which segments / sequences / competitor angles produce the highest ROI

These are scoped for later. The current scaffold is sufficient to launch.

---

## Cross-references (from this checklist)

- All plans: `plans/`
- All reference: `reference/`
- All skills: `extensions/.claude/skills/`
- Glossary: `glossary.md` / `glossary.ru.md`
- Top-level: `README.md` / `README.ru.md`
