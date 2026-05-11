# Vivica Outreach

Cold outreach for **Vivica.us** — cloud LIMS for US clinical laboratories.

## Start here

1. Read `AGENTS.md` — wiki schema, entity types, what goes where
2. Read `index.md` — master catalog with links to all files
3. Read the relevant plan from `plans/` for the current task

## Key facts

- LIMS = Laboratory Information Management System
- ICP: 3 personas × 8 competitor vendors = 24 battle cards
- Primary source: CMS POS file (9,193 CLIA-certified labs), not Apollo
- State (runs, contacts, replies) lives in `~/.gtm-mcp/projects/vivica/` — never duplicate here

## Session end

Append one entry to `tracking/log.md`. Format: `## [YYYY-MM-DD] — summary`.

## New tools / new pipelines / new dirs

If the task needs a structure that doesn't fit existing entity types — **STOP**. Do not invent dirs. Follow the Schema Extension Protocol in `AGENTS.md` (propose 2–3 options with tradeoffs, wait for approval, update AGENTS + index + decisions-log first, *then* create files).
