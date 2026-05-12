# Segments — Reference Labs Pipeline

Финальные сегменты для outreach-кампании по reference-лабораториям (CLIA Q1 2026).

Этот README — единая точка входа: откуда взялись файлы, как читать тиры, что куда грузить.

---

## TL;DR

- **Это 🟧 CMS-enrichment воронка** (наша), не 🟦 HOT-универс Петра. См. [project_two_lead_pools](../../../.claude/projects/-Users-user-vivica-outreach/memory/project_two_lead_pools.md). Не мерджить.
- Источник: **1849 reference-лабораторий из CLIA Q1 2026** → Apollo people → Apollo Reveal → FindyMail double-verify
- Выход: **344 верифицированных контакта на 270 компаниях** (37.8% покрытие CLIA)
- Стоимость: ~$22.70 (~$0.034 за контакт)
- Главный ботлнек: **Apollo покрывает только 41% доменов**, не верификация

---

## Файлы в этой папке

| Файл | Строк | Что это |
|------|-------|---------|
| **`final_contacts_verified.csv`** | 344 | Базовые верифицированные контакты — готовы к SmartLead |
| **`final_contacts_tiered.csv`** | 344 | + колонки `tier`, `score`, `cohort`, `primary_reason` (Петров скоринг) |
| **`final_contacts_scored.csv`** | 344 | + `vivica_score`, `vivica_bucket` (HOT/WARM/COOL/COLD) — **финальный приоритизированный список** |
| `companies_enriched.csv` | 281 | Лаборатории с ≥1 верифицированным контактом |
| `companies_enriched_tiered.csv` | 281 | То же + тиры |
| `companies_not_enriched.csv` | 738 | Лаборатории, требующие других методов enrichment (LinkedIn/Clay) |
| `companies_not_enriched_tiered.csv` | 738 | То же + тиры |
| `bucket_REFERENCE_domains.csv` | 1849 | Исходный bucket reference-доменов |
| `russian_candidates_nj_domains.csv` | 190 | NJ-домены, кандидаты на русскоязычные (для исключения) |
| `russian_confirmed.csv` | 19 | Подтверждённые русскоязычные → blocklist |
| `tier_summary.md` | — | Распределение тиров по всем трём сегментам |
| `apply_tiers.py` | — | Скрипт: тиры Петра → наши выходы |
| `score_contacts.py` | — | Скрипт: собственный Vivica-fit скоринг (6 сигналов из CLIA bucket + persona + tier) |
| `scoring_summary.md` | — | Распределение по bucket'ам, топ-20, bottom-10, breakdown по facility_type |

---

## Схема `final_contacts_verified.csv`

```
src_name, src_domain, src_clia, persona, contact_first_name, contact_full_name,
contact_email, contact_title, contact_linkedin, source
```

- `persona` — `ceo_owner` (64%), `medical_director` (19%), `lab_director` (17%)
- `source` — обычно `apollo+findymail_verified`

## Схема `final_contacts_tiered.csv` (расширенная)

Все колонки выше + **тиры из универса Петра**:

| Колонка | Что |
|---------|-----|
| `tier` | S+ / S / A / B / C / D / E / `—` (нет в универсе Петра) |
| `score` | Числовой скор из Петрового xlsx |
| `cohort` | Группировка (`A_fresh_le_6mo`, etc.) |
| `sources` | Какие источники подтвердили (NPI/CLIA/Medicare) |
| `primary_reason` | Текстовое объяснение скоринга |

---

## Воронка enrichment

| # | Этап | Вход | Выход | Конверсия | Потери |
|---|------|------|-------|-----------|--------|
| 1 | CLIA reference records | — | 1849 | — | — |
| 2 | Domain enrichment (Clay+Exa) | 1849 | 1019 unique доменов | 97.8% | 40 без домена |
| 3 | Apollo people search | 1019 доменов | 1252 контакта (383 домена) | 37.6% hit rate | **636 доменов без контактов** |
| 4 | Apollo Reveal (email by ID) | 1252 | 1033 verified | 82.5% | 219 misses |
| 5 | FindyMail SMTP verify | 1033 | 878 valid | 85.0% | **149 invalid (14.4% bounce)** |
| 6 | FindyMail search на misses | 219 | 1 found | 0.5% | 218 dead |
| 7 | Dedup по email | 879 | **344 unique** | 39.1% | 535 дублей (chain locations) |
| 8 | Unique companies | — | 270 | — | — |
| 9 | CLIA records covered | 698 / 1849 | — | **37.8%** | 1151 не охвачены |

Полная аналитика и стоимость по этапам:
[../enrichment-runs/2026-05-11_reference-1849_findymail-email/analytics.md](../enrichment-runs/2026-05-11_reference-1849_findymail-email/analytics.md)

Run manifest (как воспроизвести):
[../enrichment-runs/2026-05-11_reference-1849_findymail-email/manifest.md](../enrichment-runs/2026-05-11_reference-1849_findymail-email/manifest.md)

---

## Сегментация и приоритизация

Тиры подтягиваются из универса Петра ([../lab-universe-petr-2026-05/lab-universe-2026-05.xlsx](../lab-universe-petr-2026-05/lab-universe-2026-05.xlsx)) через `apply_tiers.py`.

### Verified contacts (344) — распределение

| Tier | Count | % | Что значит |
|------|-------|---|-----------|
| S+ | 1 | 0.3% | Топ-приоритет |
| S | 9 | 2.6% | Hot |
| B | 1 | 0.3% | Medium |
| — | 333 | **96.8%** | **Не в универсе Петра — тир неизвестен** |

> 🔑 **Главное**: 96.8% наших верифицированных контактов — это лабы, которых **нет** в Петровом универсе. Это не значит «плохие», это значит «другой пул». Скоринг для них нужен свой (или принять, что идём вслепую по CLIA-сигналу).

### Приоритизированный pipeline для unenriched (738)

| Priority | Tier | Count | Action |
|----------|------|-------|--------|
| HOT | S+/S | 14 | LinkedIn Sales Nav / Clay следующим заходом |
| MEDIUM | A/B | 3 | Вторая волна |
| LOW | C | 0 | Только если квота не закрылась |
| SKIP | D/E | 1 | Blocklist |
| Unknown | — | 720 | Нет в универсе Петра — нужно верифицировать вручную |

Полная разбивка: [tier_summary.md](tier_summary.md)

---

## Ключевые инсайты

1. **Apollo `email_status=verified` врёт на 14.4%** — без FindyMail double-check нельзя, угробим sender reputation
2. **Apollo coverage — главный ботлнек**: 636 из 1019 доменов (62%) не имеют ни одного контакта в Apollo. Нужны LinkedIn / Clay / ручной скрейпинг
3. **3-persona ICP coverage редкий**: только 9 из 270 компаний имеют все три персоны. 76% — одна персона на компанию
4. **FindyMail name-search на Apollo misses мёртв**: 1/219 (0.5%). Не повторять
5. **Покрытие универса Петра почти нулевое (3.2%)**: наша CMS-воронка и Петров универс — почти непересекающиеся пулы

---

## Что грузить в SmartLead

- **Базовая кампания**: `final_contacts_verified.csv` (344) — всё, что верифицировано
- **Приоритетная подкампания**: фильтр `final_contacts_tiered.csv` по `tier IN ('S+', 'S', 'B')` (11 контактов с известным тиром)
- **Blocklist**: `russian_confirmed.csv` (19) — исключить до загрузки

---

## Следующие шаги

1. ✅ `final_contacts_verified.csv` → SmartLead campaign
2. 🔄 Прогнать 738 unenriched через LinkedIn Sales Nav / Clay (есть `company_linkedin_url` из `2026-05-10_all-2039_exa`)
3. ❌ Не использовать FindyMail name-search на Apollo misses — Apollo Reveal by ID единственный рабочий путь
4. 🔍 Решить, что делать с 333 контактами вне универса Петра — построить свой скоринг или принять CLIA-only приоритет
