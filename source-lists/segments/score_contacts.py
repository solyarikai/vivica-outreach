#!/usr/bin/env python3
"""Score 344 verified contacts on Vivica-ICP fit.

Joins final_contacts_tiered.csv with CLIA bucket data to compute a custom
score for contacts outside Petr's universe (96.8% of our pool).

Calibrated to actual signal distribution in the data:
  - CLIA age and cert type dropped — no variance on CLIA Q1 2026 cohort
  - cms_facility_type_name is the real lab-type signal (not lab_type column)
  - test_volume is the strongest discriminator (range 0..11M, median ~10k)
  - site_count distinguishes truly-independent from chain locations

Signals (max ~120):
  - Facility type           independent +30 / public_health +15 / other 0 / non-lab -30
  - Test volume             1k-5k +25 / 5k-50k +25 / 1-999 +10 / 50k-500k +15 / 500k+ 0 / 0 -10
  - Site count              0-1 +10 / 2-5 0 / 6+ -10
  - Persona                 CEO +20 / Lab Dir +15 / Med Dir +10
  - LinkedIn                +5
  - Petr's tier             S+ +30 / S +20 / A +10 / B +5 / D/E -50

Buckets: HOT ≥75, WARM 50-74, COOL 25-49, COLD <25
"""

import csv
from collections import Counter
from datetime import date
from pathlib import Path

BASE = Path("/Users/user/vivica-outreach/source-lists")
SEG = BASE / "segments"
CLIA_BUCKET = BASE / "clia-q1-2026/clia_Q1_2026_segmented/bucket_REFERENCE.csv"

TODAY = date(2026, 5, 12)

NON_LAB_FACILITIES = {
    "ambulance",
    "mobile_lab",
    "hmo",
    "ambulatory_surgery_center",
    "blood_bank",
    "hospice",
    "tissue_bank",
}


def load_clia_lookup():
    lookup = {}
    with open(CLIA_BUCKET, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            clia = row.get("clia_number", "").strip()
            if clia:
                lookup[clia] = row
    return lookup


def safe_int(v) -> int:
    try:
        return int(float(str(v).strip() or 0))
    except (ValueError, TypeError):
        return 0


def score_row(contact: dict, clia_data: dict):
    breakdown = {}
    score = 0

    # 1. Facility type (cms_facility_type_name — the real classifier)
    ftype = (clia_data.get("cms_facility_type_name") or "").strip().lower()
    if ftype == "independent":
        s = 30
    elif ftype == "public_health_lab":
        s = 15
    elif ftype in NON_LAB_FACILITIES:
        s = -30
    else:
        s = 0
    breakdown["facility_type"] = s
    score += s

    # 2. Test volume (main discriminator)
    volume = safe_int(clia_data.get("test_volume"))
    if volume == 0:
        s = -10
    elif volume < 1000:
        s = 10
    elif volume < 5000:
        s = 25
    elif volume < 50000:
        s = 25
    elif volume < 500000:
        s = 15
    else:
        s = 0
    breakdown["test_volume"] = s
    score += s

    # 3. Site count (chain detection)
    sites = safe_int(clia_data.get("site_count"))
    if sites <= 1:
        s = 10
    elif sites <= 5:
        s = 0
    else:
        s = -10
    breakdown["site_count"] = s
    score += s

    # 4. Persona
    persona = (contact.get("persona") or "").strip().lower()
    persona_scores = {"ceo_owner": 20, "lab_director": 15, "medical_director": 10}
    s = persona_scores.get(persona, 0)
    breakdown["persona"] = s
    score += s

    # 5. LinkedIn presence
    s = 5 if (contact.get("contact_linkedin") or "").strip() else 0
    breakdown["has_linkedin"] = s
    score += s

    # 6. Petr's tier override
    tier = (contact.get("tier") or "—").strip()
    tier_scores = {"S+": 30, "S": 20, "A": 10, "B": 5, "C": 0, "D": -50, "E": -50}
    s = tier_scores.get(tier, 0)
    breakdown["petr_tier"] = s
    score += s

    return score, breakdown


def bucket_of(score: int) -> str:
    if score >= 75:
        return "HOT"
    if score >= 50:
        return "WARM"
    if score >= 25:
        return "COOL"
    return "COLD"


def main():
    print("Loading CLIA reference bucket...")
    clia = load_clia_lookup()
    print(f"  {len(clia)} CLIA records loaded")

    print("Loading tiered contacts...")
    with open(SEG / "final_contacts_tiered.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        contacts = list(reader)
        in_headers = reader.fieldnames or []
    print(f"  {len(contacts)} contacts")

    score_cols = [
        "vivica_score",
        "vivica_bucket",
        "s_facility_type",
        "s_test_volume",
        "s_site_count",
        "s_persona",
        "s_has_linkedin",
        "s_petr_tier",
        "facility_type_raw",
        "test_volume_raw",
        "site_count_raw",
    ]
    out_headers = in_headers + score_cols

    out = []
    missing_clia = 0
    for contact in contacts:
        clia_id = contact.get("src_clia", "").strip()
        clia_data = clia.get(clia_id, {})
        if not clia_data:
            missing_clia += 1
        score, bd = score_row(contact, clia_data)
        contact["vivica_score"] = score
        contact["vivica_bucket"] = bucket_of(score)
        contact["s_facility_type"] = bd["facility_type"]
        contact["s_test_volume"] = bd["test_volume"]
        contact["s_site_count"] = bd["site_count"]
        contact["s_persona"] = bd["persona"]
        contact["s_has_linkedin"] = bd["has_linkedin"]
        contact["s_petr_tier"] = bd["petr_tier"]
        contact["facility_type_raw"] = clia_data.get("cms_facility_type_name", "")
        contact["test_volume_raw"] = clia_data.get("test_volume", "")
        contact["site_count_raw"] = clia_data.get("site_count", "")
        out.append(contact)

    out.sort(key=lambda r: -int(r["vivica_score"]))

    out_path = SEG / "final_contacts_scored.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_headers)
        writer.writeheader()
        writer.writerows(out)
    print(f"  → {out_path.name}: {len(out)} rows ({missing_clia} missing CLIA lookup)")

    # ── summary ───────────────────────────────────────────────────────────────
    buckets = Counter(r["vivica_bucket"] for r in out)
    total = len(out)
    lines = [
        "# Vivica Score Distribution — Reference Labs Contacts",
        "",
        "**Source**: `final_contacts_tiered.csv` (344) × `bucket_REFERENCE.csv` (1849)",
        f"**Date**: {TODAY.isoformat()}",
        "**Script**: `score_contacts.py`",
        "",
        "## Scoring model (max ~120)",
        "",
        "Calibrated to actual signal distribution in the data. CLIA age and cert type",
        "were dropped — on the Q1 2026 cohort all contacts are ≤6 months old and 99%",
        "are Compliance certificates, so these signals don't discriminate.",
        "",
        "| Signal | Source | Weights |",
        "|--------|--------|---------|",
        "| Facility type | `cms_facility_type_name` | independent +30 / public_health +15 / non-lab -30 |",
        "| Test volume | `test_volume` | 1k-50k +25 / 50k-500k +15 / 1-999 +10 / 500k+ 0 / 0 -10 |",
        "| Site count | `site_count` | 0-1 +10 / 2-5 0 / 6+ -10 |",
        "| Persona | `persona` | CEO/Owner +20 / Lab Dir +15 / Med Dir +10 |",
        "| LinkedIn | `contact_linkedin` non-empty | +5 |",
        "| Petr's tier | `tier` | S+ +30 / S +20 / A +10 / B +5 / D/E -50 |",
        "",
        "## Bucket distribution",
        "",
        "| Bucket | Threshold | Count | % | Action |",
        "|--------|-----------|-------|---|--------|",
    ]
    bucket_actions = {
        "HOT": ("≥75", "First wave in SmartLead"),
        "WARM": ("50-74", "Main pool"),
        "COOL": ("25-49", "Top-up wave"),
        "COLD": ("<25", "Skip or last resort"),
    }
    for b in ["HOT", "WARM", "COOL", "COLD"]:
        n = buckets.get(b, 0)
        threshold, action = bucket_actions[b]
        pct = n / total * 100 if total else 0
        lines.append(f"| {b} | {threshold} | {n} | {pct:.1f}% | {action} |")

    lines += ["", "## Top 20 scored contacts", ""]
    lines.append(
        "| # | Score | Bucket | Lab | Persona | Facility | Vol | Sites | Tier |"
    )
    lines.append(
        "|---|-------|--------|-----|---------|----------|-----|-------|------|"
    )
    for i, r in enumerate(out[:20], 1):
        lines.append(
            f"| {i} | {r['vivica_score']} | {r['vivica_bucket']} | "
            f"{r['src_name'][:38]} | {r['persona']} | {r['facility_type_raw']} | "
            f"{r['test_volume_raw']} | {r['site_count_raw']} | {r.get('tier', '—')} |"
        )

    lines += ["", "## Bottom 10 (likely skip)", ""]
    lines.append(
        "| # | Score | Bucket | Lab | Persona | Facility | Vol | Sites | Tier |"
    )
    lines.append(
        "|---|-------|--------|-----|---------|----------|-----|-------|------|"
    )
    for i, r in enumerate(out[-10:], 1):
        lines.append(
            f"| {i} | {r['vivica_score']} | {r['vivica_bucket']} | "
            f"{r['src_name'][:38]} | {r['persona']} | {r['facility_type_raw']} | "
            f"{r['test_volume_raw']} | {r['site_count_raw']} | {r.get('tier', '—')} |"
        )

    lines += ["", "## Average contribution per signal", ""]
    lines.append("| Signal | Avg points | Max possible |")
    lines.append("|--------|------------|--------------|")
    components = [
        ("s_facility_type", 30),
        ("s_test_volume", 25),
        ("s_site_count", 10),
        ("s_persona", 20),
        ("s_has_linkedin", 5),
        ("s_petr_tier", 30),
    ]
    for col, max_val in components:
        avg = sum(int(r[col]) for r in out) / total
        lines.append(f"| {col.replace('s_', '')} | {avg:+.1f} | {max_val} |")

    lines += ["", "## Cross-check: Vivica bucket × Petr's tier", ""]
    lines.append("| | S+ | S | A | B | C | D | E | — | Total |")
    lines.append("|---|----|---|----|----|----|----|----|----|-------|")
    for b in ["HOT", "WARM", "COOL", "COLD"]:
        row = [b]
        bucket_rows = [r for r in out if r["vivica_bucket"] == b]
        tier_counts = Counter(r.get("tier", "—") for r in bucket_rows)
        for t in ["S+", "S", "A", "B", "C", "D", "E", "—"]:
            row.append(str(tier_counts.get(t, 0)))
        row.append(str(len(bucket_rows)))
        lines.append("| " + " | ".join(row) + " |")

    lines += ["", "## Facility type breakdown across pool", ""]
    ftype_counts = Counter(r["facility_type_raw"] for r in out)
    lines.append("| Facility type | Count | Avg score |")
    lines.append("|---------------|-------|-----------|")
    for ft, n in ftype_counts.most_common():
        avg_s = (
            sum(int(r["vivica_score"]) for r in out if r["facility_type_raw"] == ft) / n
        )
        lines.append(f"| {ft or '(empty)'} | {n} | {avg_s:.1f} |")

    summary_path = SEG / "scoring_summary.md"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  → {summary_path.name} written")

    print("\nDone.")


if __name__ == "__main__":
    main()
