#!/usr/bin/env python3
"""Join our reference-lab segments with Petr's tier universe.

Outputs:
  companies_enriched_tiered.csv
  companies_not_enriched_tiered.csv   (sorted by tier priority)
  final_contacts_tiered.csv
  tier_summary.md
"""

import csv
import sys
from pathlib import Path

PYTHONPATH_EXTRA = "/tmp/pylibs"
sys.path.insert(0, PYTHONPATH_EXTRA)

import openpyxl  # noqa: E402

BASE = Path("/Users/user/vivica-outreach/source-lists")
XLSX = BASE / "lab-universe-petr-2026-05/lab-universe-2026-05.xlsx"
SEG = BASE / "segments"

TIER_ORDER = {"S+": 0, "S": 1, "A": 2, "B": 3, "C": 4, "D": 5, "E": 6, "—": 7}


def load_petr_universe(xlsx_path: Path) -> dict[str, dict]:
    """Return dict keyed by CLIA # with tier, score, cohort, sources, primary_reason."""
    wb = openpyxl.load_workbook(str(xlsx_path), read_only=True, data_only=True)
    ws = wb["All Targets"]
    rows = ws.iter_rows(values_only=True)
    headers = [str(h).strip() if h else "" for h in next(rows)]

    idx = {h: i for i, h in enumerate(headers)}
    clia_col = idx.get("CLIA #")
    tier_col = idx.get("Tier")
    score_col = idx.get("Score")
    cohort_col = idx.get("Cohort")
    sources_col = idx.get("Sources")
    reason_col = idx.get("Primary reason")

    universe = {}
    for row in rows:
        clia = str(row[clia_col]).strip() if row[clia_col] else ""
        if not clia or clia == "None":
            continue
        universe[clia] = {
            "tier": str(row[tier_col]).strip() if row[tier_col] else "—",
            "score": str(row[score_col]).strip() if row[score_col] else "",
            "cohort": str(row[cohort_col]).strip() if row[cohort_col] else "",
            "sources": str(row[sources_col]).strip() if row[sources_col] else "",
            "primary_reason": str(row[reason_col]).strip() if row[reason_col] else "",
        }
    wb.close()
    return universe


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return reader.fieldnames or [], rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  → {path.name}: {len(rows)} rows")


def tier_sort_key(row: dict) -> int:
    return TIER_ORDER.get(row.get("tier", "—"), 7)


def main():
    print("Loading Petr's universe...")
    universe = load_petr_universe(XLSX)
    print(f"  {len(universe)} labs with tiers loaded")

    TIER_COLS = ["tier", "score", "cohort", "sources", "primary_reason"]

    # ── enriched ──────────────────────────────────────────────────────────────
    enriched_headers, enriched = read_csv(SEG / "companies_enriched.csv")
    new_headers_e = enriched_headers + TIER_COLS
    enriched_out = []
    for row in enriched:
        clia = str(row.get("clia_number", "")).strip()
        tier_data = universe.get(clia, {k: "—" for k in TIER_COLS})
        enriched_out.append({**row, **tier_data})
    enriched_out.sort(key=tier_sort_key)
    write_csv(SEG / "companies_enriched_tiered.csv", new_headers_e, enriched_out)

    # ── not enriched ──────────────────────────────────────────────────────────
    not_enriched_headers, not_enriched = read_csv(SEG / "companies_not_enriched.csv")
    new_headers_n = not_enriched_headers + TIER_COLS
    not_enriched_out = []
    for row in not_enriched:
        clia = str(row.get("clia_number", "")).strip()
        tier_data = universe.get(clia, {k: "—" for k in TIER_COLS})
        not_enriched_out.append({**row, **tier_data})
    not_enriched_out.sort(key=tier_sort_key)
    write_csv(
        SEG / "companies_not_enriched_tiered.csv", new_headers_n, not_enriched_out
    )

    # ── contacts ──────────────────────────────────────────────────────────────
    contacts_headers, contacts = read_csv(SEG / "final_contacts_verified.csv")
    new_headers_c = contacts_headers + TIER_COLS
    contacts_out = []
    for row in contacts:
        clia = str(row.get("src_clia", "")).strip()
        tier_data = universe.get(clia, {k: "—" for k in TIER_COLS})
        contacts_out.append({**row, **tier_data})
    contacts_out.sort(key=tier_sort_key)
    write_csv(SEG / "final_contacts_tiered.csv", new_headers_c, contacts_out)

    # ── summary ───────────────────────────────────────────────────────────────
    def tier_dist(rows: list[dict], label: str) -> str:
        from collections import Counter

        counts = Counter(r.get("tier", "—") for r in rows)
        not_in_universe = counts.get("—", 0)
        lines = [f"\n### {label} ({len(rows)} total)\n"]
        lines.append("| Tier | Count | % |")
        lines.append("|------|-------|---|")
        total = len(rows)
        for tier in ["S+", "S", "A", "B", "C", "D", "E", "—"]:
            n = counts.get(tier, 0)
            if n == 0:
                continue
            pct = n / total * 100
            label_tier = tier if tier != "—" else "— (not in universe)"
            lines.append(f"| {label_tier} | {n} | {pct:.1f}% |")
        lines.append(
            f"\n> Not in Petr's universe: **{not_in_universe}** ({not_in_universe / total * 100:.1f}%)"
        )
        return "\n".join(lines)

    summary = "# Tier Distribution — Reference Labs Segment\n"
    summary += "\n**Source**: Petr's Lab Universe (lab-universe-2026-05.xlsx)\n"
    summary += "\n---\n"
    summary += tier_dist(enriched_out, "Enriched companies (281)")
    summary += "\n\n---\n"
    summary += tier_dist(not_enriched_out, "Not enriched companies (738)")
    summary += "\n\n---\n"
    summary += tier_dist(contacts_out, "Verified contacts (344)")
    summary += "\n\n---\n"

    # actionable breakdown for not-enriched
    hot = [r for r in not_enriched_out if r.get("tier") in ("S+", "S")]
    medium = [r for r in not_enriched_out if r.get("tier") in ("A", "B")]
    low = [r for r in not_enriched_out if r.get("tier") == "C"]
    skip = [r for r in not_enriched_out if r.get("tier") in ("D", "E")]
    unknown = [r for r in not_enriched_out if r.get("tier") == "—"]

    summary += "\n## Prioritized unenriched pipeline\n\n"
    summary += "| Priority | Tier | Count | Action |\n"
    summary += "|----------|------|-------|--------|\n"
    summary += f"| HOT | S+/S | {len(hot)} | LinkedIn / Clay next |\n"
    summary += f"| MEDIUM | A/B | {len(medium)} | Second wave |\n"
    summary += f"| LOW | C | {len(low)} | Only if quota not filled |\n"
    summary += f"| SKIP | D/E | {len(skip)} | Blocklist |\n"
    summary += f"| Unknown | — | {len(unknown)} | Not in Petr's universe — verify |\n"

    out_path = SEG / "tier_summary.md"
    out_path.write_text(summary, encoding="utf-8")
    print("  → tier_summary.md written")

    print("\nDone.")


if __name__ == "__main__":
    main()
