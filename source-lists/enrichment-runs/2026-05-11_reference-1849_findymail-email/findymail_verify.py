#!/usr/bin/env python3
"""
FindyMail verify — double-verify Apollo-revealed emails via SMTP check.

Input: reveal_full.csv (filter apollo_verified=true)
POST /api/verify {"email": "..."} — 1 credit per verification.

Usage: python3 findymail_verify.py <reveal_csv> <output_csv> [--test N]
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


def verify(email: str) -> dict:
    try:
        resp = httpx.post(
            f"{BASE_URL}/api/verify",
            headers=HEADERS,
            json={"email": email},
            timeout=15,
        )
        if resp.status_code == 402:
            print("⛔ Out of credits (402). Stopping.")
            sys.exit(1)
        if resp.status_code == 429:
            print("⚠️  Rate limited (429). Sleep 10s")
            time.sleep(10)
            return {"verified": None, "status": "rate_limit"}
        resp.raise_for_status()
        data = resp.json()
        return {
            "verified": data.get("verified"),
            "status": data.get("provider") or data.get("status") or "",
        }
    except Exception as e:
        print(f"❌ {e}")
        return {"verified": None, "status": "error"}


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
            if row.get("apollo_verified") == "true" and row.get("apollo_email"):
                rows.append(row)

    if test_limit:
        rows = rows[:test_limit]

    print(f"📋 Apollo verified emails to re-verify: {len(rows)}")
    print(f"💾 Output: {output_csv}")
    print(f"💳 Max cost: ~${len(rows) * 0.01:.2f}")
    print()

    out_fields = list(fieldnames) + ["fm_verified", "fm_status"]
    seen = set()
    out_fields = [f for f in out_fields if not (f in seen or seen.add(f))]

    valid = 0
    invalid = 0
    credits = 0

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        writer.writeheader()
        for i, row in enumerate(rows, 1):
            email = row.get("apollo_email", "").strip()
            r = verify(email)
            row["fm_verified"] = (
                str(r["verified"]).lower() if r["verified"] is not None else ""
            )
            row["fm_status"] = r["status"]
            credits += 1
            if r["verified"] is True:
                valid += 1
                print(f"[{i}/{len(rows)}] ✅ {email} ({r['status']})")
            else:
                invalid += 1
                print(
                    f"[{i}/{len(rows)}] ❌ {email} verified={r['verified']} ({r['status']})"
                )
            writer.writerow(row)
            time.sleep(0.3)

    print()
    print("✅ Done.")
    print(f"   Valid:   {valid} ({valid / len(rows) * 100:.1f}%)")
    print(f"   Invalid: {invalid}")
    print(f"   Credits: {credits} (~${credits * 0.01:.2f})")


if __name__ == "__main__":
    main()
