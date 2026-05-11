#!/usr/bin/env python3
"""
FindyMail Email Enrichment
Input: Apollo people output (name + domain, no LinkedIn)
Output: same CSV + contact_email_verified column filled

Usage: python3 findymail_enrich.py <input_csv> <output_csv>
Requires: FINDYMAIL_API_KEY env var
"""

import csv
import sys
import os
import time
import httpx

FINDYMAIL_API_KEY = os.environ.get(
    "FINDYMAIL_API_KEY", "dSxRrqArQIsG2E5zba36HLTy0pBk1bGZra5ZDtykea70c139"
)
BASE_URL = "https://app.findymail.com"
HEADERS = {
    "Authorization": f"Bearer {FINDYMAIL_API_KEY}",
    "Content-Type": "application/json",
}


def find_email_by_name(name: str, domain: str) -> dict:
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
            return {"email": None, "verified": False, "found": False}
        if resp.status_code == 429:
            print("⚠️  Rate limited (429). Sleeping 10s...")
            time.sleep(10)
            return {"email": None, "verified": False, "found": False}
        resp.raise_for_status()
        data = resp.json()
        contact = data.get("contact") or {}
        email = data.get("email") or contact.get("email")
        verified = data.get("verified", False) or contact.get("verified", False)
        return {"email": email, "verified": verified, "found": bool(email)}
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP {e.response.status_code}")
        return {"email": None, "verified": False, "found": False}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"email": None, "verified": False, "found": False}


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_csv> <output_csv>")
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
            rows.append(row)

    if test_limit:
        rows = rows[:test_limit]

    print(f"📋 Loaded {len(rows)} contacts{' (TEST MODE)' if test_limit else ''}")
    print(f"💾 Output: {output_csv}")
    print()

    out_fieldnames = list(fieldnames) + ["email_found", "email_verified"]
    # Replace (require direct fetch) with actual email
    if "contact_email" not in out_fieldnames:
        out_fieldnames.append("contact_email")

    found_count = 0
    not_found = 0
    errors = 0

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames)
        writer.writeheader()

        for i, row in enumerate(rows, 1):
            name = row.get("contact_name", "").strip()
            domain = row.get("src_domain", "").strip()

            if not name or not domain:
                row["email_found"] = "false"
                row["email_verified"] = "false"
                writer.writerow(row)
                print(
                    f"[{i}/{len(rows)}] ⏭️  {name or '(no name)'}: skipping (missing name/domain)"
                )
                not_found += 1
                continue

            result = find_email_by_name(name, domain)

            if result["found"]:
                row["contact_email"] = result["email"]
                row["email_found"] = "true"
                row["email_verified"] = str(result["verified"]).lower()
                found_count += 1
                print(
                    f"[{i}/{len(rows)}] ✅ {name} ({domain}): {result['email']} (verified={result['verified']})"
                )
            else:
                row["email_found"] = "false"
                row["email_verified"] = "false"
                not_found += 1
                print(f"[{i}/{len(rows)}] ❌ {name} ({domain}): not found")

            writer.writerow(row)
            time.sleep(0.3)  # ~3 req/s, well within limits

    print()
    print("✅ Done.")
    print(f"   Found:     {found_count} ({found_count / len(rows) * 100:.1f}%)")
    print(f"   Not found: {not_found}")
    print(f"   Credits spent: ~{found_count} (${found_count * 0.01:.2f})")


if __name__ == "__main__":
    main()
