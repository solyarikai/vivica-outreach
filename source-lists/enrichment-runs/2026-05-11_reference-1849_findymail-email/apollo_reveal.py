#!/usr/bin/env python3
"""
Apollo Reveal — hydrate emails for Apollo contacts using their IDs.

Uses /people/bulk_match with apollo_id. Costs 1 credit ($0.001) per verified
email found. Misses are free.

Usage: python3 apollo_reveal.py <apollo_ids_csv> <output_csv> [--test N]
"""

import csv
import sys
import os
import time
import httpx

APOLLO_API_KEY = os.environ.get("GTM_MCP_APOLLO_API_KEY")
if not APOLLO_API_KEY:
    print("⛔ GTM_MCP_APOLLO_API_KEY not set")
    sys.exit(1)

BASE_URL = "https://api.apollo.io/api/v1"
HEADERS = {"X-Api-Key": APOLLO_API_KEY, "Content-Type": "application/json"}


def bulk_match(ids: list[str]) -> list[dict]:
    """Call Apollo /people/bulk_match for up to 10 IDs."""
    if not ids:
        return []
    details = [{"id": i} for i in ids]
    try:
        resp = httpx.post(
            f"{BASE_URL}/people/bulk_match",
            headers=HEADERS,
            json={"details": details, "reveal_personal_emails": False},
            timeout=30,
        )
        if resp.status_code == 402:
            print("⛔ Apollo credits exhausted (402). Stopping.")
            sys.exit(1)
        if resp.status_code == 429:
            print("⚠️  Rate limited (429). Sleeping 30s...")
            time.sleep(30)
            return []
        resp.raise_for_status()
        return resp.json().get("matches", []) or []
    except Exception as e:
        print(f"❌ bulk_match error: {e}")
        return []


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <apollo_ids_csv> <output_csv> [--test N]")
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
            if row.get("apollo_id"):
                rows.append(row)

    if test_limit:
        rows = rows[:test_limit]

    print(f"📋 Contacts to reveal: {len(rows)}{' (TEST)' if test_limit else ''}")
    print(f"💾 Output: {output_csv}")
    print(f"💳 Max cost: ${len(rows) * 0.001:.3f} (only verified emails charged)")
    print()

    out_fieldnames = list(fieldnames) + [
        "apollo_email",
        "apollo_full_name",
        "apollo_last_name",
        "apollo_linkedin",
        "apollo_verified",
    ]
    seen = set()
    out_fieldnames = [f for f in out_fieldnames if not (f in seen or seen.add(f))]

    found = 0
    credits = 0
    batch_size = 10

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames, extrasaction="ignore")
        writer.writeheader()

        for batch_start in range(0, len(rows), batch_size):
            batch = rows[batch_start : batch_start + batch_size]
            ids = [r["apollo_id"] for r in batch]
            matches = bulk_match(ids)

            for idx, row in enumerate(batch):
                match = matches[idx] if idx < len(matches) else None
                current = batch_start + idx + 1
                name = row.get("contact_name", "")
                domain = row.get("src_domain", "")

                if (
                    match
                    and match.get("email")
                    and match.get("email_status") == "verified"
                ):
                    email = match["email"]
                    fn = match.get("first_name", "") or ""
                    ln = match.get("last_name", "") or ""
                    full_name = f"{fn} {ln}".strip()
                    row["apollo_email"] = email
                    row["apollo_full_name"] = full_name
                    row["apollo_last_name"] = ln
                    row["apollo_linkedin"] = match.get("linkedin_url", "") or ""
                    row["apollo_verified"] = "true"
                    found += 1
                    credits += 1
                    print(
                        f"[{current}/{len(rows)}] ✅ {full_name or name} ({domain}): {email}"
                    )
                else:
                    row["apollo_email"] = ""
                    row["apollo_full_name"] = ""
                    row["apollo_last_name"] = ""
                    row["apollo_linkedin"] = ""
                    row["apollo_verified"] = "false"
                    status = match.get("email_status") if match else "no-match"
                    print(f"[{current}/{len(rows)}] ❌ {name} ({domain}): {status}")

                writer.writerow(row)

            time.sleep(0.3)

    print()
    print("✅ Done.")
    print(f"   Revealed:  {found} ({found / len(rows) * 100:.1f}%)")
    print(f"   No match:  {len(rows) - found}")
    print(f"   Credits:   {credits} (${credits * 0.001:.3f})")


if __name__ == "__main__":
    main()
