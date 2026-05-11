# Glossary — Vivica Outreach project

Single source of truth for every term used in this project. If a term is used in skills, plans, or reference material, it must be defined here. When something is unclear, this glossary is the first place to look.

Organized by category:
- [Product & domain](#product--domain) — what Vivica is and the clinical-lab world it lives in
- [ICP & segmentation](#icp--segmentation) — who we target
- [Competitors](#competitors) — the 8 LIMS vendors we track
- [Data sources](#data-sources) — CMS POS file, CLIA codes, etc.
- [Pipeline & tooling](#pipeline--tooling) — gtm-mcp, MCP servers, Apollo, SmartLead, GetSales
- [Skills & this repo](#skills--this-repo) — what each component does
- [Process & playbook terms](#process--playbook-terms) — three-phase migration, etc.
- [Team & people](#team--people) — who's who
- [Events & deadlines](#events--deadlines) — ADLM 2026
- [Agent autonomy](#agent-autonomy) — what an AI agent can and cannot do unilaterally

---

## Product & domain

### Vivica
The product we run cold outreach for. Cloud-based **LIMS** for clinical laboratories in the US. Website: vivica.us. One active customer at the time of project start (Acure Reference Lab, NJ, $100M+ revenue) plus one churned (lab closed; not a product issue). Has a published joint study with a KOL — usable in cold emails.

### LIMS (Laboratory Information Management System)
Software that manages lab samples, tests, results, billing, and compliance. The category Vivica competes in. **Not** to be confused with **LIS** (Lab Information System), though many tools combine both functions.

### LIS (Laboratory Information System)
Closely related to LIMS; LIS is more clinical-results-oriented while LIMS is more sample/inventory/workflow-oriented. Some vendors combine them (LigoLab, CrelioHealth).

> **Terminology trap — read carefully**: in this project's outreach context, when we talk about "the customer's current system" that we mirror/proxy/decommission, **it is almost always a LIMS**, not a LIS — because Vivica is a LIMS and we compete with LIMS vendors (LabWare, Clinisys, QBench, etc.). Earlier drafts of this project's docs incorrectly used "LIS" in migration descriptions; this has been corrected. Use "LIMS" for the system being replaced. Use "LIS" only when (1) describing a vendor that is genuinely combined LIS+LIMS like LigoLab/CrelioHealth, (2) discussing instrument-feed integration paths where LIS is a real component in the customer's stack, or (3) discussing Vivica's own product as "combined LIS+LIMS functionality."

### Clinical lab
A lab that runs tests on human specimens for diagnosis or treatment. Falls under CLIA regulation. Different from **research labs** (which are not Vivica's market).

### CLIA (Clinical Laboratory Improvement Amendments)
US federal regulation governing clinical labs. Every clinical lab must hold a CLIA certificate to operate. Administered by CMS.

### CLIA certificate types
- **Compliance** (`CRTFCT_TYPE_CD = 1`) — full inspection regime. Vivica targets this.
- **Waiver** (`= 2`) — only the simplest tests. Doesn't need a LIMS. Skip.
- **PPMP** (`= 3`) — Provider-Performed Microscopy Procedures. Niche.
- **Accreditation** (`= 4`) — accredited by CAP, AABB, etc. Vivica targets this too.
- **Registration** (`= 9`) — temporary while applying. Skip.

### CMS (Centers for Medicare & Medicaid Services)
US federal agency. Publishes the CLIA POS file quarterly — the canonical registry of all CLIA-certified labs.

### CAP (College of American Pathologists)
Accrediting body for clinical labs. CAP-accredited labs show `CRTFCT_TYPE_CD = 4`.

### HIPAA (Health Insurance Portability and Accountability Act)
US privacy/security regulation for health data. **Important for Russian-segment outreach**: emphasizing Russian origin of in-vitro case study can trigger HIPAA/data-security objections from US labs.

### HL7 / FHIR
Healthcare data exchange standards. LIMS must integrate with these to talk to hospital systems. Common pain point in competitor reviews ("brittle HL7 integration").

### EMR / EHR
Electronic Medical Record / Electronic Health Record. The hospital's clinical software. Epic and Cerner are dominant vendors — labs inside hospitals are locked into their EMR's lab module, which is why we **skip hospital labs**.

### Epic / Cerner
Dominant US EMR vendors. Epic's "Beaker" and Cerner's "PathNet" are their lab modules. If a lab is inside an Epic or Cerner hospital, switching LIMS is essentially impossible — the integration cost dominates everything. Skip these.

### KOL (Key Opinion Leader)
Recognized authority in the field. Vivica has a published study with a KOL via Acure — provides social proof for cold emails.

---

## ICP & segmentation

### ICP (Ideal Customer Profile)
The segment of the market that's most likely to buy. Vivica's ICP is captured in the Sally ICP Google Sheet and our `reference/icp/` files.

### Persona
A specific decision-maker role within the ICP. Vivica has three:

- **CEO / Owner** — small POL/PSC owner. Top objections: cost vs ROI, "we're fine".
- **Lab Director / Manager** — operational head. Top objections: training disruption, current system works.
- **Medical Director** — clinical authority. Top objections: compliance standards, "systems oversimplify clinical data".

### POL (Physician Office Lab)
A lab inside a doctor's office. CMS code `GNRL_FAC_TYPE_CD = 21`. Largest single bucket of the ICP (5,745 of 9,193 in Q1 2026 file). Primary target.

### PSC (Patient Service Center)
Walk-in collection point or independent diagnostic center. Like a US analogue of Russian Invitro. CMS code mostly `GNRL_FAC_TYPE_CD = 03` (ancillary test site) and friends.

### Reference Lab
A lab that accepts work from other labs and runs complex/specialized tests. CMS code `GNRL_FAC_TYPE_CD = 15` (independent). High test volume. Premium target.

### Hospital lab
A lab embedded in a hospital. CMS code `GNRL_FAC_TYPE_CD = 14`. **Excluded** because of Epic/Cerner lock-in.

### Hospital lab exception switch (HOSP_LAB_EXCPTN_SW)
CMS POS-file field. `Y` = hospital lab, `N` = standalone. We filter on `N`.

### CLIA Waiver lab
Lab with `CRTFCT_TYPE_CD = 2`. Only does the simplest tests. Doesn't need LIMS. **Excluded.**

### "Recently CLIA-certified"
A trigger segment. Lab with `CRTFCTN_DT >= 2025-01-01`. Logic: a lab that just got its certificate likely doesn't have an entrenched LIMS, so the sales cycle is faster.

### Russian-speaking segment
Lab owners who speak Russian, mostly concentrated in NJ/NY/PA per Andrew's note from kick-off. Approached separately — Andrew leads, Russian-language scripts, full Invitro case study.

### Custom self-hosted ("samopis")
Per Andrew's note: 3-5 known labs run a custom-built LIMS that a contractor maintains for ~$800/month. Different value prop ("professional cloud LIMS without maintenance burden").

### Buying trigger
An external event that makes a lab actively shopping. Examples:
- Recently CLIA-certified (the strongest)
- Expanding test menu (job postings)
- Hiring a new Lab Director
- Switching off a competitor (G2 reviews mentioning migration)
- M&A (multi-site consolidation)

### Objection handling
Pre-written responses to the most common objections per persona. Lives in `reference/icp/persona-*.md`. The three universal objections we expect:
1. "We're fine with our current system" — answered by three-phase migration
2. "Switching is 6-12 months of pain" — answered by mirror→proxy→decommission
3. "We're worried about data security" — especially acute when in-vitro case study is mentioned to non-Russian labs

---

## Competitors

The 8 LIMS vendors we track. Slugs match `lims-pain-extractor` filenames.

### LabWare (`labware`)
Global market leader, 3000+ customers (NIH, GSK, Pfizer). Strongest in pharma/biotech. G2: 4.5/5 across 100+ reviews. Common pain themes: integration complexity, customization burden.

### LabVantage (`labvantage`)
Owned by The Chatterjee Group. ~33% pharma reviews. G2: 3.8/5. Common pain: reporting customization (BO/Crystal complaints).

### QBench (`qbench`)
Modern cloud-native LIMS, 130+ G2 reviews at 4.5/5. Multi-vertical. Strongest "modern UX" competitor for Vivica. Common pain: scaling to high-volume clinical workflows.

### CrelioHealth (`creliohealth`)
Combined LIS+LIMS SaaS with transparent tiered pricing. India HQ, popular in mid-market diagnostic labs. Common pain: US-deployment friction.

### LigoLab (`ligolab`)
End-to-end LIS+LIMS+RCM (revenue cycle management) for clinical/anatomic-pathology/outreach labs. Common pain: implementation timeline, on-prem complexity.

### Clinisys (`clinisys`)
Incumbent (formerly Sunquest/Horizon family). The "safe enterprise" choice. Common pain: legacy UX, slow modernization, vendor lock-in.

### CloudLIMS (`cloudlims`)
Pure-SaaS direct competitor to Vivica on the "low IT, low upfront cost" axis. Common pain: limited customization vs enterprise needs.

### lims.net / LiMSEO (`lims_net`)
Also called **JTO** in Petr's Telegram chat. French-origin (Locasoft). Limited US adoption. Useful for European-tech-heavy labs in NJ.

### Sapiens / Sapio
Came up once in transcript as a competitor. Not in the active 8. May add later.

### Orchard / PathNet
Came up in early discussion. **Orchard** is a real LIMS competitor. **PathNet** is Cerner's lab module — it's part of "Cerner" exclusion, not a separate target.

---

## Data sources

### POS file (Provider of Services file)
CSV file CMS publishes quarterly. Contains every CLIA-certified lab in the US. Our Q1 2026 file has 676,051 rows. Downloaded from <https://qcor.cms.gov> bulk export.

### POS file fields we use

| Field | Meaning | Our use |
|---|---|---|
| `FAC_NAME` | Lab name | Display name |
| `ST_ADR`, `CITY_NAME`, `STATE_CD`, `ZIP_CD` | Address | Required (labs handle biomaterials) |
| `PHNE_NUM` | Phone | Contactability filter |
| `CRTFCT_TYPE_CD` | Certificate type | Filter to 1 or 4 |
| `CRTFCTN_DT` | Certification date | "Recently certified" trigger |
| `PGM_TRMNTN_CD` | Termination status | Filter to '00' (active) |
| `HOSP_LAB_EXCPTN_SW` | Hospital flag | Filter to 'N' |
| `GNRL_FAC_TYPE_CD` | Facility type | **Primary segmenter** (POL/PSC/REFERENCE) |
| `LAB_SITE_CNT` | Number of sites | Multi-site detection |
| `FORM_116_TEST_VOL_CNT` | Annual test volume | Lab size proxy |
| `CLIA_LAB_CLASSIFICATION_CD_1..10` | Specialty codes | **Mostly empty in practice** — use only as bonus signal |
| `PRVDR_NUM` | CLIA number | Unique ID |

### CLIA classification codes (`CLIA_LAB_CLASSIFICATION_CD_*`)
Specialty codes per 42 CFR Part 493 (e.g. 100=histopathology, 250=molecular, 800=toxicology). **Important caveat**: these fields are mostly populated as `00` (no specialty declared) for newly-certified labs. Only ~1% of POS-file rows have meaningful specialty codes. **Specialty must come from downstream website-scraping, not from CMS.**

### `GNRL_FAC_TYPE_CD` (general facility type code)
The **authoritative** segmenter. Documented in CMS layout PDF (Sept 2022). 29 values; we map them to 5 Vivica buckets (POL/PSC/REFERENCE/UNSUITABLE/OTHER).

### QCOR (Quality, Certification & Oversight Reports)
CMS portal at <https://qcor.cms.gov>. Where the POS file is downloaded from. Also has a search UI for individual labs.

### Apollo
Lead-data platform. Used downstream of `clia-source` for people enrichment (the POS file has companies but no people/emails). Per Sonya's notes: 1 keyword per request gives 7× more unique results; +45 click trick to expand pages; exclusion lists; lookalike search.

### Apollo lookalike
Apollo feature — give it a known good company, it returns similar companies. Used per Sonya for finding more labs of the same profile.

### Clay
Enrichment platform. Used by the agency for AI-powered lookups. Has Claygent (LLM agent inside Clay) and HTTP API + webhooks. Not in our pipeline (we use Apollo for people enrichment), but mentioned in the agency stack.

### Crona
AI enrichment tool mentioned in transcripts. Part of agency stack alongside Clay.

### NPI (National Provider Identifier)
US healthcare provider ID. Came up in early discussion as alternative data source — not used (CLIA POS is more relevant for labs).

### PubMed / RapidAPI
Mentioned as research sources in early-design discussion. Not in current pipeline.

### Sally Hypothesis dashboard
The agency's Google Sheet tracking which segments × hypotheses are being tested. Mirrored in `tracking/hypotheses.csv` for our project.

### Vivica ICP Google Sheet
The Sally team's working sheet of personas + objections + responses + KPIs. Source of truth for `reference/icp/persona-*.md`.

---

## Pipeline & tooling

### gtm-mcp
The team's existing production-grade outreach MCP at <https://github.com/impecablemee/gtm-mcp>. **49 tools, 13 base skills, single `/launch` command.** Owns the entire execution layer. We build extensions on top.

### MCP (Model Context Protocol)
Anthropic's standard for connecting LLMs to tools/data. Implemented as servers (e.g. gtm-mcp). Claude Code, Codex CLI, Cursor, Antigravity all support MCP.

### MCP server
A backend that exposes a set of tools to an MCP-aware client. Examples:
- **gtm-mcp** — our primary, custom-built for outreach
- **Smartlead MCP** ([LeadMagic/smartlead-mcp-server](https://github.com/LeadMagic/smartlead-mcp-server)) — 116+ tools
- **Apollo MCP** ([Chainscore/apollo-io-mcp](https://github.com/Chainscore/apollo-io-mcp)) — 27 tools
- **Notion / Linear / Supabase / GitHub / Miro** — third-party MCP servers we have available

### Agent skill / Skill
A self-contained capability folder with `SKILL.md` + scripts + references. Read by Claude Code, Codex, Antigravity. Standard at <https://github.com/anthropics/skills>. Auto-discovered from `.claude/skills/`.

### `SKILL.md`
Frontmatter file describing one skill: `name`, `description`, body explaining when to use, workflow, output format. Must be in English (Anthropic standard).

### `README.ru.md`
Russian-language companion to each `SKILL.md` so Yana and team can understand the skill without parsing English. Lives next to the SKILL.md.

### `/launch` command
gtm-mcp's main entry point. Three modes:
1. **Fresh** — new project, new offer, new ICP
2. **New campaign in existing project** — same project, new segment
3. **Append to existing campaign** — add more leads to a running campaign

### Pipeline state
gtm-mcp's persistent state at `~/.gtm-mcp/projects/<slug>/`. Contains `project.yaml`, `state.yaml`, `contacts.json`, `runs/run-N.json`, `campaigns/<slug>/`. **Never duplicate this in the project repo** — repo holds inputs and knowledge, gtm-mcp owns execution and state.

### `filter_intelligence.json`
Cross-run learning file at `~/.gtm-mcp/filter_intelligence.json`. gtm-mcp tracks keyword quality scores between runs — keywords that produced low-quality leads get downweighted next time.

### GOD_SEQUENCE / 12-rule email sequence
gtm-mcp's `email-sequence` skill applies 12 rules to generate copy. Used downstream of any segment we build.

### `linkedin-sequence` (414 flows)
gtm-mcp's LinkedIn sequence skill. 414 pre-built flows. Used via GetSales.

### `reply-classification` (3-tier funnel)
gtm-mcp's reply handler. Tier 1: regex (free). Tier 2: keywords (free). Tier 3: LLM (cheap). Used to triage incoming replies into interested / not-interested / out-of-office / etc.

### Cost gating
gtm-mcp rule: **never spend Apollo (or any paid API) credits without explicit user confirmation**. We follow this rule in all our extensions too.

### Blacklist
gtm-mcp deduplication via cleaned domain. `blacklist_check`, `blacklist_add`, `blacklist_import` tools. Used to avoid contacting the same domain twice across runs.

### Cleaned domain
Domain after stripping `www.`, mailto:, params, etc. The canonical key for company dedup.

### SmartLead
Email-sending platform. Used by gtm-mcp for cold-email campaigns. We never push to SmartLead without confirmation (sending to real people).

### GetSales
LinkedIn automation platform. Used by gtm-mcp for LinkedIn flows. Has SSI (Social Selling Index) calculator inside — see Sofia's training notes.

### Sender Profile (GetSales)
A LinkedIn account configured in GetSales. Multiple sender profiles can rotate to spread send volume — see Sofia's training.

### SSI (Social Selling Index)
LinkedIn metric. GetSales has a calculator. Higher SSI = better delivery rates.

### Antigravity / Claude Code / Codex CLI / Cursor
MCP-aware AI development environments. Skills must work across all of these (Agent Skills standard guarantees this).

---

## Skills & this repo

### `vivica-outreach` repo
This project's git repository. Contains plans, reference, extensions, input-data, tracking. Versioned in git.

### `extensions/.claude/skills/`
Where our 3 Vivica-specific skills live. Auto-discovered by Claude Code when working in this repo.

### `clia-source` skill
Our skill #1. Filters the CMS POS file (676k rows) into Vivica ICP companies (~9k). Produces master JSON + per-bucket CSVs in gtm-mcp project format. **Replaces** Apollo company-search step for the lab vertical (Apollo doesn't index CLIA data).

### `lims-pain-extractor` skill
Our skill #2. Builds a corpus of competitor LIMS pain points by scraping G2/Capterra/SourceForge/ITQlick/TrustRadius. Outputs structured pain entries (theme + count + intensity + ≤15-word quote + source URL) per vendor. Feeds into `email-sequence` for competitor-conquest sequences.

### `lims-detector` skill
Our skill #3. Detects which LIMS vendor a specific lab uses. Signals: iframe src on patient portal, JS bundle URLs, DNS CNAME on `results.<domain>` / `portal.<domain>`, job posting language. Outputs `current_lims` field per company.

### `reference/` directory
Domain knowledge in our repo: ICP personas, competitor profiles, battle cards, case studies, playbooks, vivica-intel. Read by skills and plans.

### `plans/` directory
Outreach plans, one per campaign. Each gets fed to `/launch`. Modeled on `outreach-plan-fintech.md` from gtm-mcp (~400 lines, 3 sequences).

### `input-data/` directory
Raw inputs: POS file CSV, ADLM attendees list, scraped HTML, etc. Mostly gitignored if PII.

### `tracking/` directory
Business analytics on top of gtm-mcp runs. Contains `hypotheses.csv` (mirrors Sally Hypothesis dashboard) and `decisions-log.md`.

### Battle card
A document for one persona × one competitor. Combines: the persona's top objections (from ICP table) + the competitor's top pains (from `lims-pain-extractor`) + the right Vivica response. Lives in `reference/battle-cards/<competitor>_x_<persona>.md`.

### Competitor profile
A document for one competitor (e.g. `reference/competitors/labware.md`). Contains: market position, pain corpus from `lims-pain-extractor`, internal notes, migration angle.

### Three-phase migration framework
Vivica's universal answer to "switching is too risky":
1. **Mirror** current LIS configuration in Vivica (parallel setup, no disruption)
2. **Proxy** live workflows through Vivica next to legacy (validate end-to-end)
3. **Decommission** legacy components incrementally under monitoring

Lives in `reference/playbooks/three-phase-migration.md`.

### Russian segment playbook
Rules for handling russian-speaking outreach: Andrew leads, Russian scripts, full Invitro case study OK, **anonymize Invitro for non-Russian labs**. Lives in `reference/playbooks/russian-segment.md`.

### Acure case study
Vivica's flagship reference customer. Acure Reference Lab in NJ, $100M+ revenue. Joint published study with KOL — usable in cold emails. Lives in `reference/case-studies/acure-reference-lab-nj.md`.

### Outreach plan
A markdown file in `plans/` that describes one campaign end to end: ICP, segments, sequences, schedule, KPIs. Modeled on gtm-mcp's `outreach-plan-fintech.md` (447 lines, 3 sequences). Fed to `/launch`.

### Hypothesis tracking
Each campaign tests a hypothesis ("recently CLIA + russian-speaking has higher reply rate than just recently CLIA"). Tracked in `tracking/hypotheses.csv`, mirroring Sally's dashboard.

---

## Process & playbook terms

### Cold outreach / Cold email
Sending email/LinkedIn messages to people who haven't asked for them, hoping to start a sales conversation.

### Sequence
A series of 4-5 emails (or LinkedIn messages) sent on a schedule (typically 3-4 days apart). Industry standard: follow-ups generate ~42% of all replies.

### Tier 1 / Tier 2 personalization
- **Tier 1**: same boilerplate for whole segment (just `{firstName}` + segment name)
- **Tier 2**: per-person research (current LIMS, recent triggers, specialty)
- gtm-mcp's email-sequence does Tier 2 automatically when we provide enriched data

### Volume sequence vs Fresh sequence vs Competitor-conquest
Three sequence types from gtm-mcp's `outreach-plan-fintech.md`:
- **Volume**: broad ICP, generic pain, low personalization, big audience
- **Fresh**: trigger-based (recently funded, recently certified). Highest reply rates.
- **Competitor-conquest**: targets known users of competitor X, uses pain corpus

### Reply rate / Open rate / Bounce rate
Standard email metrics. Targets per gtm-mcp's plan: open >40%, reply >2%, bounce <2%.

### A/B test
Two subject-line variants run on the same audience to see which performs better. Standard practice; gtm-mcp's email-sequence supports this natively.

### "Via negativa" qualification
gtm-mcp's `company-qualification` skill philosophy. Instead of trying to confirm "is this a fit?", it tries to **disqualify**: "is there a clear reason this is NOT a fit?" Reaches 97% accuracy with a 2-pass re-evaluation.

### Apify
Web-scraping infrastructure. gtm-mcp's `scrape_website` and `scrape_batch` use Apify proxy to handle JS rendering and avoid blocks. Our `lims-detector` and `lims-pain-extractor` should use the same Apify path when run inside Claude Code.

---

## Team & people

### Petr Nikolaev (Sally / Life Data Lab)
Strategy, agency side. Wrote the $500/month scope plan in Telegram (image #1). Knows JTO = lims.net (image #2).

### Yana Arnautova (Sally / Life Data Lab)
Day-to-day pipeline operator and owner. Russian speaker. **The whole project is built to be runnable end-to-end by Yana** — this drives the bilingual READMEs and self-explanatory plans.

### Rinat Khatipov (Sally / Life Data Lab)
Agency lead. Made the parallel comparison "we did this for a CRM project — figured out which CRM each company used, then wrote competitor-specific messages."

### Chris Hilinsky (Vivica)
Co-founder, US market, English LinkedIn outreach. Source of the patient-portal iframe detection technique.

### Andrew (Vivica)
Russian-speaking segment lead. Offers $100 Amazon gift cards for 30-min interviews. Knows the 3-5 "samopis" (custom self-hosted) labs.

### Evgenia Farikh (Vivica)
Optional third LinkedIn account.

### Sonya / Sofia (Sally training)
Apollo workflow trainer (Sonya) and GetSales trainer (Sofia). Sources of the Apollo workflow notes (`Apollo.md`) and GetSales notes (`GetSales.md`).

### Acure Reference Lab
Vivica's flagship customer. NJ-based, $100M+ revenue. Has a joint published study with a KOL.

---

## Events & deadlines

### ADLM 2026
**Critical deadline.** AACC's annual meeting. **26-30 July 2026, Anaheim Convention Center, ~15,000 attendees, 850+ exhibitors.** Pre-conference outreach is the project's main deliverable. As of 10 May 2026, that's ~11 weeks away.

### Pre-conference outreach
Reaching out to confirmed attendees 4-6 weeks before the conference, offering a meeting at the booth or in Anaheim.

### Onsite outreach
Real-time outreach during the conference itself. Different cadence (same-day responses) and tone (more casual).

### Post-conference follow-up
Reaching out 1-2 weeks after the conference to people who attended but didn't book a meeting. Trigger phrase: "saw you at ADLM".

---

## Agent autonomy

What an AI agent (Claude in Claude Code, or any agent driving gtm-mcp) **can do without asking** vs what requires human approval. This is critical for letting Yana run the project.

### Agent CAN do without asking

**Read-only operations:**
- Read any file in `reference/`, `plans/`, `input-data/`, `tracking/`
- Read gtm-mcp state in `~/.gtm-mcp/projects/vivica/`
- Read past run logs and replies
- Search through past chats for context

**CLIA data work** (free, no API):
- Run `clia-source` filter with any `--since` date
- Re-segment the POS file by any axis (state, specialty, facility type)
- Generate per-segment CSVs
- Cross-reference `russian_candidates_nj.csv` with input data

**Public-web scraping** (free, no API):
- Run `lims-pain-extractor` on G2, Capterra, SourceForge, ITQlick, TrustRadius
- Refresh competitor pain corpus when stale
- Run `lims-detector` on a single domain or batch
- Re-classify a lab's `current_lims` when previous detection was unknown

**Generation & maintenance** (free, no external API):
- Generate battle cards from existing personas + pain corpus
- Generate competitor profiles from pain corpus
- Update reference docs to match latest CMS layout or data findings
- Validate copyright rules (≤15-word quotes, ≤1 quote per source, no song lyrics)
- Reformat plans to match gtm-mcp's expected structure
- Lint outreach plans for missing fields
- Update `tracking/hypotheses.csv` with run results

**Git operations on feature branches:**
- Create feature branches
- Commit changes
- Push to feature branches
- Open PRs for review

### Agent MUST ask before

**Spending money:**
- Apollo people enrichment (consumes credits)
- Apollo company enrichment by domain (consumes credits)
- Any paid API call
- Even small spends — this is gtm-mcp's hard rule

**Sending real messages:**
- Pushing campaigns to SmartLead (sends real emails)
- Pushing flows to GetSales (sends LinkedIn messages)
- Adding leads to active campaigns
- Anything that arrives in a real person's inbox

**Destructive operations:**
- Deleting files in `reference/`, `plans/`, `tracking/`
- Force-pushing to main
- Removing entries from blacklist
- Stopping running campaigns mid-flight

**High-stakes interpretation:**
- Confirming a lab is "russian-speaking owner" (Andrew's call, not the agent's)
- Anonymizing the in-vitro case study (the agent applies the rule, but humans verify edge cases)
- Adding a new competitor to the tracked-8 list

### Agent NEVER does

- Modify another team's repo (gtm-mcp itself — only PRs)
- Share leads or PII outside the project repo
- Quote >15 words from a copyrighted source
- Use the in-vitro case study verbatim for non-Russian labs
- Generate emails directly to send (always through gtm-mcp's email-sequence + human review)
- Bypass the cost-gating rule, even with claimed urgency

### Default behavior when in doubt

**If unsure, ask.** Better to interrupt for confirmation than to spend credits or send messages incorrectly. This is a paid client project; trust loss is worse than time loss.

When asking, be specific about:
1. **What** the agent wants to do
2. **Why** (which trigger / data prompted it)
3. **Cost** (credits, real-message volume, time)
4. **Reversibility** (can we undo if wrong?)

---

## Cross-references

- For the architectural separation between gtm-mcp and this repo, see `README.md`.
- For the data-source story (CMS POS file → ICP), see `extensions/.claude/skills/clia-source/SKILL.md`.
- For the competitor pain corpus structure, see `extensions/.claude/skills/lims-pain-extractor/SKILL.md`.
- For LIMS vendor detection details, see `extensions/.claude/skills/lims-detector/SKILL.md`.
- For Russian-language version of this glossary, see `glossary.ru.md`.
