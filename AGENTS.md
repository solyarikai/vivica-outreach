# Vivica Outreach — Agent Schema

> **START HERE.** Read this file first, then [[index]] to orient yourself before any work.

---

## Entity Types & Directories

| Type | Directory | Create/update when |
|---|---|---|
| Source Lists — raw | `source-lists/<source-name>/` | Raw + segmented company lists from external sources (CMS POS, Apollo exports). Source-of-truth, immutable. |
| Source Lists — enrichment runs | `source-lists/enrichment-runs/<YYYY-MM-DD>_<segment>_<tool>/` | One folder per enrichment prog. Contains `input.csv`, `output.csv` (+ stages if multi-step), and `manifest.md`. |
| Source Lists — segments | `source-lists/segments/` | Final merged artifacts ready for downstream pipeline (domains/contacts merged in). |
| Outreach Plans | `plans/` | New campaign, segment pivot, targeting change |
| ICP Personas | `reference/icp/` | New insight from calls, objection pattern discovered |
| Competitor Profiles | `reference/competitors/` | New G2 review, pricing intel, product update |
| Battle Cards | `reference/battle-cards/` | Competitive angle found, new pain confirmed |
| Playbooks | `reference/playbooks/` | Workflow change, new segment process |
| Company Intel | `reference/company/` | Vivica product/positioning update |
| Case Studies | `reference/case-studies/` | New reference customer, new outcome data |
| Decisions | `tracking/decisions-log` | Any strategic call: stop, scale, pivot |
| Session Log | `tracking/log` | **Every session end** — append one entry |
| Data Log | `tracking/data-log` | **Every data operation** (enrichment run, merge, export) — append entry with run-id, counts, errors |

---

## [[Wikilink]] Convention

Use `[[filename]]` for all internal links. Obsidian resolves these by filename without extension.

```markdown
[[index]]                          # root file
[[persona-ceo-owner]]              # reference/icp/
[[clinisys]]                       # reference/competitors/
[[clinisys_x_ceo-owner]]          # reference/battle-cards/
[[outreach-plan-vivica-clia-fresh]] # plans/
[[decisions-log]]                  # tracking/
```

**Rules:**
- Every plan → links to the ICP personas it targets + competitors it conquests
- Every battle card → links back to its `[[competitor]]` + `[[persona]]`
- Every decision entry → links to the plan or file it affects
- `reference/` files are **foundations** — they receive links, link to each other only when directly relevant, never link to `plans/` or `tracking/`

---

## What Goes Where — Decision Tree

```
New campaign segment?         → plans/outreach-plan-vivica-[segment].md
ICP insight from call?        → reference/icp/persona-[role].md
Competitor pain confirmed?    → reference/competitors/[vendor].md + battle card update
"We decided to stop X"        → tracking/decisions-log (append entry)
New workflow / process?       → reference/playbooks/[name].md
Session end?                  → tracking/log (append entry)
Data op (enrich, merge)?      → tracking/data-log (append entry) + new run folder under source-lists/enrichment-runs/
New reference customer?       → reference/case-studies/[lab-name].md
Vivica product update?        → reference/company/vivica-intel.md
```

---

## Index Update Protocol

When you **create** a new file or **significantly update** an existing one:
1. Open [[index]]
2. Add/update its entry under the correct section
3. Format: `- [[filename]] — one-line description (≤10 words)`

---

## Log Protocol

At the end of every session, append to [[tracking/log]]:

```markdown
## [YYYY-MM-DD] — one-line session summary
- what changed or was decided
- what's next
```

---

## Foundations Rule

`reference/` is a **terminal layer** — files here are source-of-truth reference material.

- They **receive** `[[links]]` from plans, battle cards, and AGENTS
- They **link to each other** only when directly relevant (e.g., a battle card links to its competitor + persona)
- They **never link to** `plans/`, `tracking/`, or root files
- Update them carefully — they're the base layer everything else is built on

---

## Enrichment Run Convention

Every data operation (enrichment, scrape, batch lookup) lives in its own folder under `source-lists/enrichment-runs/`:

```
source-lists/enrichment-runs/<YYYY-MM-DD>_<segment>_<tool>/
  input.csv           # what went in
  output.csv          # what came back (final result of this run)
  stages/             # optional — intermediate batches if run was multi-step
    <stage-name>.csv
  manifest.md         # what, when, why, counts in/out, errors, status
  analytics.md        # optional — funnel breakdown, persona splits, cost analysis for runs with non-trivial multi-stage pipelines
  *.py                # optional — scripts used for this run (kept for reproducibility)
```

**Folder name format:** `<date>_<segment>_<tool>` — e.g. `2026-05-10_russian-190_clay`, `2026-05-12_reference-1849_exa`. Lowercase, hyphens, no spaces.

**manifest.md must contain:**
- Date, run-id (= folder name), tool used, operator
- Source: which raw file or upstream run this draws from
- Input: row count, columns sent
- Output: row count, columns added, success rate
- Errors / skipped rows
- Status: in-progress / done / superseded-by-<run-id> / failed
- Cost (credits, $ if applicable)
- Next: where this output flows to (segment file, downstream run)

**Append to `tracking/data-log`** for every run — one-line summary that points to the manifest.

**SMTP double-verify rule** (per [[decisions-log]] 2026-05-11): emails from Apollo Reveal MUST be re-verified via FindyMail `/api/verify` before loading to SmartLead. Apollo's `verified` flag has ~14% real bounce rate.

**Apollo Reveal rule** (per [[decisions-log]] 2026-05-11): always save `apollo_id` in Apollo people search outputs and hydrate emails by `id` (Reveal). Do NOT use name-based email-finders on obfuscated Apollo first-name-only contacts.

**Lifecycle:**
- Raw inputs in `source-lists/<source-name>/` are immutable
- Enrichment runs are append-only — never edit a finished run, supersede it with a new dated folder
- Final merged artifacts go to `source-lists/segments/`
- Test/abandoned runs stay in `enrichment-runs/` with `status: superseded` in manifest — don't delete history

---

## Schema Extension Protocol

When the work doesn't fit existing entity types — **STOP**. Do not invent new top-level dirs or entity types silently. The schema is contract, not suggestion.

### Step 1 — Classify the need

| Situation | Action |
|---|---|
| New file matches existing entity type (new competitor, persona, plan) | ✅ Just create it in the existing dir, update [[index]] |
| New file doesn't match any existing type | ⛔ STOP, go to Step 2 |
| Need to restructure (move, split, rename dirs) | ⛔ STOP, go to Step 2 |
| New top-level directory | ⛔ STOP, go to Step 2 |

### Step 2 — Frame the question (answer all before proposing)

1. **What problem does this solve?** (1 sentence)
2. **Lifecycle** — one-off, or will more files like this appear over time?
3. **Content** — tool output, human-curated knowledge, raw data, generated artifact?
4. **Ownership** — agent auto-updates, human-only, mixed?
5. **Connections** — which existing [[entities]] should it cross-reference?

### Step 3 — Propose 2–3 options to user, then wait

Present concrete options with tradeoffs. Template:

```
Need: <one-line problem statement>

Option A — extend existing entity type
  Where: reference/tools/<name>.md
  Pros:  reuses foundation rules, no schema change
  Cons:  forces it into "reference" mental model

Option B — new top-level dir
  Where: <newdir>/
  Pros:  clear ownership when has its own state/scripts/artifacts
  Cons:  schema growth, more rules to maintain

Option C — inside extensions/
  Where: extensions/.claude/skills/<name>/
  Pros:  pure automation logic, no domain knowledge
  Cons:  invisible to non-Claude users

Recommend: <pick one with reason>. Confirm or pick another?
```

### Step 4 — After user approves

Before creating the actual files:
1. Update [[AGENTS]] — add new entity type to the table at top
2. Update [[index]] — add new section with [[wikilinks]]
3. Append to [[decisions-log]] — record the schema decision with date + reasoning
4. *Then* create files

### Worked example — "We're adding Apollo enrichment, where does it go?"

```
Need: store Apollo-specific gotchas, search filters, credit rules, lookup scripts

Q1 problem: knowledge + ops for one external tool
Q2 lifecycle: recurring — more tools (Findymail, Clay) likely follow same pattern
Q3 content: mix — markdown knowledge + JSON configs + bash scripts
Q4 ownership: human-curated knowledge, agent-updated gotchas
Q5 connections: linked from plans/ that use Apollo, references competitors

Option A — reference/tools/apollo.md (single file)
  Pros: lightweight, fits existing foundation pattern
  Cons: scripts/configs don't fit in markdown

Option B — tools/apollo/ (new top-level dir with subfiles)
  Pros: scales to multiple tools, holds knowledge + scripts + state
  Cons: new entity type "Tool Integration" needs AGENTS.md table update

Option C — extensions/.claude/skills/apollo/
  Pros: zero schema change, native Claude skill location
  Cons: domain knowledge buried in skill folder, not browsable in Obsidian

Recommend: B if more tools are coming. A if Apollo is the only one. Pick?
```

---

## Do NOT

- Duplicate gtm-mcp state — runs, contacts, replies live in `~/.gtm-mcp/projects/vivica/`
- Store PII in this repo
- **Create top-level dirs or new entity types without Schema Extension Protocol**
- Write speculative information — only confirmed intel goes into reference files
