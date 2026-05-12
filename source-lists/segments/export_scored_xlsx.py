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
        ("What this document is", h2),
        (
            "Final prioritized list of 344 verified contacts at US reference labs. "
            "Each contact is scored on 6 signals and assigned to a HOT / WARM / "
            "COOL / COLD bucket. The 'Contacts' sheet holds the data, sorted by "
            "vivica_score descending.",
            wrap,
        ),
        ("", None),
        ("Pool", bold),
        (
            "Our CMS-enrichment funnel (NOT to be confused with Petr's HOT universe). "
            "Source: CMS CLIA Q1 2026 (1,849 reference labs) -> Apollo people search "
            "-> Apollo Reveal by ID -> FindyMail SMTP double-verify. "
            "344 unique contacts across 270 companies.",
            wrap,
        ),
        ("", None),
        ("How it was assembled — funnel", h2),
        ("1. CMS CLIA Q1 2026 -> 1,849 reference labs", None),
        ("2. Domain enrichment (Clay + Exa) -> 1,019 unique domains", None),
        (
            "3. Apollo people search -> 1,252 contacts across 383 domains (37% domain hit)",
            None,
        ),
        ("4. Apollo Reveal (email by ID) -> 1,033 verified", None),
        ("5. FindyMail SMTP verify -> 878 valid (14% bounce filtered out)", None),
        ("6. Dedup by email -> 344 unique contacts", None),
        (
            "Full funnel with conversions: source-lists/enrichment-runs/2026-05-11_reference-1849_findymail-email/analytics.md",
            None,
        ),
        ("", None),
        ("Scoring model (max ~120 points)", h2),
        (
            "Calibrated to the actual signal distribution in the data. CLIA age "
            "and certificate type were dropped — on the Q1 2026 cohort there is "
            "no variance (all <=6 months old, 99% Compliance).",
            wrap,
        ),
        ("", None),
        ("Signal | Source | Weights", bold),
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
            "Petr's tier | tier (only if present in his universe) | S+ +30 / S +20 / A +10 / B +5 / D/E -50",
            None,
        ),
        ("", None),
        ("Bucket thresholds — why these cutoffs", h2),
        (
            "Thresholds are anchored to the 'reference contact' baseline. A typical "
            "independent lab + single site + LinkedIn already nets 45 points before "
            "persona or volume — so any meaningful prospect lands at 50+. The cutoffs "
            "express WHAT is missing, not just a number.",
            wrap,
        ),
        ("", None),
        (
            "HOT (>=75)  — 188 contacts (54.7%)  — Independent lab + decision-maker + reasonable volume. Fundamentally a good fit. Wave 1 in SmartLead.",
            wrap,
        ),
        (
            "WARM (50-74) —  97 contacts (28.2%) — Independent lab but one signal is off: non-CEO persona, or 0 volume data, or large enterprise. Still worth the touch. Main pool.",
            wrap,
        ),
        (
            "COOL (25-49) —  26 contacts (7.6%)  — Multiple weak signals: small chain (2-5 sites) OR public-health lab OR low-seniority persona. Top-up wave if quota is open.",
            wrap,
        ),
        (
            "COLD (<25)   —  33 contacts (9.6%)  — Facility type is wrong: ambulance / mobile_lab / ASC / blood_bank / hospice / tissue_bank. These are NOT lab ICP for Vivica — they slipped into REFERENCE bucket by CMS misclassification. SKIP.",
            wrap,
        ),
        ("", None),
        (
            "Typical score arithmetic for a HOT contact: independent (+30) + sweet-spot volume 1k-50k (+25) + single site (+10) + CEO/Owner (+20) + LinkedIn (+5) = 90. Add Petr's S/S+ tier and you're at 110-120.",
            wrap,
        ),
        (
            "Typical COLD: non-lab facility (-30) + no volume (-10) + 2 sites (0) + persona (+10..20) + LinkedIn (+5) = -5 to -15.",
            wrap,
        ),
        ("", None),
        ("Columns on the Contacts sheet", h2),
        ("Base (from verify pipeline):", bold),
        ("src_name — lab company name (from CMS CLIA)", None),
        ("src_domain — primary domain", None),
        ("src_clia — CLIA number (join key for CMS data)", None),
        (
            "persona — Apollo classification: ceo_owner / lab_director / medical_director",
            None,
        ),
        (
            "contact_first_name / contact_full_name / contact_email / contact_title / contact_linkedin",
            None,
        ),
        ("source — typically apollo+findymail_verified", None),
        ("", None),
        (
            "Petr's scoring (from his universe — only 11/344 contacts have it):",
            bold,
        ),
        ("tier — S+/S/A/B/C/D/E or — (not in universe)", None),
        ("score / cohort / sources / primary_reason — external scoring fields", None),
        ("", None),
        ("Our Vivica-fit scoring:", bold),
        ("vivica_score — total score (max ~120)", None),
        ("vivica_bucket — HOT / WARM / COOL / COLD", None),
        (
            "s_facility_type / s_test_volume / s_site_count / s_persona / s_has_linkedin / s_petr_tier — per-signal contribution",
            None,
        ),
        (
            "facility_type_raw / test_volume_raw / site_count_raw — raw values (for transparency)",
            None,
        ),
        ("", None),
        ("How to use", h2),
        ("1. Load Wave 1 into SmartLead: filter vivica_bucket = HOT (188)", None),
        ("2. After Wave 1 -> Wave 2: vivica_bucket = WARM (97)", None),
        ("3. COOL (26) — top-up if quota is not filled", None),
        (
            "4. COLD (33) — DO NOT load. These are ambulances / mobile units, not ICP for Vivica LIMS.",
            None,
        ),
        (
            "5. Blocklist (Russian-speaking): subtract source-lists/segments/russian_confirmed.csv (19) separately.",
            None,
        ),
        ("", None),
        ("Key caveats", h2),
        (
            "- Apollo email_status=verified is wrong 14.4% of the time. All 344 contacts here passed FindyMail SMTP — safe to load.",
            None,
        ),
        (
            "- 333/344 contacts are outside Petr's universe. This is not a bug, it's a different pool (CMS-only pipeline).",
            None,
        ),
        (
            "- 76% of companies have only one persona reached (full 3-persona ICP coverage is rare).",
            None,
        ),
        (
            "- Outreach angle: 'migrate from your current system' (established operators), NOT 'buy right the first time' (that copy is for Petr's HOT universe).",
            None,
        ),
        ("", None),
        ("Related files", h2),
        (
            "source-lists/segments/README.md — overview of the whole segments folder",
            None,
        ),
        (
            "source-lists/segments/scoring_summary.md — distribution, top-20, breakdown",
            None,
        ),
        ("source-lists/segments/score_contacts.py — the scoring script", None),
        ("source-lists/segments/tier_summary.md — Petr's tier distribution", None),
        (
            "source-lists/enrichment-runs/2026-05-11_reference-1849_findymail-email/manifest.md — enrichment run manifest",
            None,
        ),
        ("tracking/data-log.md — log of all data operations", None),
        ("", None),
        ("Scoring run-id: segments-internal-scoring (2026-05-12)", None),
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
