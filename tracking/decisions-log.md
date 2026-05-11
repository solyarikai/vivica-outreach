# Decisions Log — Vivica Outreach

Chronological record of significant decisions: scope, scale-up/down, segment activation, copy changes, pivot moments. Update **at every weekly sync** and any time a meaningful operational decision is made.

Format per entry:
- **Date** (YYYY-MM-DD)
- **Decision** (one-line summary)
- **Context** (what data / observation triggered this)
- **Owner** (who made the call)
- **Reversible?** (yes / no — affects how cautious we should be)

---

## 2026-05-10 — project scaffold complete

**Decision**: project repo scaffolded with skills, plans, reference, glossary, checklist. Ready for stakeholder kick-off.

**Context**: 4-response generation sprint over kick-off conversation produced 47 files, ~7,700 lines. CLIA Q1 2026 file processed → 9,193 ICP labs ready in 5 buckets + 190 russian candidates.

**Owner**: Yana

**Reversible?**: yes (everything still pre-launch)

**Affects**: [[outreach-plan-vivica-clia-fresh]] · [[outreach-plan-vivica-russian-nj]] · [[outreach-plan-vivica-using-labware]] · [[outreach-plan-vivica-adlm-2026]]

**Next actions**:
- Stakeholder kick-off call (Chris, Andrew, Petr, Yana)
- Close Acure open questions (10 items in [[acure-reference-lab-nj]])
- Decide: pilot segment (POL recommended)
- Decide: git remote, repo access roster
- Set up environment per [[CHECKLIST]] Step 2

---

## 2026-05-10 — schema extension: Source Lists entity type

**Decision**: add `source-lists/` as new entity type for raw + segmented company lists and enrichment input/output staging. Existing `clia-icp-companies-Q1-2026/` folder (created ad-hoc) renamed/moved to `source-lists/clia-q1-2026/`. New enrichment staging lives at `source-lists/clay-enrich-input/`.

**Context**: 190-company Russian list and 1849-company Reference list need Clay enrichment for domains + LinkedIn. Existing schema had no entity type for source data — `reference/` is for foundations (personas, competitors, playbooks), `plans/` is campaigns, `tracking/` is logs. Created Clay-input CSVs without schema update; caught and corrected per Schema Extension Protocol.

**Owner**: Yana

**Reversible?**: yes

**Affects**: [[AGENTS]] · [[index]] · [[outreach-plan-vivica-russian-nj]] · [[outreach-plan-vivica-clia-fresh]]

**Next actions**:
- Run Clay Find Company on both CSVs → produce enriched CSVs in `source-lists/clay-enrich-output/`
- Re-merge domains back into segmented bucket files
- Move to people enrichment (Apollo MCP + FindyMail) per plan gating

---

## 2026-05-10 — schema refactor: enrichment-runs + data-log, kill input-data

**Decision**: restructure `source-lists/` to use **per-run folders** under `enrichment-runs/<date>_<segment>_<tool>/` with mandatory `manifest.md`. Add new `tracking/data-log.md` (append-only journal of data operations, separate from session log). Delete unused top-level `input-data/`. Replace flat `clay-enrich-input/` + `clay-enrich-output/` with run-folder structure.

**Context**: after first enrichment session, `clay-enrich-output/` already had 13 files from one project across 2 tools (Clay + Exa) and 4 Exa stages — no way to tell which is final, test, superseded. At 10 projects unsearchable. No data-operations log existed (`tracking/log.md` is session-level only). `input-data/` was scaffold-only, never used, semantic dup with `clay-enrich-input/`.

**Owner**: Yana

**Reversible?**: yes (file moves only, no data loss)

**Affects**: [[AGENTS]] · [[index]] · all future enrichment work

**Next actions**:
- Move files into 3 run folders: `2026-05-10_russian-190_clay`, `2026-05-10_reference-1849_clay`, `2026-05-10_all-2039_exa`
- Write manifest.md for each run, backfill data-log
- Delete `input-data/`, `clay-enrich-input/`, `clay-enrich-output/`

---

## 2026-05-11 — Apollo `verified` flag is NOT trusted, SMTP double-verify mandatory

**Decision**: every email pulled from Apollo Reveal must be SMTP-verified via FindyMail `/api/verify` before loading to SmartLead. Apollo's `email_status=verified` flag alone is insufficient.

**Context**: in the reference-1849 run, 1033 Apollo-"verified" emails were re-checked via FindyMail SMTP — **14.4% failed** (149 invalid + 6 other). Loading these directly into SmartLead would have caused immediate bounce-driven reputation damage. Double-verify added ~$10 cost on 1033 emails but saved sender reputation and ~12% campaign deliverability.

**Owner**: Sales Engineer (Yarik)

**Reversible?**: no — this is a permanent quality gate for all future enrichment runs

**Affects**: [[AGENTS]] (enrichment convention) · all future enrichment runs · [[outreach-plan-vivica-clia-fresh]] · [[outreach-plan-vivica-russian-nj]]

**Next actions**:
- Apply same double-verify to russian-190 segment when it goes to enrichment
- Document SMTP double-verify as standard step in enrichment run convention

---

## 2026-05-11 — FindyMail name-search forbidden on obfuscated Apollo names

**Decision**: do NOT use FindyMail `/api/search/name` on contacts where only Apollo `first_name` is known (last name obfuscated). Use Apollo Reveal by `id` exclusively for hydrating Apollo-found contacts.

**Context**: in the reference-1849 run, FindyMail name-search on 219 Apollo misses (first_name + domain only, no surname) returned **1 found out of 219 = 0.5% hit rate**. Earlier in the same session, the same approach on the first 269 contacts gave 12% hit but all `verified=false` (32 dirty emails, wasted ~$0.32 GetSally credits). Apollo Reveal by `id` gives 82.5% hit on the same contacts. The right pattern is: Apollo people search **always saves `id`** → Apollo Reveal by `id`, never name-based fallback.

**Owner**: Sales Engineer (Yarik)

**Reversible?**: no — wastes credits and produces dirty data

**Affects**: [[AGENTS]] (enrichment convention) · all future Apollo-based enrichment

**Next actions**:
- Always save `apollo_id` column in Apollo people search outputs
- For non-Apollo segments (LinkedIn, Clay, manual): FindyMail name-search OK only with **full** first+last name

---

<!-- Template for future entries:

## YYYY-MM-DD — Short title

**Decision**: 

**Context**: 

**Owner**: 

**Reversible?**: 

**Next actions**:
- 

-->
