# Vivica Outreach — Project Repository

Cold outreach campaigns for **Vivica.us**, a cloud-based LIMS (Laboratory Information Management System) for clinical laboratories. Built on top of [gtm-mcp](https://github.com/impecablemee/gtm-mcp).

## Quick start

```bash
# 1. clone alongside gtm-mcp
git clone <this-repo> ~/code/vivica-outreach
cd ~/code/vivica-outreach

# 2. ensure gtm-mcp is installed and configured
# (see https://github.com/impecablemee/gtm-mcp)

# 3. open Claude Code in this directory
claude

# 4. launch the first campaign — recently CLIA-certified labs
/launch plans/outreach-plan-vivica-clia-fresh.md
```

## Architecture

```
gtm-mcp                       this repo
─────────                     ──────────────────
49 tools           ◄────────  /launch <plan>
13 base skills                  + extensions/
~/.gtm-mcp/state                + reference/
                                + plans/
                                + tracking/
```

**gtm-mcp** owns: Apollo search, classification, SmartLead/GetSales push, sequence generation (12 rules), reply classification, blacklist, runs/state.yaml, cross-run intelligence.

**This repo** owns: Vivica-specific domain knowledge (ICP personas, competitor pains, battle cards, case studies, playbooks), CLIA POS-file as alternative source to Apollo, LIMS-vendor detection, hypothesis tracking.

## Repository layout

```
extensions/.claude/skills/        # Vivica-specific skills, auto-loaded by Claude Code
  clia-source/                    # filter CMS POS file → ICP companies (alternative to Apollo)
  lims-pain-extractor/            # parse G2/Capterra reviews of competitor LIMS vendors
  lims-detector/                  # detect which LIMS a lab uses (iframe inspection)

plans/                            # outreach plans, each fed to /launch
  outreach-plan-vivica-clia-fresh.md       # primary: recently CLIA-certified labs
  outreach-plan-vivica-russian-nj.md       # russian-speaking lab owners (NJ market)
  outreach-plan-vivica-using-labware.md    # competitor-conquest: LabWare migrants
  outreach-plan-vivica-adlm-2026.md        # pre-conference outreach for ADLM (July)

reference/                        # domain knowledge, read by skills and plans
  company/                        # what is Vivica
  icp/                            # 3 personas with objection responses
  competitors/                    # 8 competitor profiles with G2-extracted pains
  battle-cards/                   # competitor × persona matrix
  case-studies/                   # Acure Reference Lab (NJ)
  playbooks/                      # russian-segment, three-phase migration, ADLM workflow

input-data/                       # raw data sources (gitignored if PII)
  POS_File_CLIA_Q1_2026.csv       # CMS Provider of Services file (676k labs)

tracking/                         # business analytics on top of gtm-mcp runs
  hypotheses.csv                  # mirrors Sally Hypothesis dashboard
  decisions-log.md                # rationale for stopping/scaling segments
```

## Where state lives

| What | Where | Why |
|---|---|---|
| Pipeline state, runs, contacts, replies | `~/.gtm-mcp/projects/vivica/` | gtm-mcp canonical state |
| Outreach plans, ICP, competitors, playbooks | this repo (`reference/`, `plans/`) | versioned domain knowledge |
| Raw CLIA file, attendee lists | this repo (`input-data/`) | source data |
| Hypothesis tracking | this repo (`tracking/`) | business analytics |

Never duplicate gtm-mcp state into this repo. The repo is **inputs and knowledge**; gtm-mcp owns **execution and outputs**.

## Team

- **Chris Hilinsky** — Vivica co-founder, US market, English outreach LinkedIn
- **Andrew** — russian-speaking segment lead
- **Evgenia Farikh** — optional third LinkedIn account
- **Petr (Sally)** — strategy, agency side
- **Yana (Sally)** — campaign operations, day-to-day pipeline
- **Rinat (Sally)** — agency lead

## See also

- [README.ru.md](./README.ru.md) — то же самое на русском для команды
- [gtm-mcp CLAUDE.md](https://github.com/impecablemee/gtm-mcp/blob/main/CLAUDE.md) — base pipeline reference
