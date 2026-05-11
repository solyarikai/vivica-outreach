#!/usr/bin/env python3
"""
Apollo People Search — find CEO/Owner/Lab Director contacts for clinical labs

Usage: python3 apollo_people_search.py <input_csv> <output_csv> [--test N]

Requirements:
- GTM_MCP_APOLLO_API_KEY environment variable set (from ~/.gtm-mcp/.env)
- Input CSV with: name, domain, city, state, clia_number

Output CSV will contain:
- src_name, src_domain, src_clia (source)
- persona, contact_name, contact_email, contact_title, contact_linkedin_url, contact_phone
"""

import csv
import sys
import os
import json
import time
import urllib.request
import urllib.error


def get_apollo_key():
    key = os.environ.get("GTM_MCP_APOLLO_API_KEY")
    if not key:
        raise ValueError("GTM_MCP_APOLLO_API_KEY not set. Add to ~/.gtm-mcp/.env")
    return key


def query_apollo_domain(domain, api_key):
    """
    Query Apollo for people at a domain, optionally filtered by persona keywords

    Personas:
    - CEO/Owner: CEO, President, Founder, Owner, Managing Partner
    - Lab Director: Lab Director, Lab Manager, Director of Operations, Operations Manager
    - Medical Director: Medical Director, CLIA Director, Pathologist, Director of Pathology
    """
    url = "https://api.apollo.io/api/v1/mixed_people/api_search"

    payload = {
        "q_organization_domains": domain,
        "page": 1,
        "per_page": 25,
        "person_seniorities": ["owner", "founder", "c_suite", "vp", "head", "director"],
    }

    headers = {"Content-Type": "application/json", "X-Api-Key": api_key}

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("people", [])

    except urllib.error.HTTPError as e:
        if e.code == 402:
            print("⚠️  Apollo credit exhausted (402). Cannot continue.")
            raise
        elif e.code == 429:
            print("⚠️  Rate limited (429). Waiting 10s...")
            time.sleep(10)
            return []
        else:
            print(f"❌ Apollo API error {e.code}: {e.reason}")
            return []
    except Exception as e:
        print(f"❌ Error querying Apollo: {e}")
        return []


def filter_persona_match(person, persona_keywords):
    """Check if person's title matches persona keywords"""
    title = (person.get("title") or "").lower()
    keywords = [k.lower() for k in persona_keywords]
    return any(kw in title for kw in keywords)


def get_email_from_person(person):
    """Extract email from Apollo person record"""
    # Apollo stores email in various places depending on the endpoint
    if person.get("email"):
        return person.get("email")
    if person.get("email_address"):
        return person.get("email_address")
    # Email may not be included in list results; only has_email flag
    return None


def extract_contacts_by_persona(domain, people, api_key):
    """
    Extract one contact per persona type from Apollo people results

    Returns: dict with keys 'ceo_owner', 'lab_director', 'medical_director'
    """
    personas = {
        "ceo_owner": {
            "keywords": ["ceo", "president", "founder", "owner", "managing partner"],
            "data": None,
        },
        "lab_director": {
            "keywords": [
                "lab director",
                "lab manager",
                "director of operations",
                "operations manager",
            ],
            "data": None,
        },
        "medical_director": {
            "keywords": [
                "medical director",
                "clia director",
                "pathologist",
                "director of pathology",
            ],
            "data": None,
        },
    }

    # Try to match people to personas
    for person in people:
        for persona_key, persona_info in personas.items():
            if persona_info["data"] is None:  # not yet filled
                if filter_persona_match(person, persona_info["keywords"]):
                    persona_info["data"] = person
                    break  # move to next person

    return personas


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_csv> <output_csv> [--test N]")
        print("  --test N: run on first N companies only")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    test_mode = False
    test_limit = 0

    if "--test" in sys.argv:
        test_idx = sys.argv.index("--test")
        test_limit = int(sys.argv[test_idx + 1])
        test_mode = True

    api_key = get_apollo_key()

    # Read input
    companies = []
    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if test_mode and i >= test_limit:
                break
            companies.append(row)

    print(f"📋 Loaded {len(companies)} companies")
    print("🔑 Using Apollo API")
    print(f"💾 Output: {output_csv}")
    print()

    # Prepare output
    output_rows = []

    # Process each company
    for i, company in enumerate(companies, 1):
        name = company.get("name", "")
        domain = company.get("domain", "")
        clia = company.get("clia_number", "")

        if not domain:
            print(f"[{i}/{len(companies)}] ⏭️  {name}: no domain, skipping")
            continue

        print(f"[{i}/{len(companies)}] 🔍 {name} ({domain})")

        # Query Apollo for this domain
        people = query_apollo_domain(domain, api_key)

        if not people:
            print("             ❌ No people found")
            continue

        print(f"             ✅ Found {len(people)} people")

        # Extract personas
        personas = extract_contacts_by_persona(domain, people, api_key)

        for persona_type, persona_info in personas.items():
            person = persona_info["data"]
            if person:
                email = get_email_from_person(person)
                output_rows.append(
                    {
                        "src_name": name,
                        "src_domain": domain,
                        "src_clia": clia,
                        "persona": persona_type,
                        "apollo_id": person.get("id", ""),
                        "contact_name": f"{person.get('first_name', '')} {person.get('last_name_obfuscated', '')}".strip(),
                        "contact_first_name": person.get("first_name", ""),
                        "contact_email": email or "(require direct fetch)",
                        "contact_title": person.get("title", ""),
                        "contact_linkedin_url": person.get("linkedin_url", ""),
                        "contact_phone": "(require direct fetch)"
                        if person.get("has_direct_phone") == "Yes"
                        else "",
                    }
                )
                print(
                    f"             ✏️  {persona_type}: {person.get('first_name')} (${email or 'email pending'})"
                )

        # Rate limiting
        time.sleep(0.5)

    # Write output
    if output_rows:
        with open(output_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "src_name",
                    "src_domain",
                    "src_clia",
                    "persona",
                    "apollo_id",
                    "contact_name",
                    "contact_first_name",
                    "contact_email",
                    "contact_title",
                    "contact_linkedin_url",
                    "contact_phone",
                ],
            )
            writer.writeheader()
            writer.writerows(output_rows)

        print(f"\n✅ Done. {len(output_rows)} contacts extracted to {output_csv}")
    else:
        print("\n❌ No contacts found")


if __name__ == "__main__":
    main()
