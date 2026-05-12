#!/usr/bin/env python3
"""Export final_contacts_scored.csv to xlsx with a README sheet.

Two sheets:
  - README: how to read the file, scoring model, bucket meanings, source pipeline
  - Contacts: the 344 scored contacts (same as CSV)
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, "/tmp/pylibs")

from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

BASE = Path("/Users/user/vivica-outreach/source-lists/segments")
SRC = BASE / "final_contacts_scored.csv"
DST = BASE / "final_contacts_scored.xlsx"

BUCKET_FILL = {
    "HOT": PatternFill("solid", fgColor="FFD6D6"),
    "WARM": PatternFill("solid", fgColor="FFE9C2"),
    "COOL": PatternFill("solid", fgColor="DDEEFF"),
    "COLD": PatternFill("solid", fgColor="E0E0E0"),
}


def add_readme(ws):
    bold = Font(bold=True, size=12)
    h1 = Font(bold=True, size=16)
    h2 = Font(bold=True, size=13)
    wrap = Alignment(wrap_text=True, vertical="top")
    header_fill = PatternFill("solid", fgColor="F0F0F0")

    rows = [
        ("Vivica Outreach — Scored Contacts", h1),
        ("", None),
        ("Что это за документ", h2),
        (
            "Финальный приоритизированный список из 344 верифицированных контактов "
            "по US reference-лабораториям. Каждый контакт оценён по 6 сигналам и "
            "распределён в bucket HOT / WARM / COOL / COLD. Лист 'Contacts' — данные, "
            "отсортированные по убыванию vivica_score.",
            wrap,
        ),
        ("", None),
        ("Pool", bold),
        (
            "🟧 Наша CMS-enrichment воронка (НЕ путать с 🟦 HOT-универсом Петра). "
            "Источник: CMS CLIA Q1 2026 (1849 reference-лаб) → Apollo people search → "
            "Apollo Reveal по ID → FindyMail SMTP double-verify. "
            "344 уникальных контакта на 270 компаниях.",
            wrap,
        ),
        ("", None),
        ("Как собрано — воронка", h2),
        ("1. CMS CLIA Q1 2026 → 1849 reference-лаб", None),
        ("2. Domain enrichment (Clay + Exa) → 1019 уникальных доменов", None),
        (
            "3. Apollo people search → 1252 контакта на 383 доменах (37% domain hit)",
            None,
        ),
        ("4. Apollo Reveal (email by ID) → 1033 verified", None),
        ("5. FindyMail SMTP verify → 878 valid (14% bounce отсеяно)", None),
        ("6. Dedup по email → 344 unique contacts", None),
        (
            "Полная воронка с конверсиями: source-lists/enrichment-runs/2026-05-11_reference-1849_findymail-email/analytics.md",
            None,
        ),
        ("", None),
        ("Скоринг — модель (max ~120 баллов)", h2),
        (
            "Калиброван под реальное распределение сигналов в данных. CLIA age и "
            "cert type исключены — на Q1 2026 cohort нет дисперсии (все ≤6 мес, "
            "99% Compliance).",
            wrap,
        ),
        ("", None),
        ("Сигнал | Источник | Веса", bold),
        (
            "Facility type | cms_facility_type_name | independent +30 / public_health +15 / non-lab -30",
            None,
        ),
        (
            "Test volume | test_volume | 1k-50k +25 / 50k-500k +15 / 1-999 +10 / 500k+ 0 / 0 -10",
            None,
        ),
        ("Site count | site_count | 0-1 +10 / 2-5 0 / 6+ -10", None),
        ("Persona | persona | CEO/Owner +20 / Lab Dir +15 / Med Dir +10", None),
        ("LinkedIn | contact_linkedin not empty | +5", None),
        (
            "Petr's tier | tier (если в его универсе) | S+ +30 / S +20 / A +10 / B +5 / D/E -50",
            None,
        ),
        ("", None),
        ("Buckets", h2),
        ("🔥 HOT (≥75) — 188 контактов (54.7%) — первая волна SmartLead", None),
        ("🌡 WARM (50-74) — 97 контактов (28.2%) — основной пул", None),
        ("❄️ COOL (25-49) — 26 контактов (7.6%) — добивка", None),
        (
            "🧊 COLD (<25) — 33 контакта (9.6%) — SKIP. В основном ambulances/mobile_labs/ASCs/blood_banks (по факту не лабы)",
            None,
        ),
        ("", None),
        ("Колонки на листе Contacts", h2),
        ("Базовые (из verify-пайплайна):", bold),
        ("src_name — имя лабораторной компании (из CMS CLIA)", None),
        ("src_domain — основной домен", None),
        ("src_clia — CLIA-номер (ключ для join с CMS-данными)", None),
        (
            "persona — Apollo-классификация: ceo_owner / lab_director / medical_director",
            None,
        ),
        (
            "contact_first_name / contact_full_name / contact_email / contact_title / contact_linkedin",
            None,
        ),
        ("source — обычно apollo+findymail_verified", None),
        ("", None),
        ("Петров скоринг (из его универса, если CLIA там есть — у 11/344):", bold),
        ("tier — S+/S/A/B/C/D/E или — (нет в универсе)", None),
        ("score / cohort / sources / primary_reason — внешний скоринг", None),
        ("", None),
        ("Наш Vivica-fit скоринг:", bold),
        ("vivica_score — суммарный балл (max ~120)", None),
        ("vivica_bucket — HOT / WARM / COOL / COLD", None),
        (
            "s_facility_type / s_test_volume / s_site_count / s_persona / s_has_linkedin / s_petr_tier — вклад каждого сигнала",
            None,
        ),
        (
            "facility_type_raw / test_volume_raw / site_count_raw — исходные значения (для прозрачности)",
            None,
        ),
        ("", None),
        ("Как использовать", h2),
        ("1. Загрузить Wave 1 в SmartLead: фильтр vivica_bucket = HOT (188)", None),
        ("2. После Wave 1 — Wave 2: vivica_bucket = WARM (97)", None),
        ("3. COOL (26) — на добивку если квота не закрылась", None),
        (
            "4. COLD (33) НЕ грузить — это ambulances/mobile units, не ICP для Vivica LIMS",
            None,
        ),
        (
            "5. Blocklist (русскоязычные): отдельно вычесть source-lists/segments/russian_confirmed.csv (19)",
            None,
        ),
        ("", None),
        ("Ключевые предостережения", h2),
        (
            "• Apollo email_status=verified врёт на 14.4% — все 344 пропущены через FindyMail SMTP, можно грузить",
            None,
        ),
        (
            "• 333/344 контактов вне Петровой универсума — это не баг, это другой пул (CMS-only пайплайн)",
            None,
        ),
        (
            "• 76% компаний имеют только одну персону (full 3-persona ICP coverage редкий)",
            None,
        ),
        (
            "• Угол outreach: 'мигрируй с текущей системы' (established операторы), НЕ 'купи правильно с первого раза' (это для Петрового HOT-универса)",
            None,
        ),
        ("", None),
        ("Связанные файлы", h2),
        ("source-lists/segments/README.md — обзор всей папки segments", None),
        (
            "source-lists/segments/scoring_summary.md — распределение, топ-20, breakdown",
            None,
        ),
        ("source-lists/segments/score_contacts.py — скрипт, которым посчитано", None),
        ("source-lists/segments/tier_summary.md — распределение Петрова tier", None),
        (
            "source-lists/enrichment-runs/2026-05-11_reference-1849_findymail-email/manifest.md — manifest run'а",
            None,
        ),
        ("tracking/data-log.md — лог всех data-операций", None),
        ("", None),
        ("Run-id скоринга: segments-internal-scoring (2026-05-12)", None),
    ]

    for i, (text, style) in enumerate(rows, start=1):
        cell = ws.cell(row=i, column=1, value=text)
        if style:
            if style is bold:
                cell.font = bold
            elif style is h1:
                cell.font = h1
            elif style is h2:
                cell.font = h2
                cell.fill = header_fill
            elif style is wrap:
                cell.alignment = wrap

    ws.column_dimensions["A"].width = 140
    for i in range(1, len(rows) + 1):
        ws.row_dimensions[i].height = None


def add_contacts(ws):
    with open(SRC, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="333333")
    for j, h in enumerate(headers, start=1):
        c = ws.cell(row=1, column=j, value=h)
        c.font = header_font
        c.fill = header_fill

    bucket_idx = headers.index("vivica_bucket")
    score_idx = headers.index("vivica_score")

    for i, row in enumerate(rows, start=2):
        bucket = row[bucket_idx]
        fill = BUCKET_FILL.get(bucket)
        for j, val in enumerate(row, start=1):
            if j - 1 == score_idx:
                try:
                    val = int(val)
                except ValueError:
                    pass
            c = ws.cell(row=i, column=j, value=val)
            if fill and (j - 1) in (bucket_idx, score_idx):
                c.fill = fill
                c.font = Font(bold=True)

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(rows) + 1}"

    widths = {
        "src_name": 38,
        "src_domain": 28,
        "src_clia": 14,
        "persona": 17,
        "contact_first_name": 14,
        "contact_full_name": 24,
        "contact_email": 32,
        "contact_title": 36,
        "contact_linkedin": 36,
        "source": 24,
        "tier": 6,
        "score": 8,
        "cohort": 18,
        "sources": 18,
        "primary_reason": 40,
        "vivica_score": 10,
        "vivica_bucket": 11,
        "facility_type_raw": 16,
        "test_volume_raw": 12,
        "site_count_raw": 10,
    }
    for j, h in enumerate(headers, start=1):
        w = widths.get(h, 10)
        ws.column_dimensions[get_column_letter(j)].width = w


def main():
    wb = Workbook()

    ws_readme = wb.active
    ws_readme.title = "README"
    add_readme(ws_readme)

    ws_contacts = wb.create_sheet("Contacts")
    add_contacts(ws_contacts)

    wb.save(str(DST))
    print(f"  → {DST.name}")


if __name__ == "__main__":
    main()
