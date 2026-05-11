# Глоссарий — проект Vivica Outreach

Единый источник правды по всем терминам проекта. Если термин используется в скиллах, планах или reference-материалах — он определён здесь. Когда что-то непонятно — этот файл первый, куда смотреть.

Структура:
- [Продукт и доменная область](#продукт-и-доменная-область) — что такое Vivica и в каком мире она живёт
- [ICP и сегментация](#icp-и-сегментация) — на кого таргетим
- [Конкуренты](#конкуренты) — 8 LIMS-вендоров
- [Источники данных](#источники-данных) — POS-файл CMS, CLIA-коды и т.д.
- [Pipeline и инструменты](#pipeline-и-инструменты) — gtm-mcp, MCP-серверы, Apollo, SmartLead, GetSales
- [Скиллы и этот репо](#скиллы-и-этот-репо) — что делает каждый компонент
- [Процессы и playbooks](#процессы-и-playbooks) — three-phase migration и др.
- [Команда и люди](#команда-и-люди)
- [События и дедлайны](#события-и-дедлайны) — ADLM 2026
- [Автономия агента](#автономия-агента) — что AI-агент может делать сам, что — только с подтверждением

---

## Продукт и доменная область

### Vivica
Продукт, для которого мы делаем аутрич. Облачная **LIMS** для клинических лабораторий в США. Сайт: vivica.us. На момент старта — один активный клиент (Acure Reference Lab, NJ, оборот $100M+) и один ушедший (лаба закрылась, не из-за продукта). Есть совместное опубликованное исследование с KOL — можно открыто упоминать в холодных письмах.

### LIMS (Laboratory Information Management System)
Система управления данными лаборатории. Управляет образцами, тестами, результатами, биллингом, compliance. Категория, в которой Vivica конкурирует. **Не путать с LIS** (Lab Information System), хотя часть вендоров совмещает обе функции.

### LIS (Laboratory Information System)
Близкая к LIMS система; LIS больше про клинические результаты, LIMS — про образцы/inventory/workflow. Некоторые вендоры (LigoLab, CrelioHealth) совмещают.

> **Терминологическая ловушка — читай внимательно**: в outreach-контексте этого проекта, когда говорим про "текущую систему клиента", которую мы зеркалируем/проксируем/выводим — **это почти всегда LIMS**, не LIS. Потому что Vivica — это LIMS, и конкурируем мы с LIMS-вендорами (LabWare, Clinisys, QBench и т.д.). В ранних черновиках этого проекта я ошибочно использовал "LIS" в описаниях миграции; это исправлено. Используем "LIMS" для замещаемой системы. "LIS" используем только когда: (1) описываем вендора, который реально combined LIS+LIMS типа LigoLab/CrelioHealth, (2) обсуждаем интеграцию приборов через LIS как реальный компонент стека клиента, (3) описываем сам продукт Vivica как "combined LIS+LIMS functionality".

### Клиническая лаборатория
Лаба, которая делает тесты на человеческих биообразцах для диагностики/лечения. Регулируется CLIA. Отличается от **исследовательских лабораторий** (это не наш рынок).

### CLIA (Clinical Laboratory Improvement Amendments)
Федеральный закон США, регулирующий клинические лаборатории. Каждая клин-лаба обязана иметь CLIA-сертификат. Администрируется CMS.

### Типы CLIA-сертификатов
- **Compliance** (`CRTFCT_TYPE_CD = 1`) — полный режим инспекций. Vivica таргетит.
- **Waiver** (`= 2`) — только простые тесты. LIMS не нужна. Пропускаем.
- **PPMP** (`= 3`) — Provider-Performed Microscopy Procedures. Нишево.
- **Accreditation** (`= 4`) — аккредитация CAP, AABB и т.п. Тоже таргетим.
- **Registration** (`= 9`) — временный, пока подают документы. Пропускаем.

### CMS (Centers for Medicare & Medicaid Services)
Федеральное агентство США. Публикует CLIA POS-файл квартально — canonical-реестр всех CLIA-сертифицированных лаб.

### CAP (College of American Pathologists)
Аккредитующий орган для клин-лаб. Лабы с CAP-аккредитацией имеют `CRTFCT_TYPE_CD = 4`.

### HIPAA (Health Insurance Portability and Accountability Act)
Закон США о приватности и безопасности медицинских данных. **Важно для русскоязычного сегмента**: акцент на российских корнях in-vitro кейса вызывает у US-лаб опасения по HIPAA/безопасности данных.

### HL7 / FHIR
Стандарты обмена медицинскими данными. LIMS обязана уметь говорить с госпитальными системами через эти стандарты. Часто упоминается как боль в отзывах ("brittle HL7 integration").

### EMR / EHR
Electronic Medical Record / Electronic Health Record. Клинический софт госпиталя. Epic и Cerner — доминирующие вендоры. Лабы внутри госпиталей заперты в их лаб-модули, поэтому **госпитальные лабы пропускаем**.

### Epic / Cerner
Доминирующие EMR-вендоры в США. Epic "Beaker" и Cerner "PathNet" — их лаб-модули. Если лаба внутри Epic/Cerner-госпиталя, сменить LIMS практически невозможно — стоимость интеграции переломит всё. Пропускаем.

### KOL (Key Opinion Leader)
Признанный авторитет в области. У Vivica есть совместное исследование с KOL через Acure — социальное доказательство для холодных писем.

---

## ICP и сегментация

### ICP (Ideal Customer Profile)
Сегмент рынка, наиболее склонный к покупке. ICP Vivica зафиксирована в Sally ICP Google Sheet и в наших файлах `reference/icp/`.

### Persona (персона)
Конкретная роль ЛПР внутри ICP. У Vivica три:

- **CEO / Owner** — владелец небольшой POL/PSC. Главные возражения: ROI vs стоимость, "у нас и так нормально".
- **Lab Director / Manager** — оперативный руководитель лабы. Главные возражения: обучение персонала, "наша система работает".
- **Medical Director** — клинический авторитет. Главные возражения: соответствие compliance, "системы упрощают клинические данные".

### POL (Physician Office Lab)
Лаба внутри врачебного офиса. CMS-код `GNRL_FAC_TYPE_CD = 21`. Самый большой бакет ICP (5 745 из 9 193 в Q1 2026 файле). Главный таргет.

### PSC (Patient Service Center)
Walk-in пункт сбора или независимый диагностический центр. Аналог российского "Инвитро". CMS-коды `GNRL_FAC_TYPE_CD = 03` (ancillary test site) и т.п.

### Reference Lab
Лаба, которая принимает работу от других лаб и делает сложные/специализированные тесты. CMS-код `GNRL_FAC_TYPE_CD = 15` (independent). Высокий объём тестов. Премиум-таргет.

### Госпитальная лаба
Лаба внутри госпиталя. CMS-код `GNRL_FAC_TYPE_CD = 14`. **Исключаем** из-за Epic/Cerner lock-in.

### `HOSP_LAB_EXCPTN_SW` (флаг госпитальной лабы)
Поле POS-файла CMS. `Y` = госпитальная, `N` = независимая. Фильтруем по `N`.

### CLIA Waiver лаба
Лаба с `CRTFCT_TYPE_CD = 2`. Делает только простейшие тесты. LIMS не нужна. **Исключаем.**

### "Recently CLIA-certified" (свежесертифицированная)
Триггерный сегмент. Лаба с `CRTFCTN_DT >= 2025-01-01`. Логика: лаба, которая только получила сертификат, ещё не закопалась в LIMS, поэтому цикл продажи короче.

### Русскоязычный сегмент
Владельцы лаб, говорящие по-русски, в основном в NJ/NY/PA по заметке Эндрю с кик-офф звонка. Подход отдельный — ведёт Эндрю, скрипты на русском, in-vitro кейс целиком.

### Самопис (custom self-hosted)
По заметке Эндрю: 3-5 известных лаб используют самописную LIMS, которую поддерживает контрактный разработчик за ~$800/месяц. Другая ценностная модель ("профессиональная облачная LIMS без необходимости поддерживать").

### Buying trigger (триггер покупки)
Внешнее событие, которое делает лабу активным покупателем. Примеры:
- Свежесертифицированная по CLIA (самый сильный)
- Расширение test menu (вакансии)
- Найм нового Lab Director
- Уход от конкурента (отзывы на G2 про миграцию)
- M&A (консолидация мульти-сайтов)

### Objection handling (отбивка возражений)
Заранее подготовленные ответы на самые частые возражения по персоне. Живёт в `reference/icp/persona-*.md`. Три универсальных возражения:
1. "Нас и так устраивает" → отвечаем three-phase migration
2. "Сменить систему — это 6-12 месяцев боли" → mirror→proxy→decommission
3. "Нас беспокоит безопасность данных" → особо актуально, когда упоминаем in-vitro кейс не русскоязычной лабе

---

## Конкуренты

8 LIMS-вендоров, которых отслеживаем. Slug'и совпадают с именами файлов в `lims-pain-extractor`.

### LabWare (`labware`)
Глобальный лидер рынка, 3000+ клиентов (NIH, GSK, Pfizer). Сильнейший в pharma/biotech. G2: 4.5/5 на 100+ отзывов. Типичные боли: сложность интеграций, нагрузка по кастомизации.

### LabVantage (`labvantage`)
Принадлежит The Chatterjee Group. ~33% pharma в отзывах. G2: 3.8/5. Типичная боль: кастомизация отчётов (жалобы на BO/Crystal).

### QBench (`qbench`)
Современная cloud-native LIMS, 130+ G2-отзывов на 4.5/5. Multi-vertical. Сильнейший конкурент Vivica по "modern UX" оси. Типичная боль: масштабирование на high-volume клинические workflows.

### CrelioHealth (`creliohealth`)
Объединённая LIS+LIMS SaaS с прозрачным tier-pricing. HQ в Индии, популярна в mid-market диагностических лабах. Типичная боль: фрикционы при US-деплое.

### LigoLab (`ligolab`)
End-to-end LIS+LIMS+RCM (revenue cycle management) для клинических/anatomic-pathology/outreach лаб. Типичная боль: сроки внедрения, on-prem сложность.

### Clinisys (`clinisys`)
Инкумбент (бывший Sunquest/Horizon). "Безопасный enterprise" выбор. Типичная боль: legacy UX, медленная модернизация, vendor lock-in.

### CloudLIMS (`cloudlims`)
Pure-SaaS прямой конкурент Vivica по оси "low IT, low upfront". Типичная боль: ограниченная кастомизация vs enterprise-нужды.

### lims.net / LiMSEO (`lims_net`)
Также называется **JTO** в Telegram-чате Петра. Французского происхождения (Locasoft). Ограниченное распространение в США. Полезен для labs в NJ с европейским tech-stack'ом.

### Sapiens / Sapio
Упоминался один раз как конкурент. Не входит в активную восьмёрку. Возможно, добавим позже.

### Orchard / PathNet
Упоминались в раннем обсуждении. **Orchard** — реальный конкурент LIMS. **PathNet** — это лаб-модуль Cerner, входит в "Cerner exclusion", не отдельный таргет.

---

## Источники данных

### POS-файл (Provider of Services file)
CSV-файл, который CMS публикует квартально. Содержит каждую CLIA-сертифицированную лабу в США. Наш Q1 2026 файл — 676 051 строка. Скачивается с <https://qcor.cms.gov> через bulk export.

### Поля POS-файла, которые мы используем

| Поле | Смысл | Как используем |
|---|---|---|
| `FAC_NAME` | Имя лабы | Display name |
| `ST_ADR`, `CITY_NAME`, `STATE_CD`, `ZIP_CD` | Адрес | Обязателен (биообразцы) |
| `PHNE_NUM` | Телефон | Контактируемость |
| `CRTFCT_TYPE_CD` | Тип сертификата | Фильтр на 1 или 4 |
| `CRTFCTN_DT` | Дата сертификации | Триггер "недавно сертифицирована" |
| `PGM_TRMNTN_CD` | Статус активности | Фильтр на '00' (активна) |
| `HOSP_LAB_EXCPTN_SW` | Флаг госпитальной | Фильтр на 'N' |
| `GNRL_FAC_TYPE_CD` | Тип учреждения | **Главный сегментатор** (POL/PSC/REFERENCE) |
| `LAB_SITE_CNT` | Кол-во сайтов | Мульти-сайт |
| `FORM_116_TEST_VOL_CNT` | Объём тестов в год | Размер лабы |
| `CLIA_LAB_CLASSIFICATION_CD_1..10` | Коды специализации | **Почти всегда пустые на практике** — только бонусный сигнал |
| `PRVDR_NUM` | CLIA-номер | Уникальный ID |

### CLIA classification codes (`CLIA_LAB_CLASSIFICATION_CD_*`)
Коды специализации по 42 CFR Part 493 (например, 100=histopathology, 250=molecular, 800=toxicology). **Важная оговорка**: эти поля почти всегда заполнены `00` (специализация не указана) у свежесертифицированных лаб. Только ~1% строк POS-файла имеют осмысленные коды специализации. **Специализацию надо подтягивать downstream через скрейп сайтов, а не из CMS.**

### `GNRL_FAC_TYPE_CD` (general facility type code)
**Авторитетный** сегментатор. Документирован в layout PDF от CMS (сентябрь 2022). 29 значений; мы маппим их в 5 бакетов Vivica (POL/PSC/REFERENCE/UNSUITABLE/OTHER).

### QCOR (Quality, Certification & Oversight Reports)
Портал CMS на <https://qcor.cms.gov>. Откуда скачивается POS-файл. Также имеет UI для поиска по конкретным лабам.

### Apollo
Платформа лидов. Используется downstream от `clia-source` для people enrichment (POS-файл содержит компании, но не людей/email). По заметкам Сони: 1 keyword на запрос даёт 7× больше уникальных результатов; +45 click-трюк для расширения страниц; exclusion lists; lookalike-поиск.

### Apollo lookalike
Фича Apollo — даёшь известно хорошую компанию, возвращает похожие. По заметке Сони используется для поиска похожих лаб.

### Clay
Платформа enrichment. Используется агентством для AI-обогащения. Включает Claygent (LLM-агент внутри Clay) и HTTP API + webhooks. **Не в нашем pipeline** (мы используем Apollo для people enrichment), но упомянута в стеке агентства.

### Crona
AI enrichment-инструмент, упомянут в транскриптах. Часть стека агентства вместе с Clay.

### NPI (National Provider Identifier)
ID медработника в США. Упоминался в раннем обсуждении как альтернативный источник. Не используется (CLIA POS более релевантен для лаб).

### PubMed / RapidAPI
Упоминались как research-источники в раннем обсуждении. Не в текущем pipeline.

### Sally Hypothesis dashboard
Google Sheet агентства, отслеживает какие сегменты × гипотезы тестируются. Зеркалится в `tracking/hypotheses.csv`.

### Vivica ICP Google Sheet
Рабочий sheet команды Sally с персонами + возражениями + ответами + KPI. Источник правды для `reference/icp/persona-*.md`.

---

## Pipeline и инструменты

### gtm-mcp
Существующий production-grade outreach-MCP команды на <https://github.com/impecablemee/gtm-mcp>. **49 инструментов, 13 базовых скиллов, единая команда `/launch`.** Владеет всем execution-слоем. Мы пишем расширения сверху.

### MCP (Model Context Protocol)
Стандарт Anthropic для подключения LLM к инструментам/данным. Реализуется как серверы (например, gtm-mcp). Claude Code, Codex CLI, Cursor, Antigravity все поддерживают MCP.

### MCP server
Backend, экспонирующий набор инструментов MCP-aware клиенту. Примеры:
- **gtm-mcp** — наш основной, кастомный для аутрича
- **Smartlead MCP** ([LeadMagic/smartlead-mcp-server](https://github.com/LeadMagic/smartlead-mcp-server)) — 116+ инструментов
- **Apollo MCP** ([Chainscore/apollo-io-mcp](https://github.com/Chainscore/apollo-io-mcp)) — 27 инструментов
- **Notion / Linear / Supabase / GitHub / Miro** — третье-сторонние MCP, доступные

### Agent skill / Skill
Самостоятельный capability-folder с `SKILL.md` + scripts + references. Читается Claude Code, Codex, Antigravity. Стандарт на <https://github.com/anthropics/skills>. Auto-discover из `.claude/skills/`.

### `SKILL.md`
Frontmatter-файл, описывающий один скилл: `name`, `description`, тело с workflow и output. Должен быть на английском (стандарт Anthropic).

### `README.ru.md`
Русскоязычный компаньон к каждому `SKILL.md`. Чтобы Яна и команда могли понять без английского. Лежит рядом с SKILL.md.

### `/launch` команда
Главная точка входа gtm-mcp. Три режима:
1. **Fresh** — новый проект, новый offer, новый ICP
2. **New campaign in existing project** — тот же проект, новый сегмент
3. **Append to existing campaign** — добавить лидов в работающую кампанию

### Pipeline state
Постоянное состояние gtm-mcp в `~/.gtm-mcp/projects/<slug>/`. Содержит `project.yaml`, `state.yaml`, `contacts.json`, `runs/run-N.json`, `campaigns/<slug>/`. **Никогда не дублируем это в репо** — репо хранит входы и знания, gtm-mcp владеет execution и state.

### `filter_intelligence.json`
Файл cross-run обучения в `~/.gtm-mcp/filter_intelligence.json`. gtm-mcp трекает quality scores ключевых слов между runs — слова, давшие плохих лидов, в следующий раз получают меньший вес.

### GOD_SEQUENCE / 12-rule email sequence
Скилл `email-sequence` в gtm-mcp применяет 12 правил для генерации копирайта. Используется downstream от любого сегмента, который мы делаем.

### `linkedin-sequence` (414 flows)
LinkedIn-sequence скилл gtm-mcp. 414 готовых flow. Используется через GetSales.

### `reply-classification` (3-tier funnel)
Reply handler gtm-mcp. Tier 1: regex (бесплатно). Tier 2: keywords (бесплатно). Tier 3: LLM (дёшево). Раскладывает входящие ответы на interested / not-interested / out-of-office / etc.

### Cost gating
Правило gtm-mcp: **никогда не тратим Apollo-кредиты (или любые платные API) без явного подтверждения пользователя**. Соблюдаем это правило во всех наших расширениях.

### Blacklist
Дедуп gtm-mcp по cleaned domain. Инструменты `blacklist_check`, `blacklist_add`, `blacklist_import`. Чтобы не контактировать один домен дважды между runs.

### Cleaned domain
Домен после удаления `www.`, mailto:, параметров и т.п. Canonical key для дедупа компаний.

### SmartLead
Платформа отправки email. gtm-mcp использует для cold-email кампаний. Никогда не пушим в SmartLead без подтверждения (отправка реальным людям).

### GetSales
Платформа автоматизации LinkedIn. gtm-mcp использует для LinkedIn flows. Внутри есть SSI (Social Selling Index) калькулятор — по обучению Софьи.

### Sender Profile (GetSales)
LinkedIn-аккаунт, настроенный в GetSales. Несколько sender-профилей могут ротироваться, чтобы распределять объём отправки — по обучению Софьи.

### SSI (Social Selling Index)
LinkedIn-метрика. У GetSales есть калькулятор. Выше SSI = лучше доставляемость.

### Antigravity / Claude Code / Codex CLI / Cursor
MCP-aware AI dev-окружения. Скиллы должны работать кросс-платформенно (стандарт Agent Skills гарантирует это).

---

## Скиллы и этот репо

### `vivica-outreach` репо
Git-репозиторий проекта. Содержит plans, reference, extensions, input-data, tracking. Версионируется в git.

### `extensions/.claude/skills/`
Где живут наши 3 Vivica-specific скилла. Auto-discover'ится Claude Code при работе в этом репо.

### Скилл `clia-source`
Скилл #1. Фильтрует POS-файл CMS (676k строк) в ICP-компании Vivica (~9k). Выдаёт master JSON + per-bucket CSV в формате gtm-mcp проекта. **Заменяет** Apollo-поиск компаний для лаб-вертикали (Apollo не индексирует CLIA).

### Скилл `lims-pain-extractor`
Скилл #2. Строит корпус болей конкурентных LIMS, парсит G2/Capterra/SourceForge/ITQlick/TrustRadius. Выдаёт структурированные boли (тема + count + intensity + ≤15-словная цитата + source URL) по вендору. Кормит `email-sequence` для competitor-conquest sequence.

### Скилл `lims-detector`
Скилл #3. Детектит, какую LIMS использует конкретная лаба. Сигналы: iframe src на пациентском портале, JS bundle URLs, DNS CNAME на `results.<domain>` / `portal.<domain>`, язык вакансий. Выдаёт поле `current_lims` по компании.

### Директория `reference/`
Доменные знания в репо: ICP персоны, профили конкурентов, battle cards, case studies, playbooks, vivica-intel. Читается скиллами и планами.

### Директория `plans/`
Outreach-планы, по одному на кампанию. Каждый идёт в `/launch`. Образец — `outreach-plan-fintech.md` из gtm-mcp (~400 строк, 3 sequences).

### Директория `input-data/`
Сырые входы: POS-файл CSV, список ADLM attendees, скрейп HTML и т.д. В основном gitignored если PII.

### Директория `tracking/`
Бизнес-аналитика поверх runs gtm-mcp. Содержит `hypotheses.csv` (зеркалит Sally Hypothesis dashboard) и `decisions-log.md`.

### Battle card
Документ для одной персоны × одного конкурента. Объединяет: топ-возражения персоны (из ICP-таблицы) + топ-боли конкурента (из `lims-pain-extractor`) + правильный ответ Vivica. Живёт в `reference/battle-cards/<competitor>_x_<persona>.md`.

### Профиль конкурента
Документ по одному конкуренту (например, `reference/competitors/labware.md`). Содержит: позицию на рынке, корпус болей из `lims-pain-extractor`, внутренние заметки, миграционный угол.

### Three-phase migration framework (миграция в 3 фазы)
Универсальный ответ Vivica на "сменить — слишком рискованно":
1. **Mirror** — зеркалируем текущую конфигурацию LIS в Vivica (параллельная установка, без disruption)
2. **Proxy** — прогоняем live-workflows через Vivica параллельно с legacy (валидируем end-to-end)
3. **Decommission** — выводим legacy-компоненты постепенно под мониторингом

Живёт в `reference/playbooks/three-phase-migration.md`.

### Russian segment playbook
Правила работы с русскоязычным аутричем: ведёт Эндрю, скрипты на русском, in-vitro кейс целиком ОК для русскоязычных, **анонимизируем in-vitro для не-русскоязычных лаб**. Живёт в `reference/playbooks/russian-segment.md`.

### Acure case study
Флагманский референс-клиент Vivica. Acure Reference Lab в NJ, оборот $100M+. Совместное опубликованное исследование с KOL — можно использовать в письмах. Живёт в `reference/case-studies/acure-reference-lab-nj.md`.

### Outreach plan
Markdown-файл в `plans/`, описывающий одну кампанию end-to-end: ICP, сегменты, sequences, расписание, KPI. Образец — `outreach-plan-fintech.md` из gtm-mcp (447 строк, 3 sequences). Идёт в `/launch`.

### Hypothesis tracking (трекинг гипотез)
Каждая кампания тестирует гипотезу ("recently CLIA + русскоязычный даёт лучше reply rate, чем просто recently CLIA"). Трекается в `tracking/hypotheses.csv`, зеркалит dashboard Sally.

---

## Процессы и playbooks

### Cold outreach / Cold email (холодный аутрич)
Отправка email/LinkedIn-сообщений людям, которые не просили, в надежде начать sales-разговор.

### Sequence
Серия из 4-5 писем (или LinkedIn-сообщений) по расписанию (обычно 3-4 дня между). Стандарт индустрии: follow-ups дают ~42% всех ответов.

### Tier 1 / Tier 2 персонализация
- **Tier 1**: один шаблон на весь сегмент (только `{firstName}` + название сегмента)
- **Tier 2**: per-person research (текущая LIMS, недавние триггеры, специализация)
- email-sequence в gtm-mcp делает Tier 2 автоматически, если мы дадим обогащённые данные

### Volume sequence vs Fresh sequence vs Competitor-conquest
Три типа sequence из `outreach-plan-fintech.md` gtm-mcp:
- **Volume**: широкая ICP, общая боль, низкая персонализация, большая аудитория
- **Fresh**: на основе триггера (свежее финансирование, свежая сертификация). Самый высокий reply rate.
- **Competitor-conquest**: таргет на известных пользователей конкурента X, использует pain corpus

### Reply rate / Open rate / Bounce rate
Стандартные email-метрики. Цели по плану gtm-mcp: open >40%, reply >2%, bounce <2%.

### A/B тест
Два варианта subject line на одной аудитории, проверяем кто лучше. Стандартная практика; email-sequence gtm-mcp поддерживает нативно.

### "Via negativa" квалификация
Философия скилла `company-qualification` gtm-mcp. Вместо "это fit?" пытается **дисквалифицировать**: "есть ли явная причина, почему это НЕ fit?". Точность 97% на 2-pass re-evaluation.

### Apify
Веб-скрейпинг инфраструктура. `scrape_website` и `scrape_batch` gtm-mcp используют Apify proxy для JS-рендеринга и обхода блокировок. Наши `lims-detector` и `lims-pain-extractor` должны использовать тот же Apify-путь, когда работают внутри Claude Code.

---

## Команда и люди

### Petr Nikolaev (Sally / Life Data Lab)
Стратегия со стороны агентства. Написал в Telegram план scope на $500/месяц (image #1). Знает что JTO = lims.net (image #2).

### Yana Arnautova (Sally / Life Data Lab)
Day-to-day оператор и владелец pipeline. Русскоязычная. **Весь проект построен так, чтобы быть запускаемым end-to-end Яной** — отсюда требование двуязычных README и self-explanatory планов.

### Rinat Khatipov (Sally / Life Data Lab)
Лид агентства. Сделал параллель: "делали такое для CRM-проекта — определяли, какую CRM использует компания, потом писали competitor-specific сообщения".

### Chris Hilinsky (Vivica)
Co-founder, US-рынок, английский LinkedIn-аутрич. Источник техники определения LIMS через iframe пациентского портала.

### Andrew (Vivica)
Лид русскоязычного сегмента. Готов платить $100 Amazon gift cards за 30-минутные интервью. Знает 3-5 "самопис"-лаб.

### Evgenia Farikh (Vivica)
Опционально третий LinkedIn-аккаунт.

### Sonya / Sofia (тренировки Sally)
Sonya — тренер по Apollo, Sofia — тренер по GetSales. Источники заметок Apollo (`Apollo.md`) и GetSales (`GetSales.md`).

### Acure Reference Lab
Флагман-клиент Vivica. NJ, оборот $100M+. Совместное опубликованное исследование с KOL.

---

## События и дедлайны

### ADLM 2026
**Критический дедлайн.** Ежегодное собрание AACC. **26-30 июля 2026, Anaheim Convention Center, ~15 000 участников, 850+ exhibitors.** Pre-conference outreach — главный deliverable проекта. На 10 мая 2026 — это ~11 недель.

### Pre-conference outreach
Аутрич к подтверждённым участникам за 4-6 недель до конференции, предложение встречи на стенде или в Анахайме.

### Onsite outreach
Real-time аутрич во время самой конференции. Другая каденция (same-day ответы) и тон (более casual).

### Post-conference follow-up
Аутрич через 1-2 недели после конференции к тем, кто был, но не записался. Триггер-фраза: "видел вас на ADLM".

---

## Автономия агента

Что AI-агент (Claude в Claude Code или любой агент, дёргающий gtm-mcp) **может делать без вопросов** и что требует подтверждения. Критично для того, чтобы Яна могла самостоятельно запускать проект.

### Агент МОЖЕТ делать без вопросов

**Read-only операции:**
- Читать любой файл в `reference/`, `plans/`, `input-data/`, `tracking/`
- Читать состояние gtm-mcp в `~/.gtm-mcp/projects/vivica/`
- Читать прошлые run logs и replies
- Искать по прошлым чатам для контекста

**Работа с CLIA-данными** (бесплатно, без API):
- Запускать `clia-source` фильтр с любой `--since` датой
- Пере-сегментировать POS-файл по любой оси (штат, специальность, тип учреждения)
- Генерировать per-segment CSV
- Кросс-сравнивать `russian_candidates_nj.csv` с input-данными

**Public-web скрейпинг** (бесплатно, без API):
- Запускать `lims-pain-extractor` на G2, Capterra, SourceForge, ITQlick, TrustRadius
- Обновлять corpus болей конкурентов когда устарел
- Запускать `lims-detector` на одном домене или батче
- Перепроверять `current_lims` лабы, когда предыдущая детекция была unknown

**Генерация и поддержка** (бесплатно, без внешних API):
- Генерировать battle cards, комбинируя существующие персоны + corpus болей
- Генерировать профили конкурентов из corpus
- Обновлять reference-доки под последний CMS layout или находки в данных
- Валидировать копирайт-правила (≤15 слов на цитату, ≤1 цитата на источник, никаких текстов песен)
- Переформатировать планы под структуру, ожидаемую gtm-mcp
- Линтить outreach-планы на отсутствующие поля
- Обновлять `tracking/hypotheses.csv` результатами runs

**Git-операции на feature-ветках:**
- Создавать feature-ветки
- Делать коммиты
- Пушить в feature-ветки
- Открывать PR на ревью

### Агент ОБЯЗАН спросить перед

**Тратой денег:**
- Apollo people enrichment (тратит кредиты)
- Apollo company enrichment по домену (тратит кредиты)
- Любой платный API-вызов
- Даже маленькие траты — это hard rule gtm-mcp

**Отправкой реальных сообщений:**
- Push кампаний в SmartLead (отправит реальные письма)
- Push flows в GetSales (отправит LinkedIn-сообщения)
- Добавление лидов в активные кампании
- Что угодно, что попадёт в inbox реального человека

**Деструктивными операциями:**
- Удаление файлов в `reference/`, `plans/`, `tracking/`
- Force-push в main
- Удаление записей из blacklist
- Остановка работающих кампаний посередине

**Высокоставочными интерпретациями:**
- Подтверждение "это русскоязычный владелец" (решает Эндрю, не агент)
- Анонимизация in-vitro кейса (агент применяет правило, но люди проверяют edge-cases)
- Добавление нового конкурента в восьмёрку

### Агент НИКОГДА не делает

- Изменение чужого репо (сам gtm-mcp — только PR'ы)
- Шаринг лидов или PII вне репо проекта
- Цитирование >15 слов из защищённого авторским правом источника
- Использование in-vitro кейса verbatim для не-русскоязычных лаб
- Генерация писем напрямую для отправки (всегда через email-sequence gtm-mcp + ревью человеком)
- Обход cost-gating правила, даже под предлогом срочности

### Поведение по умолчанию при сомнении

**Если непонятно — спроси.** Лучше прервать ради подтверждения, чем потратить кредиты или отправить сообщения неправильно. Это платный клиентский проект; потеря доверия хуже потери времени.

При вопросе будь конкретным:
1. **Что** агент хочет сделать
2. **Почему** (какой триггер / какие данные подтолкнули)
3. **Сколько стоит** (кредиты, объём реальных сообщений, время)
4. **Обратимо ли** (можно ли отменить, если ошибся)

---

## Перекрёстные ссылки

- Архитектурное разделение gtm-mcp и этого репо — см. `README.md`
- История источника данных (POS-файл CMS → ICP) — см. `extensions/.claude/skills/clia-source/SKILL.md`
- Структура corpus'а болей — см. `extensions/.claude/skills/lims-pain-extractor/SKILL.md`
- Детали детекции LIMS — см. `extensions/.claude/skills/lims-detector/SKILL.md`
- Английская версия глоссария — см. `glossary.md`
