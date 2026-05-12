# Session Log — Vivica Outreach

Append-only chronological record of sessions. One entry per session.

Format:
```
## [YYYY-MM-DD] — one-line summary
- what changed / decided
- what's next
```

---

## [2026-05-10] — project scaffold complete, wiki initialized

- Repo scaffolded: 47 files, ~7,700 lines across plans, reference, tracking
- CLIA Q1 2026 file processed → 9,193 ICP labs in 5 buckets + 190 russian candidates
- Added: [[AGENTS]], [[index]], [[tracking/log]] — Obsidian wiki system initialized
- Next: stakeholder kick-off call (Chris, Andrew, Petr, Yana)
- Next: pilot segment decision (POL recommended), git remote, env setup per [[CHECKLIST]]

## [2026-05-11] — market analysis US clinical LIMS — first foundation pass

- Created [[market-analysis-us-clinical-labs-2026]] (.md + .html) in `reference/company/` — sized as company-intel extension to avoid new top-level dir
- Key findings: US LIMS $735M→$1.30B by 2030 (~10% CAGR); FDA LDT rule rescinded Sept 2025 (kill old positioning); Clinisys/Sunquest = primary conquest target; 24K/yr lab tech vacancies = burnout/automation angle
- Recommendations: spin up `outreach-plan-vivica-sunquest-conquest` (mirror of LabWare plan); confirm SOC 2; add CoPathPlus sunset hunting list; rewrite cold sequences to drop FDA-LDT angle
- Next: discuss findings with Chris; decide on Sunquest plan and CoPathPlus plan; refresh sequence copy

## [2026-05-11] — enrichment runs finalized, people enrichment blocked on Apollo API

**Domain enrichment completed:**
- Final segmented files copied to `source-lists/segments/`: russian_candidates_nj_domains.csv (190), bucket_REFERENCE_domains.csv (1849)
- All 3 enrichment runs finalized with manifests: Exa (all-2039), Clay (russian-190), Clay (reference-1849)

**People enrichment setup (blocked):**
- Created `2026-05-11_reference-1849_apollo-people` run folder with input sample (20 companies for test)
- Built `apollo_people_search.py` script for batch 3-persona (CEO/Owner, Lab Director, Medical Director) Apollo queries
- **Blocker**: Apollo API endpoint returned 404 — needs verification (endpoint structure change? account permissions?)
- Next: test Apollo API directly, resolve endpoint issue, then run script on sample + full 1849

**What's ready:**
- ✅ Domains for all reference labs (1849) + Russian candidates (190)
- ✅ Script + manifest for people enrichment
- ⏸️ Awaiting: Apollo API verification + Andrew's confirmation of russian-speaking labs

## [2026-05-11] — market analysis editorial pass + stakeholder briefings

- [[market-analysis-us-clinical-labs-2026]] — editorial rewrite (tone/readability, no data changes)
- Created brief-sally-petr-2026-05 — internal Sally briefing: project status, blockers, decisions needed (later deleted)
- Created brief-vivica-team-2026-05 — strategic market brief for Vivica team: 3 open windows, competitive landscape, what-not-to-do, open questions before active phase (later deleted)
- Next: share with Petr and Vivica team; get answers on Acure open questions; resolve Apollo API blocker

## [2026-05-11] — Reference segment email enrichment complete (Apollo Reveal + FindyMail double-verify)

- Apollo Reveal by `id` on 1252 contacts → 1033 verified (82.5%)
- FindyMail SMTP verify → 878 valid (14.4% bounce filtered — Apollo "verified" is unreliable)
- FindyMail name-search on 219 Apollo misses → 1 found (dead path with obfuscated names — won't repeat)
- Final: **344 verified contacts / 270 companies / 698 CLIA records (37.8%)** at total cost **~$11.70**
- Built `companies_enriched.csv` (281), `companies_not_enriched.csv` (738), `final_contacts_verified.csv` (344)
- Full funnel + persona analytics in `source-lists/enrichment-runs/2026-05-11_reference-1849_findymail-email/analytics.md`
- Updated `plans/outreach-plan-vivica-clia-fresh.md` with results section
- Next: 344 → SmartLead campaign per persona; 738 unenriched → LinkedIn Sales Nav / Clay (have `company_linkedin_url`)

## [2026-05-11] — brief-sally-petr rewrite: structure, Obsidian/MCP, lead analytics, removed Yaroslav

- Rewrote [[brief-sally-petr-2026-05]]: added project document structure map (8 types, 47 files), tool/MCP table (Exa, Clay, Apollo, FindyMail, SmartLead), full lead funnel (1849 → 344 verified contacts), key findings from analytics
- Removed Yaroslav references from all files (brief + findymail manifest → "Sales Engineer")
- Next: load 344 contacts to SmartLead; second enrichment pass for 738 unenriched companies

## [2026-05-12] — Russian segment: director name scan expanded candidate pool

**Что сделали:**
- NPI-скан по всем 86 REFERENCE-лабам в NJ/NY/PA — новых русских не нашли
- Обнаружили слепую зону: 580 POL-лабов в NJ/NY/PA не попали в 190 кандидатов из-за фильтра по словам в названии
- Запустили скан имён по всем 665 пропущенным лабам + NPI по 65 лабам в Russian-community городах
- **Нашли 7 новых подтверждённых русскоязычных лаб** которые не были в исходных 190

**Ключевая находка:** GREGORY SHIFRIN MD PC OB GYN (Brooklyn, 276,946 тестов/год) — крупнейшая из найденных, пропустил исходный фильтр

**Итого confirmed:** 13 лаб сохранены в `source-lists/segments/russian_confirmed.csv`
- 6 из прошлой сессии (из 190 кандидатов)
- 7 новых (за пределами 190 кандидатов, найдены через директорские имена)

**Метод верификации:** NPI Registry API → фамилия/имя директора → паттерны русских/армянских фамилий + список русских имён

**Следующие шаги:**
- Расширить гео: Florida (Sunny Isles), California (Sacramento/LA), Illinois
- Добавить паттерны: грузинские фамилии (-shvili/-dze), -in/-ina с поддержкой от русских имён
- Русскоязычные справочники врачей в США (RussianAmericana, community directories)

## [2026-05-12] — Russian segment: FL/CA + community-city expansion

**Что сделали:**
- Скан 86 REFERENCE-лаб NJ/NY/PA + FL/CA расширение → 3 новых (ALAN SEMION, BORIS ZAKS, ALEXANIAN)
- -in/-ina pattern + double signal: 0 STRONG hits на 17 штатах — pattern даёт много false positives (MOUNTAIN, JOAQUIN, MEDINA)
- Strict surname scan (-ov/-ev/-sky/-enko) на 17 штатах вне NJ/NY/PA: 13 кандидатов, NPI verify → 0 русскоязычных (все Polish/Jewish-American Anglicized: Olansky-Alan, Klatsky-Peter, Potozkin-Jerome, Warshawsky-Aaron)
- NPI city-scan по 85 русским community-городам (823 ICP-лаб) → 2 новых: **Alexander Reyzelman** (Folsom CA, 2 лабы), **Ilya Reyter** (Sherman Oaks CA)
- Per-lab NPI в dense cities (Miami/LA/Houston/Chicago) → 1 хит, но ассимилированный (Floyd Schlossberg) — пропуск

**Итог:** 19 confirmed labs (было 16, +3 этой сессии)

**Главный вывод:** surname-only patterns не работают для русскоязычной сегментации — большинство Slavic/Jewish фамилий в США это ассимилированные 2-3 поколения американцев. Critical signal — **русское имя + русская фамилия** (double check). Без double signal hit rate ~0%.

**FL пустышка:** Sunny Isles Beach / Aventura — там стабильные практики (открыты до 2025), наш ICP-фильтр режет по `CRTFCTN_DT >= 2025-01-01`. Чтобы их достать — нужен сырой POS file без date filter (требует ручной навигации на qcor.cms.gov).

**NPI ограничение:** city query capped at 200 orgs → в плотных городах (Miami 48 ICP labs / 0 matched, LA 19/0) coverage частичный.

**Следующие шаги (не выполнено):**
- Скачать сырой POS file → расширить ICP без date filter → перескан Sunny Isles
- Русскоязычные справочники: russianDoctor.com, ZdravoUSA, russian-community-listings

## [2026-05-12] — Russian segment: NPI first-name carpet bomb

**Что сделали:**
- Public Russian doctor directories (rushealthcare.com, russiandoctors.us) — мертвы (DNS unresolved / 403)
- Сменил подход: NPI Registry carpet bomb по 75 русским именам × 21 штат → 1575 API queries, 73841 NPI individual records просканировано
- Cross-reference: NPI individual address → CLIA POS address (state + zip5 + first 30 alnum chars street)
- Double signal: русское имя (strict whitelist) + русская фамилия (-ov/-ev/-sky/-enko/-stein/-berg/-man)
- 31 unique CLIA hit → 29 отфильтровано (hospitals/chains: Quest, LabCorp, Cleveland Clinic, Kaiser, Banner, OHSU, Rush, MultiCare, Quest)

**Итог: +2 confirmed independent POLs**
- Lyudmila Kuznetsova — Pain & Rehab Consultants, Emeryville CA, vol 94129
- Viktoriya Kaganskaya — Nassir Medical Corp Lab, Los Angeles CA, vol 156350

**Всего: 21 confirmed labs** (было 19, +2)

**Боковая intel (не Vivica таргет, но видно):** русскоязычные врачи embedded в крупных системах — Quest MA (Tatiana Achildiev, vol 232k), Cleveland Clinic Avon (Larisa Schwartzman), Westchester Med (Svetlana Krasnokutsky), San Mateo Public Health (Lev Volosskiy). Полезно для общего понимания распределения, но эти лабы уже на собственных enterprise LIMS.

**Метод подтвердил себя:** NPI carpet bomb по first_name даёт надёжный double-signal без шума surname-patterns. Hit rate низкий (2 из 73841 = 0.003%), но zero false positives после фильтра на chains.

**Что осталось не сделано:**
- Сырой POS file без time-фильтра (для устоявшихся практик в Sunny Isles)
- Telegram/VK русскоязычные lab-owner groups (требует ручной координации Andrew)
