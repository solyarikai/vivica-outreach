# Vivica Outreach — рабочий репозиторий

Холодный аутрич для **Vivica.us** — облачная LIMS (система управления данными лабораторий) для клинических лабораторий в США. Работает поверх [gtm-mcp](https://github.com/impecablemee/gtm-mcp).

## Быстрый старт

```bash
# 1. клонируем рядом с gtm-mcp
git clone <этот репо> ~/code/vivica-outreach
cd ~/code/vivica-outreach

# 2. убеждаемся, что gtm-mcp установлен и настроен
# (см. https://github.com/impecablemee/gtm-mcp)

# 3. открываем Claude Code в этой директории
claude

# 4. запускаем первую кампанию — свежесертифицированные CLIA лаборатории
/launch plans/outreach-plan-vivica-clia-fresh.md
```

## Архитектура — кто что делает

```
gtm-mcp                       этот репо
─────────                     ──────────────────
49 инструментов    ◄────────  /launch <план>
13 базовых скиллов              + extensions/
~/.gtm-mcp/state                + reference/
                                + plans/
                                + tracking/
```

**gtm-mcp** делает: поиск через Apollo, классификацию компаний, отправку в SmartLead/GetSales, генерацию писем (12 правил), классификацию ответов, blacklist, хранение state и трассировку runs.

**Этот репо** хранит: специфичные для Vivica знания (3 персоны ICP с ответами на возражения, профили конкурентов, battle cards, кейс Acure, playbooks), CLIA POS-файл как альтернативный источник лидов вместо Apollo, детектор LIMS у конкретной лаборатории, трекинг гипотез.

## Где что лежит

```
extensions/.claude/skills/        # скиллы под Vivica — Claude Code их подхватывает сам
  clia-source/                    # фильтрует POS-файл CMS → ICP-компании (вместо Apollo)
  lims-pain-extractor/            # парсит отзывы конкурентов на G2/Capterra
  lims-detector/                  # определяет, какую LIMS использует конкретная лаба

plans/                            # планы аутрича, каждый идёт в /launch
  outreach-plan-vivica-clia-fresh.md       # главный: свежие CLIA-сертификации
  outreach-plan-vivica-russian-nj.md       # русскоязычные владельцы (NJ)
  outreach-plan-vivica-using-labware.md    # перехват клиентов LabWare
  outreach-plan-vivica-adlm-2026.md        # подготовка к ADLM (июль)

reference/                        # доменные знания, скиллы и планы их читают
  company/                        # что такое Vivica
  icp/                            # 3 персоны с ответами на возражения
  competitors/                    # 8 профилей конкурентов с болями из G2
  battle-cards/                   # матрица конкурент × персона
  case-studies/                   # Acure Reference Lab (NJ)
  playbooks/                      # русский сегмент, миграция в 3 фазы, ADLM

input-data/                       # сырые данные (PII в .gitignore)
  POS_File_CLIA_Q1_2026.csv       # POS-файл CMS (676 тыс лабораторий)

tracking/                         # бизнес-аналитика поверх gtm-mcp
  hypotheses.csv                  # копия Sally Hypothesis dashboard
  decisions-log.md                # почему остановили/масштабировали сегмент
```

## Где живёт состояние

| Что | Где | Почему |
|---|---|---|
| Состояние pipeline, runs, контакты, ответы | `~/.gtm-mcp/projects/vivica/` | gtm-mcp хранит canonical state |
| Планы, ICP, конкуренты, playbooks | этот репо | доменные знания, версионируем |
| POS-файл, списки участников конференций | этот репо (`input-data/`) | исходники |
| Трекинг гипотез | этот репо (`tracking/`) | бизнес-аналитика |

**Никогда не дублируем состояние gtm-mcp в репо.** Репо — это **входные данные и знания**, gtm-mcp — **выполнение и результаты**.

## Что важно знать про продукт (Yana, читай это)

**Vivica** — это облачная LIMS (Laboratory Information Management System). Она нужна клиническим лабораториям, чтобы вести образцы, тесты, результаты, billing. Это не AI-агентство и не автоматизация чего попало.

**Один активный клиент** — Acure Reference Lab в Нью-Джерси, оборот $100M+. С ними есть совместное опубликованное исследование с KOL — можно упоминать в письмах открыто.

**Какие лаборатории мы НЕ таргетим:**
- Госпитальные (Hospital Labs) — заперты в экосистемах Epic/Cerner, интеграция стоит безумно дорого
- Лаборатории с CLIA Waiver — им LIMS не нужна, они делают только базовые тесты

**Какие таргетим:**
- POL (Physician Office Lab) — врач с маленькой лабой при клинике
- PSC (Patient Service Center) — независимые/walk-in лабы вроде Invitro
- Reference Labs — принимают заказы от других лаб, делают сложные анализы

**Главное возражение** на любом холодном письме: «менять систему — это 6-12 месяцев боли». Мы отбиваем это three-phase migration playbook (зеркалируем текущую LIMS → запускаем параллельно через прокси → выводим старую систему). Подробности в `reference/playbooks/three-phase-migration.md`.

**Русскоязычный сегмент** — отдельная история. Эндрю ведёт. Кейс in vitro (2000 локаций, 1М тестов в день) — рассказываем целиком только русскоязычным владельцам. Для US-лаб in vitro анонимизируем («крупный международный референс-лаб»), потому что российские корни могут вызвать вопросы по HIPAA/безопасности данных. Подробности в `reference/playbooks/russian-segment.md`.

**Конкуренты, которых мы знаем (8 штук):**
- Топ премиум: LabWare, LabVantage
- Среднее: Clinisys (бывший Sunquest), CrelioHealth, LigoLab
- Современные cloud-native: QBench, CloudLIMS
- Европейский: lims.net (он же JTO в чате с Петром)

## Команда

- **Chris Hilinsky** — co-founder Vivica, US-рынок, английский LinkedIn
- **Andrew** — русскоязычный сегмент
- **Evgenia Farikh** — опционально третий LinkedIn
- **Петр (Sally)** — стратегия со стороны агентства
- **Яна (Sally)** — операционка кампаний, ежедневный pipeline
- **Ринат (Sally)** — лид агентства

## Если что-то непонятно

Сначала смотри `reference/`. Если там нет — `plans/`. Если совсем непонятно — пишешь в общий чат «Life Data Lab <> Sally AI Lead Generation».
