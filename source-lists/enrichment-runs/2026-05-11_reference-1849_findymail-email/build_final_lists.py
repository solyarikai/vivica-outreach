#!/usr/bin/env python3
"""
Build final two company lists:
1. companies_enriched.csv — companies with at least one verified email
2. companies_not_enriched.csv — original 1849 reference labs without any email

Verified = FindyMail fm_verified=true (Apollo+FindyMail double-check),
plus the 1 found via FindyMail misses search.
"""

import csv

SOURCE = (
    "/Users/user/vivica-outreach/source-lists/segments/bucket_REFERENCE_domains.csv"
)
VERIFY = "verify_full.csv"
MISSES = "misses_searched.csv"
APOLLO_RAW = "../2026-05-11_reference-1849_apollo-people/output_with_ids.csv"

OUT_ENRICHED = "companies_enriched.csv"
OUT_NOT_ENRICHED = "companies_not_enriched.csv"
OUT_CONTACTS = "final_contacts_verified.csv"


def main():
    # Load source 1849 reference labs
    source_labs = {}
    with open(SOURCE, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            d = (row.get("domain") or "").strip().lower()
            if d:
                source_labs[d] = row

    print(f"Source labs: {len(source_labs)} unique domains (of 1849)")

    # Load verify results — keep only fm_verified=true
    verified_contacts = []
    with open(VERIFY, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("fm_verified") == "true":
                verified_contacts.append(row)
    print(f"Apollo-verified + FindyMail-verified contacts: {len(verified_contacts)}")

    # Load misses (FindyMail search) — keep only fm_email found
    misses_found = []
    with open(MISSES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("fm_email"):
                misses_found.append(row)
    print(f"FindyMail-found from Apollo misses: {len(misses_found)}")

    # Build enriched domain set
    enriched_domains = set()
    final_contacts = []
    for row in verified_contacts:
        d = (row.get("src_domain") or "").strip().lower()
        if d:
            enriched_domains.add(d)
        final_contacts.append(
            {
                "src_name": row.get("src_name", ""),
                "src_domain": row.get("src_domain", ""),
                "src_clia": row.get("src_clia", ""),
                "persona": row.get("persona", ""),
                "contact_first_name": row.get("contact_first_name", ""),
                "contact_full_name": row.get("apollo_full_name", ""),
                "contact_email": row.get("apollo_email", ""),
                "contact_title": row.get("contact_title", ""),
                "contact_linkedin": row.get("apollo_linkedin", "")
                or row.get("contact_linkedin_url", ""),
                "source": "apollo+findymail_verified",
            }
        )
    for row in misses_found:
        d = (row.get("src_domain") or "").strip().lower()
        if d:
            enriched_domains.add(d)
        final_contacts.append(
            {
                "src_name": row.get("src_name", ""),
                "src_domain": row.get("src_domain", ""),
                "src_clia": row.get("src_clia", ""),
                "persona": row.get("persona", ""),
                "contact_first_name": row.get("contact_first_name", ""),
                "contact_full_name": "",
                "contact_email": row.get("fm_email", ""),
                "contact_title": row.get("contact_title", ""),
                "contact_linkedin": row.get("contact_linkedin_url", ""),
                "source": "findymail_search",
            }
        )

    # Write final contacts (deduplicated by email)
    seen_emails = set()
    deduped_contacts = []
    for c in final_contacts:
        e = c["contact_email"].lower().strip()
        if e and e not in seen_emails:
            seen_emails.add(e)
            deduped_contacts.append(c)

    with open(OUT_CONTACTS, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(deduped_contacts[0].keys()))
        w.writeheader()
        w.writerows(deduped_contacts)

    # Companies enriched
    enriched_rows = []
    for d in sorted(enriched_domains):
        lab = source_labs.get(d, {})
        # count contacts for this domain
        contacts_here = [c for c in deduped_contacts if c["src_domain"].lower() == d]
        enriched_rows.append(
            {
                "domain": d,
                "name": lab.get("name", ""),
                "city": lab.get("city", ""),
                "state": lab.get("state", ""),
                "clia_number": lab.get("clia_number", ""),
                "lab_type": lab.get("lab_type", ""),
                "test_volume": lab.get("test_volume", ""),
                "verified_contacts_count": len(contacts_here),
                "emails": "; ".join(c["contact_email"] for c in contacts_here),
            }
        )

    with open(OUT_ENRICHED, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(enriched_rows[0].keys()))
        w.writeheader()
        w.writerows(enriched_rows)

    # Companies NOT enriched
    not_enriched_rows = []
    for d, lab in source_labs.items():
        if d in enriched_domains:
            continue
        not_enriched_rows.append(
            {
                "domain": d,
                "name": lab.get("name", ""),
                "city": lab.get("city", ""),
                "state": lab.get("state", ""),
                "clia_number": lab.get("clia_number", ""),
                "lab_type": lab.get("lab_type", ""),
                "test_volume": lab.get("test_volume", ""),
            }
        )

    with open(OUT_NOT_ENRICHED, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(not_enriched_rows[0].keys()))
        w.writeheader()
        w.writerows(not_enriched_rows)

    print()
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"  Total reference labs:        {len(source_labs)}")
    print(
        f"  Enriched (have email):       {len(enriched_domains)} "
        f"({len(enriched_domains) / len(source_labs) * 100:.1f}%)"
    )
    print(f"  NOT enriched:                {len(not_enriched_rows)}")
    print(f"  Verified contacts (dedup):   {len(deduped_contacts)}")
    print()
    print(f"  → {OUT_ENRICHED}")
    print(f"  → {OUT_NOT_ENRICHED}")
    print(f"  → {OUT_CONTACTS}")


if __name__ == "__main__":
    main()
