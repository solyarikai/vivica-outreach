# lims-detector — определяем какую LIMS использует конкретная лаба

## Зачем

Из заметки Криса с кик-офф звонка:

> Какую LIMS использует лаба — определяется через сайт. Портал пациентов в правом верхнем углу, при входе открывается iframe. Правая кнопка → inspect element → видно хостинг.

Это самый дешёвый и точный способ узнать, против кого мы играем. Как только знаем вендора X — включается вся персонализация:
- цитата боли вендора X из корпуса `lims-pain-extractor`
- battle card по вендору X
- migration framework (mirror→proxy→decommission)
- social proof: «к нам переходили клиенты X, говорят...»

Без этого скилла письмо генерик. С ним — точечное.

## Когда запускать

В стандартном gtm-mcp pipeline:

```
Apollo / clia-source  →  скрейпим сайты  →  qualify
                                                 │
                            ┌────────────────────┤
                            │   ЭТОТ СКИЛЛ       │
                            │   работает здесь   │
                            └────────────────────┘
                                                 │
                                                 ▼
                                            people enrichment
                                                 │
                                                 ▼
                                       email-sequence
                                       (использует определённого вендора)
```

Запускаем на КАЖДОЙ квалифицированной таргет-лабе, не на всех результатах Apollo — каждая компания делает HTTP-запросы.

## Сигналы (по приоритету)

### Сигнал 1: iframe пациентского портала

Кнопка пациентского портала обычно справа сверху на главной. По клику открывается iframe со страницей вендора. `src` атрибут iframe выдаёт вендора:

| Паттерн iframe src | Вендор |
|---|---|
| `*.labware.com/`, `*.labware-online.com/` | LabWare |
| `*.labvantage.com/`, `*.lvportal.com/` | LabVantage |
| `*.qbench.com/`, `portal.qbench.io/` | QBench |
| `*.creliohealth.com/`, `*.creliohealth.in/` | CrelioHealth |
| `*.ligolab.com/` | LigoLab |
| `*.clinisys.com/`, `*.sunquestinfo.com/` | Clinisys (вкл. legacy Sunquest) |
| `*.cloudlims.com/` | CloudLIMS |
| `*.lims.net/`, `*.limseo.eu/` | lims.net / LiMSEO (он же JTO) |

### Сигнал 2: JavaScript бандлы

Если портал — это JS-виджет, а не iframe, то загружаемые скрипты часто содержат имя вендора:

```
<script src="//cdn.qbench.com/widget.js"></script>
```

### Сигнал 3: Поддомен результатов

Лабы часто хостят LIMS на своём поддомене, привязанном (cname) к вендору:

```
results.acmelab.com  →  CNAME  →  acmelab.creliohealth.com
```

DNS-lookup даёт сигнал. Бесплатный DoH провайдер, ключ не нужен.

### Сигнал 4: Вакансии

Если лаба нанимает IT для лаб-системы, вакансия часто называет систему:

> «2+ года администрирования LabWare LIMS»

Скрейпим LinkedIn, Indeed, страницы карьеры. Это медленный fallback — только когда сигналы 1-3 не дают результата.

### Сигнал 5: Самописная LIMS

Из кик-офф звонка (заметка Эндрю):

> 3-5 клиентов используют самописную LIMS — платят $800 разработчику, который пишет и поддерживает. Дёшево, гибко, но не масштабируется.

Если сигналы 1-3 не дают вендора И портал выглядит самописным (нет third-party CDN, кастомный URL на собственном домене лабы) — тегаем `custom_self_hosted`. Value prop для них другой: «профессиональная облачная LIMS без необходимости поддерживать».

## Что на выходе

Скилл обогащает каждую компанию полем `current_lims`:

```json
{
  "name": "ACME Diagnostic Lab",
  "domain": "acmelab.com",
  "current_lims": {
    "vendor": "labware",
    "vendor_display_name": "LabWare LIMS",
    "confidence": 0.92,
    "detected_via": ["iframe_src"],
    "evidence": [...],
    "detected_at": "2026-05-10T14:23:00Z"
  }
}
```

Возможные значения `vendor`:
- Один из 8 вендоров (labware, labvantage, qbench, creliohealth, ligolab, clinisys, cloudlims, lims_net)
- `custom_self_hosted` — самописная
- `unknown` — не определили, на ручную проверку
- `none_detected` — портала нет (мелкие POL без онлайн-присутствия)

## Confidence

| Сигналы | Confidence |
|---|---|
| Только Сигнал 1 | 0.85 |
| Сигналы 1+2 | 0.95 |
| Только Сигнал 2 | 0.65 |
| Только Сигнал 3 | 0.75 |
| Только Сигнал 4 | 0.55 |
| Все четыре | 0.99 |

Порог доверия в email-sequence: `confidence >= 0.7`. Ниже — генерик (без vendor-specific цитаты).

## Pipeline

```
1. Читаем company.domain (если null — пропускаем, не наша задача найти)
2. Ищем страницу пациентского портала:
   GET /patient-portal, /portal, /results, /lab-results
3. Если есть iframe — берём src → паттерны IFRAME_PATTERNS
4. Если есть JS бандлы — паттерны JS_BUNDLE_PATTERNS
5. Если всё ещё неоднозначно — DNS lookup results.<domain>, portal.<domain>
6. Если всё ещё unknown И есть вакансии — парсим
7. Считаем confidence, пишем обратно в company
8. Если unknown — флаг на ручную проверку (по кик-оффу — Эндрю готов
   платить $100 Amazon gift card за 30-мин интервью)
```

## Приватность и rate limiting

- Не больше 3 HTTP запросов на лабу (главная + портал + DNS)
- Не сохраняем скрейп-HTML дольше извлечения LIMS-сигнала
- Уважаем robots.txt
- Используем Apify прокси gtm-mcp когда доступно

## Запуск

```bash
# Один домен
python scripts/detect_lims.py --domain acmelab.com

# Батч по списку
python scripts/detect_lims.py --batch ~/.gtm-mcp/projects/vivica/qualified.json

# Только перепроверить unknown
python scripts/detect_lims.py --batch <file> --only-unknown
```

## Чего скилл НЕ делает

- НЕ ищет людей/email (это Apollo через gtm-mcp)
- НЕ пишет письма (это `email-sequence` после того как мы определили вендора)
- НЕ парсит G2 (это `lims-pain-extractor`)
- НЕ определяет специализацию лабы (это `clia-source` по CLIA-кодам)

## См. также

- `scripts/detect_lims.py` — полный список паттернов
- `../lims-pain-extractor/SKILL.md` — что делаем, когда узнали вендора
- `../../reference/battle-cards/` — матрица вендор × персона
