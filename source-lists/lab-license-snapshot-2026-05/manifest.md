# Lab License Snapshot — May 2026

**Google Sheet:** https://docs.google.com/spreadsheets/d/1QLbbSA0aCenDd1060e8Z8KYzfmAk2GscUKaPOeB0J2M/edit?gid=0#gid=0

**Built:** 2026-05-07 · **Operator:** Petr · **Tool:** magnum-opus / `tasks/vivica`

---

## Что это

Снэпшот всех клинических лабораторий США, которые **получили лицензию за последние 6 месяцев** (с 2025-11-07). Логика: недавно открытая лаба = скорее всего ещё без LIMS или в активном поиске. Это наш главный входящий сигнал на «fresh» сегмент.

---

## Источники данных

Пайплайн тянет из 13 источников и мержит всё в один шит:

| Группа | Источники |
|---|---|
| Федеральные | CLIA bulk (CMS), NPPES NPI Registry |
| Штаты | NY, CA, FL, WA, PA, RI, MD |
| Аккредитационные тела | COLA, CAP, Joint Commission, AABB |

Каждый источник — отдельный таб `*_raw` в шите. Мерж по CLIA number + NPI (дедупликация).

---

## Структура шита

| Таб | Что |
|---|---|
| `hot_leads_vivica` | **Целевые лиды** — прошли все фильтры ICP. Отсюда работаем. |
| `merged` | Все лабы после мержа и дедупа, без фильтрации |
| `clia_raw`, `nppes_raw`, `state_*_raw`, `accred_*_raw` | Сырые данные по каждому источнику |
| `run_log` | Статус каждого источника: строк, время, ошибки |

---

## Фильтр горячих лидов (таб `hot_leads_vivica`)

Лаба попадает, если **все** условия выполнены:

1. `effective_date >= 2025-11-07` — лицензия выдана за последние 6 месяцев
2. `certificate_type` = `Compliance` или `Accreditation` — не waived/PPM (реальный clinical workflow)
3. `complexity_level` = `moderate` или `high` (или `null` — принимается при compliance/accreditation)
4. `provider_category` **не** hospital / hospital_lab / critical_access_hospital
5. `provider_category` **в** target-категориях: `independent`, `physician_office`, `reference`, `patient_service_center`, `community_clinic`, `other`

---

## Колонки (LabRecord schema)

`source` · `source_id` · `clia_number` · `npi` · `name` · `dba` · `address` · `city` · `state` · `zip` · `phone` · `owner_name` · `lab_director` · `certificate_type` · `complexity_level` · `specialties` · `provider_category` · `effective_date` · `expiration_date` · `accreditations` · `state_license_id` · `taxonomy` · `first_seen_date` · `raw_url` · `dup_keys`

---

## Известные ограничения

- **Сетевые лабы не отфильтрованы** — `provider_category = reference` включает крупные сети (Quest, LabCorp, BioReference и т.д.). У них всё налажено, Vivica не нужна. Нужен ручной QA или блэклист по `owner_name`.
- `complexity_level` часто `null` для CLIA-источника — CLIA API не возвращает specialty codes надёжно. Лабы с `null` оставлены, если cert_type уже говорит о сложности.
- `provider_category = other` — включён для ручного просмотра, не все релевантны.
- Охват по штатам неполный — только 7 штатов с парсерами. Остальные — только через федеральные CLIA/NPPES.

---

## Связанные файлы

- [[outreach-plan-vivica-clia-fresh]] — план работы с этим сегментом
- [[lab-universe-2026-05]] — более широкий датасет (8,256 лаб всех возрастов, от Петра)
- `source-lists/clia-q1-2026/` — CMS CLIA Q1 2026, исходный сырой файл
