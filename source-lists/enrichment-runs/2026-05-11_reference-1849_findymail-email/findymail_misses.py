#!/usr/bin/env python3
"""
FindyMail search for Apollo misses — find emails for contacts Apollo Reveal failed.

Input: reveal_full.csv (filter apollo_verified=false)
Search by first_name + domain via FindyMail /api/search/name.

Usage: python3 findymail_misses.py <reveal_csv> <output_csv> [--test N]
"""

import csv
import sys
import os
import time
import httpx

API_KEY = os.environ.get(
    "FINDYMAIL_API_KEY", "dSxRrqArQIsG2E5zba36HLTy0pBk1bGZra5ZDtykea70c139"
)
BASE_URL = "https://app.findymail.com"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def search(name: str, domain: str) -> dict:
    try:
        resp = httpx.post(
            f"{BASE_URL}/api/search/name",
            headers=HEADERS,
            json={"name": name, "domain": domain},
            timeout=15,
        )
        if resp.status_code == 402:
            print("⛔ Out of credits (402). Stopping.")
            sys.exit(1)
        if resp.status_code == 404:
            return {"email": None, "verified": False}
        if resp.status_code == 429:
            print("⚠️  Rate limited (429). Sleep 10s")
            time.sleep(10)
            return {"email": None, "verified": False}
        resp.raise_for_status()
        data = resp.json()
        contact = data.get("contact") or {}
        return {
            "email": data.get("email") or contact.get("email"),
            "verified": data.get("verified", False) or contact.get("verified", False),
        }
    except Exception as e:
        print(f"❌ {e}")
        return {"email": None, "verified": False}


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <reveal_csv> <output_csv> [--test N]")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    test_limit = None
    if "--test" in sys.argv:
        idx = sys.argv.index("--test")
        test_limit = int(sys.argv[idx + 1])

    rows = []
    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row.get("apollo_verified") != "true":
                rows.append(row)

    if test_limit:
        rows = rows[:test_limit]

    print(f"📋 Apollo misses to search: {len(rows)}")
    print(f"💾 Output: {output_csv}")
    print()

    out_fields = list(fieldnames) + ["fm_email", "fm_verified"]
    seen = set()
    out_fields = [f for f in out_fields if not (f in seen or seen.add(f))]

    found = 0
    credits = 0

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        writer.writeheader()
        for i, row in enumerate(rows, 1):
            name = row.get("contact_first_name", "").strip()
            domain = row.get("src_domain", "").strip()
            if not name or not domain:
                row["fm_email"] = ""
                row["fm_verified"] = "false"
                writer.writerow(row)
                print(f"[{i}/{len(rows)}] ⏭️  skip (no name/domain)")
                continue

            r = search(name, domain)
            if r["email"]:
                row["fm_email"] = r["email"]
                row["fm_verified"] = str(r["verified"]).lower()
                found += 1
                credits += 1
                print(
                    f"[{i}/{len(rows)}] ✅ {name} ({domain}): {r['email']} (verified={r['verified']})"
                )
            else:
                row["fm_email"] = ""
                row["fm_verified"] = "false"
                print(f"[{i}/{len(rows)}] ❌ {name} ({domain})")
            writer.writerow(row)
            time.sleep(0.3)

    print()
    print("✅ Done.")
    print(f"   Found:   {found} ({found / len(rows) * 100:.1f}%)")
    print(f"   Credits: {credits} (~${credits * 0.01:.2f})")


if __name__ == "__main__":
    main()
