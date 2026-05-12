#!/usr/bin/env python3
"""Score 344 verified contacts on Vivica-ICP fit.

Joins final_contacts_tiered.csv with CLIA bucket data to compute a custom
score for contacts that are outside Petr's universe (96.8% of our pool).

Signals used (max ~150):
  - Lab type (independent vs chain)      ±30 / -10
  - CLIA age (≤2y / 2-10y / 10+y)        +25 / +10 / 0
  - CLIA cert type (Compliance/Accred)   +20 / 0 / -10
  - Persona (CEO/Lab/Med Director)       +20 / +15 / +10
  - Test volume size                     +15 / +10 / 0
  - Has LinkedIn                         +5
  - Petr's tier (if any)                 S+ +30 / S +20 / A +10 / B +5 / D/E -50

Buckets: HOT ≥80, WARM 50-79, COOL 30-49, COLD <30
"""

import csv
from collections import Counter
from datetime import date
from pathlib import Path

BASE = Path("/Users/user/vivica-outreach/source-lists")
SEG = BASE / "segments"
CLIA_BUCKET = BASE / "clia-q1-2026/clia_Q1_2026_segmented/bucket_REFERENCE.csv"

TODAY = date(2026, 5, 12)


def load_clia_lookup() -> dict[str, dict]:
    """Return CLIA# → {certified_at, certificate_type, site_count, test_volume, lab_type}."""
    lookup = {}
    with open(CLIA_BUCKET, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            clia = row.get("clia_number", "").strip()
            if clia:
                lookup[clia] = row
    return lookup


def years_since(date_str: str) -> float | None:
    if not date_str:
        return None
    try:
        d = date.fromisoformat(date_str.strip()[:10])
        return (TODAY - d).days / 365.25
    except (ValueError, TypeError):
        return None


def safe_int(v) -> int:
    try:
        return int(float(str(v).strip() or 0))
    except (ValueError, TypeError):
        return 0


def score_row(contact: dict, clia_data: dict) -> tuple[int, dict]:
    """Return (score, breakdown_dict)."""
    breakdown = {}
    score = 0

    # 1. Lab type
    lab_type = (clia_data.get("lab_type") or "").strip().lower()
    if lab_type == "independent":
        s = 30
    elif lab_type == "chain":
        s = -10
    else:
        s = 0
    breakdown["lab_type"] = s
    score += s

    # 2. CLIA age
    age = years_since(clia_data.get("certified_at", ""))
    if age is None:
        s = 0
    elif age <= 2:
        s = 25
    elif age <= 10:
        s = 10
    else:
        s = 0
    breakdown["clia_age"] = s
    score += s

    # 3. CLIA cert type
    cert = (clia_data.get("certificate_type") or "").strip().lower()
    if cert in ("compliance", "accreditation"):
        s = 20
    elif cert == "ppm":
        s = 0
    elif cert == "waiver":
        s = -10
    else:
        s = 0
    breakdown["cert_type"] = s
    score += s

    # 4. Persona
    persona = (contact.get("persona") or "").strip().lower()
    persona_scores = {"ceo_owner": 20, "lab_director": 15, "medical_director": 10}
    s = persona_scores.get(persona, 0)
    breakdown["persona"] = s
    score += s

    # 5. Test volume (lab size proxy)
    volume = safe_int(clia_data.get("test_volume"))
    if 1 <= volume <= 5000:
        s = 15  # small operator, easier sale
    elif 5000 < volume <= 50000:
        s = 10  # mid-size, has budget
    elif volume > 50000:
        s = 0  # enterprise, long cycle
    else:
        s = 0
    breakdown["test_volume"] = s
    score += s

    # 6. LinkedIn presence
    s = 5 if (contact.get("contact_linkedin") or "").strip() else 0
    breakdown["has_linkedin"] = s
    score += s

    # 7. Petr's tier override
    tier = (contact.get("tier") or "—").strip()
    tier_scores = {"S+": 30, "S": 20, "A": 10, "B": 5, "C": 0, "D": -50, "E": -50}
    s = tier_scores.get(tier, 0)
    breakdown["petr_tier"] = s
    score += s

    return score, breakdown


def bucket_of(score: int) -> str:
    if score >= 80:
        return "HOT"
    if score >= 50:
        return "WARM"
    if score >= 30:
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
        "s_lab_type",
        "s_clia_age",
        "s_cert_type",
        "s_persona",
        "s_test_volume",
        "s_has_linkedin",
        "s_petr_tier",
        "lab_type_raw",
        "clia_age_years",
        "cert_type_raw",
        "test_volume_raw",
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
        age = years_since(clia_data.get("certified_at", ""))
        contact["vivica_score"] = score
        contact["vivica_bucket"] = bucket_of(score)
        contact["s_lab_type"] = bd["lab_type"]
        contact["s_clia_age"] = bd["clia_age"]
        contact["s_cert_type"] = bd["cert_type"]
        contact["s_persona"] = bd["persona"]
        contact["s_test_volume"] = bd["test_volume"]
        contact["s_has_linkedin"] = bd["has_linkedin"]
        contact["s_petr_tier"] = bd["petr_tier"]
        contact["lab_type_raw"] = clia_data.get("lab_type", "")
        contact["clia_age_years"] = f"{age:.1f}" if age is not None else ""
        contact["cert_type_raw"] = clia_data.get("certificate_type", "")
        contact["test_volume_raw"] = clia_data.get("test_volume", "")
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
        "## Scoring model (max ~150)",
        "",
        "| Signal | Source | Weights |",
        "|--------|--------|---------|",
        "| Lab type | `bucket_REFERENCE.lab_type` | independent +30 / chain -10 |",
        "| CLIA age | `bucket_REFERENCE.certified_at` | ≤2y +25 / 2-10y +10 / 10+y 0 |",
        "| Cert type | `bucket_REFERENCE.certificate_type` | Compliance/Accred +20 / PPM 0 / Waiver -10 |",
        "| Persona | `final_contacts.persona` | CEO/Owner +20 / Lab Dir +15 / Med Dir +10 |",
        "| Test volume | `bucket_REFERENCE.test_volume` | 1-5k +15 / 5k-50k +10 / 50k+ 0 |",
        "| LinkedIn | `contact_linkedin` non-empty | +5 |",
        "| Petr's tier | from `final_contacts_tiered.tier` | S+ +30 / S +20 / A +10 / B +5 / D/E -50 |",
        "",
        "## Bucket distribution",
        "",
        "| Bucket | Threshold | Count | % | Action |",
        "|--------|-----------|-------|---|--------|",
    ]
    bucket_actions = {
        "HOT": ("≥80", "First wave in SmartLead"),
        "WARM": ("50-79", "Main pool"),
        "COOL": ("30-49", "Top-up wave"),
        "COLD": ("<30", "Skip or last resort"),
    }
    for b in ["HOT", "WARM", "COOL", "COLD"]:
        n = buckets.get(b, 0)
        threshold, action = bucket_actions[b]
        pct = n / total * 100 if total else 0
        lines.append(f"| {b} | {threshold} | {n} | {pct:.1f}% | {action} |")

    # Top 20 examples
    lines += ["", "## Top 20 scored contacts", ""]
    lines.append(
        "| # | Score | Bucket | Lab | Persona | Lab type | CLIA age (y) | Cert | Tier |"
    )
    lines.append(
        "|---|-------|--------|-----|---------|----------|--------------|------|------|"
    )
    for i, r in enumerate(out[:20], 1):
        lines.append(
            f"| {i} | {r['vivica_score']} | {r['vivica_bucket']} | "
            f"{r['src_name'][:40]} | {r['persona']} | {r['lab_type_raw']} | "
            f"{r['clia_age_years']} | {r['cert_type_raw']} | {r.get('tier', '—')} |"
        )

    # Score component averages
    lines += ["", "## Average contribution per signal", ""]
    lines.append("| Signal | Avg points | Max possible |")
    lines.append("|--------|------------|--------------|")
    components = [
        ("s_lab_type", 30),
        ("s_clia_age", 25),
        ("s_cert_type", 20),
        ("s_persona", 20),
        ("s_test_volume", 15),
        ("s_has_linkedin", 5),
        ("s_petr_tier", 30),
    ]
    for col, max_val in components:
        avg = sum(int(r[col]) for r in out) / total
        lines.append(f"| {col.replace('s_', '')} | {avg:+.1f} | {max_val} |")

    # Cross-tab: bucket × Petr's tier
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

    summary_path = SEG / "scoring_summary.md"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  → {summary_path.name} written")

    print("\nDone.")


if __name__ == "__main__":
    main()
