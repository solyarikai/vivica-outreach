# Vivica Outreach — Index

> Agent: read [[AGENTS]] for schema rules, then this file to find what you need.
> Human: use Obsidian graph view to see connections.

---

## Schema & Navigation
- [[AGENTS]] — wiki rules, entity types, what goes where (read first)
- [[README]] — architecture, team, quick start, repo layout

---

## Active Plans

| Plan | Segment | Status |
|---|---|---|
| [[outreach-plan-vivica-clia-fresh]] | Recently CLIA-certified labs | Active |
| [[outreach-plan-vivica-russian-nj]] | Russian-speaking lab owners, NJ | Active |
| [[outreach-plan-vivica-using-labware]] | LabWare migration conquest | Active |
| [[outreach-plan-vivica-adlm-2026]] | Pre-conference ADLM, July 2026 | Planned |

---

## ICP Personas

- [[persona-ceo-owner]] — decision-maker, budget owner, entrepreneur mindset
- [[persona-lab-director]] — operational buyer, day-to-day LIMS pain
- [[persona-medical-director]] — clinical oversight, compliance-driven

---

## Competitors (8 vendors)

| File | Vendor | Key angle |
|---|---|---|
| [[clinisys]] | Clinisys / Sunquest / Horizon | Largest, legacy on-prem, slow modernization |
| [[labware]] | LabWare | Enterprise, migration target, high TCO |
| [[lims-net]] | LIMS-net | SMB-focused, limited scalability |
| [[labvantage]] | LabVantage | Mid-market, complex implementation |
| [[cloudlims]] | CloudLIMS | Cloud-native but shallow feature set |
| [[creliohealth]] | Creliohealth | India-origin, US expansion |
| [[ligolab]] | LigoLab | Reference lab focus |
| [[qbench]] | QBench | Modern UI, SMB |

---

## Battle Cards (competitor × persona)

| | CEO/Owner | Lab Director | Medical Director |
|---|---|---|---|
| Clinisys | [[clinisys_x_ceo-owner]] | [[clinisys_x_lab-director]] | [[clinisys_x_medical-director]] |
| LabWare | [[labware_x_ceo-owner]] | [[labware_x_lab-director]] | [[labware_x_medical-director]] |
| LIMS-net | [[lims-net_x_ceo-owner]] | [[lims-net_x_lab-director]] | [[lims-net_x_medical-director]] |

---

## Playbooks

- [[russian-segment]] — workflow for Russian-speaking lab segment
- [[three-phase-migration]] — migration playbook for vendor-conquest
- [[adlm-conference]] — pre/during/post ADLM conference outreach

---

## Company & Case Studies

- [[vivica-intel]] — what Vivica is, positioning, differentiators
- [[market-analysis-us-clinical-labs-2026]] — US LIMS market sizing, competitor moves, audience pain (HTML version next to the .md)
- [[acure-reference-lab-nj]] — NJ reference lab (open questions inside)
- [[intake-report-vivica-2026-05]] — project intake report: discovery findings, market, ICP, segments, funnel, what's ready (May 2026)

---

## Source Lists

- `source-lists/clia-q1-2026/` — CMS CLIA Q1 2026 raw + segmented buckets (POL, REFERENCE, PSC, OTHER) + russian candidates NJ
- `source-lists/enrichment-runs/` — one folder per enrichment run with input/output/manifest (see [[AGENTS]] § Enrichment Run Convention)
- `source-lists/segments/` — final merged artifacts ready for downstream pipeline

---

## Tracking

- [[decisions-log]] — why we made strategic calls (stop/scale/pivot)
- [[tracking/log]] — session history, append-only
- [[data-log]] — data operations (enrichment runs, merges, exports), append-only

---

## Glossary

- [[glossary]] — EN terms
- [[glossary.ru]] — RU terms
