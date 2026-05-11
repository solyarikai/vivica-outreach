#!/usr/bin/env python3
"""
Single source of truth for reference-segment enrichment funnel.

Reads run artifacts + CMS source-of-truth, recomputes every funnel metric
from scratch, and prints a canonical report. Other documents (analytics.md,
intake-report-vivica-2026-05.md) must derive numbers from this output, not
the other way around.

Usage:
    python3 funnel_recount.py

Inputs (relative to repo root):
    source-lists/segments/bucket_REFERENCE_domains.csv
    source-lists/enrichment-runs/2026-05-11_reference-1849_findymail-email/
        companies_enriched.csv
        companies_not_enriched.csv
        final_contacts_verified.csv
"""

import csv
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
RUN = REPO / "source-lists/enrichment-runs/2026-05-11_reference-1849_findymail-email"
CMS = REPO / "source-lists/segments/bucket_REFERENCE_domains.csv"


def load(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def norm(d):
    return (d or "").lower().strip()


def main():
    cms = load(CMS)
    enriched = load(RUN / "companies_enriched.csv")
    not_enriched = load(RUN / "companies_not_enriched.csv")
    contacts = load(RUN / "final_contacts_verified.csv")

    # CLIA records layer
    cms_total = len(cms)
    cms_with_domain = [r for r in cms if norm(r["domain"])]
    cms_no_domain = cms_total - len(cms_with_domain)

    # Unique companies (domain dedup of CMS records-with-domain)
    cms_domains = Counter(norm(r["domain"]) for r in cms_with_domain)
    unique_companies = len(cms_domains)

    # Apollo people-search split (from build_final_lists output)
    enriched_domains = {norm(r["domain"]) for r in enriched}
    not_enriched_domains = {norm(r["domain"]) for r in not_enriched}

    # Verified-contacts layer
    final_domains = {norm(r["src_domain"]) for r in contacts if r["src_domain"]}
    total_contacts = len(contacts)
    unique_companies_with_contacts = len(final_domains)

    # CLIA records "covered" — records whose domain has a verified contact
    covered_records = [r for r in cms_with_domain if norm(r["domain"]) in final_domains]
    n_covered = len(covered_records)

    # Records per covered company (chain inflation)
    covered_per_company = Counter()
    for r in covered_records:
        covered_per_company[norm(r["domain"])] += 1

    chains = {d: n for d, n in covered_per_company.items() if n >= 5}
    independents = {d: n for d, n in covered_per_company.items() if n == 1}
    midsize = {d: n for d, n in covered_per_company.items() if 2 <= n <= 4}

    # Persona breakdown
    personas = Counter(c["persona"] for c in contacts)

    # ---- Output ----
    print("=" * 70)
    print("REFERENCE SEGMENT ENRICHMENT FUNNEL — recount from raw data")
    print("=" * 70)

    print("\n## Layer 1 — CLIA records (locations)")
    print(f"  CMS reference rows                      {cms_total:>6}")
    print(f"  ├─ with domain                          {len(cms_with_domain):>6}")
    print(f"  └─ no domain (skipped)                  {cms_no_domain:>6}")

    print("\n## Layer 2 — Unique companies (dedup by domain)")
    print(f"  Unique domains in CMS                   {unique_companies:>6}")
    print(f"  ├─ Apollo found people (enriched)       {len(enriched_domains):>6}")
    print(f"  └─ Apollo dark (no people found)        {len(not_enriched_domains):>6}")
    print(
        f"     sanity: {len(enriched_domains)} + {len(not_enriched_domains)} = "
        f"{len(enriched_domains) + len(not_enriched_domains)} (expect {unique_companies})"
    )

    print("\n## Layer 3 — Final verified contacts")
    print(f"  Verified contacts (after SMTP + dedup)  {total_contacts:>6}")
    print(
        f"  Unique companies with ≥1 contact        {unique_companies_with_contacts:>6}"
    )
    drop = len(enriched_domains) - unique_companies_with_contacts
    print(
        f"  ├─ Lost between enriched→verified       {drop:>6}  "
        f"(emails failed SMTP or all dedup'd as chain duplicates)"
    )

    print("\n## CLIA records covered (records-level)")
    print(
        f"  Records whose domain ∈ verified set     {n_covered:>6}  "
        f"({n_covered / cms_total * 100:.1f}% of {cms_total})"
    )
    avg = n_covered / unique_companies_with_contacts
    print(f"  Avg CLIA records per covered company    {avg:>6.2f}")

    print("\n## Chain vs independent breakdown (of 270 covered companies)")
    print(f"  Independents (1 CLIA record)            {len(independents):>6}")
    print(f"  Mid-size (2-4 records)                  {len(midsize):>6}")
    print(f"  Chains (5+ records)                     {len(chains):>6}")
    if chains:
        print("  Top 10 chains by record count:")
        for d, n in sorted(chains.items(), key=lambda x: -x[1])[:10]:
            print(f"    {n:>4}  {d}")

    print("\n## Persona distribution (verified contacts)")
    for p, n in personas.most_common():
        print(f"  {p:<25} {n:>4}  ({n / total_contacts * 100:.1f}%)")

    print("\n## Addressable pool sanity")
    addr = len(independents) + len(midsize)
    print(
        f"  Realistic addressable companies         {addr:>6}  "
        f"(independents + mid-size; chains ≠ buyers of Vivica)"
    )
    print(
        f"  Dark labs (Apollo found 0 people)       {len(not_enriched_domains):>6}  "
        f"← second-pass enrichment target"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()
