---
name: lims-detector
description: Detect which LIMS vendor a specific clinical lab is currently using, by inspecting their patient portal iframe, JavaScript bundles, and job postings. Use this skill during the company-qualification phase whenever a target lab has been identified, BEFORE the email-sequence skill writes the message — knowing the current LIMS unlocks competitor-conquest sequences with vendor-specific pain quotes from the lims-pain-extractor corpus. Triggers include phrases like "what LIMS does X use", "detect their LIMS", "which system is this lab on", or any mention of patient portal inspection, iframe detection, or LIMS fingerprinting.
---

# lims-detector — fingerprint a lab's current LIMS vendor

## Why this exists

Per Chris Hilinsky's note in the kick-off call:

> Determining which LIMS a lab uses is possible via the website — patient portal in the top-right corner. When clicked, an iframe opens. Right-click → inspect element → see the hosting.

This is the cheapest, highest-fidelity way to know what we're up against. Once we know vendor X is in use, the entire personalization machinery activates:
- competitor-specific pain quote from `lims-pain-extractor` corpus
- competitor-specific battle card lookup
- migration-framework angle (three-phase mirror→proxy→decommission)
- "we hear from former <X> customers..." social proof

Without this skill, the email is generic. With it, the email is precision-guided.

## When to use this skill

In the standard gtm-mcp pipeline:

```
Apollo / clia-source  →  scrape websites  →  qualify
                                                 │
                            ┌────────────────────┤
                            │   THIS SKILL       │
                            │   runs here        │
                            └────────────────────┘
                                                 │
                                                 ▼
                                            people enrichment
                                                 │
                                                 ▼
                                       email-sequence
                                       (uses detected vendor)
```

Run this skill on EACH qualified target lab, not on the full Apollo result set
— it makes targeted requests per company, costs scale with batch size.

## Detection signals (in priority order)

### Signal 1: Patient portal iframe src

The patient portal is usually a button or link in the top-right of the lab's homepage. When clicked, it opens an iframe pointing to the LIMS vendor's hosted portal. The iframe `src` attribute reveals the vendor:

| Iframe src pattern | Vendor |
|---|---|
| `*.labware.com/`, `*.labware-online.com/` | LabWare |
| `*.labvantage.com/`, `*.lvportal.com/` | LabVantage |
| `*.qbench.com/`, `portal.qbench.io/` | QBench |
| `*.creliohealth.com/`, `*.creliohealth.in/` | CrelioHealth |
| `*.ligolab.com/`, `portal.ligolab.com/` | LigoLab |
| `*.clinisys.com/`, `*.sunquestinfo.com/` | Clinisys (incl. legacy Sunquest) |
| `*.cloudlims.com/` | CloudLIMS |
| `*.lims.net/`, `*.limseo.eu/` | lims.net / LiMSEO (a.k.a. JTO) |

Full pattern list lives in `scripts/detect_lims.py` `IFRAME_PATTERNS`.

### Signal 2: JavaScript bundle URLs

If the patient portal isn't a direct iframe but is a JS-rendered widget, the
loaded scripts often carry vendor identifiers:

```
<script src="//cdn.qbench.com/widget.js"></script>
<link rel="stylesheet" href="https://static.creliohealth.com/portal.css"/>
```

These give the same vendor signal even when the iframe is absent.

### Signal 3: Result-portal subdomain

Some labs run the LIMS as a subdomain on their own domain (cname'd to the
vendor). DNS lookup of `results.<lab-domain>.com` or `portal.<lab-domain>.com`
often resolves to a vendor-controlled host:

```
results.acmelab.com  →  CNAME  →  acmelab.creliohealth.com
```

This is a reliable signal but requires DNS access (we use a free DNS-over-HTTPS
provider — no API key needed).

### Signal 4: Job posting language

If the lab is hiring lab IT staff, the posting often names the system explicitly:

> "Experience required: 2+ years LabWare LIMS administration"

We scrape job posts from LinkedIn, Indeed, and the lab's own career page when
the previous signals are inconclusive. This is a Signal 4 (low priority, slow)
fallback only.

### Signal 5: Custom self-hosted ("samopis")

Per the kick-off call (Andrew's note):

> 3-5 customers run a custom-built LIMS — they pay $800 to a developer who
> writes and maintains the system. Cheap, flexible, but doesn't scale.

If signals 1-3 turn up no vendor pattern AND the patient portal looks home-grown
(no third-party CDN, custom URL on lab's own domain), tag the lab as
`custom_self_hosted`. Vivica's value prop for this segment is different:
"professional cloud LIMS without the maintenance burden".

## Output

This skill enriches each company record with a `current_lims` field:

```json
{
  "name": "ACME Diagnostic Lab",
  "domain": "acmelab.com",
  "current_lims": {
    "vendor": "labware",
    "vendor_display_name": "LabWare LIMS",
    "confidence": 0.92,
    "detected_via": ["iframe_src"],
    "evidence": [
      {
        "signal": "iframe_src",
        "value": "https://acmelab.labware-online.com/portal",
        "scraped_from": "https://acmelab.com/patient-portal"
      }
    ],
    "detected_at": "2026-05-10T14:23:00Z"
  }
}
```

Possible `vendor` values:
- One of the 8 tracked vendors (labware, labvantage, qbench, creliohealth, ligolab, clinisys, cloudlims, lims_net)
- `custom_self_hosted` — home-grown system
- `unknown` — couldn't detect, leave for human review
- `none_detected` — no patient portal found at all (small POL labs without online presence)

## Confidence scoring

| Signals matched | Confidence |
|---|---|
| Signal 1 only | 0.85 |
| Signal 1 + Signal 2 | 0.95 |
| Signal 2 only | 0.65 |
| Signal 3 only | 0.75 |
| Signal 4 only | 0.55 |
| All four | 0.99 |

Threshold for trusting vendor in email-sequence: `confidence >= 0.7`. Below that,
fall back to a generic sequence (no vendor-specific pain quote).

## Workflow

```
1. Read company.domain (must exist; if null, skip — caller's job to enrich)
2. Try to find the patient portal page:
   - GET /patient-portal, /portal, /results, /lab-results
   - parse HTML, find <iframe>, <a href="...">, button targets
3. If iframe found, extract src → match against IFRAME_PATTERNS
4. If JS bundles found, match script srcs against JS_BUNDLE_PATTERNS
5. If still ambiguous, DNS lookup results.<domain>, portal.<domain>
6. If still unknown AND we have job postings on file (career page scrape),
   parse for vendor mentions
7. Compute confidence, write back to company record
8. If unknown, tag for human review (Andrew's worth a $100 Amazon gift card
   for a 30-min interview per kick-off call)
```

## Privacy & rate limiting

- We make at most 3 HTTP requests per lab (homepage + portal + DNS)
- We do NOT persist scraped HTML beyond extracting the LIMS signal
- We respect robots.txt
- We use the same Apify proxy that gtm-mcp's scrape_website uses, when available

## Usage

```bash
# Detect for a single domain
python scripts/detect_lims.py --domain acmelab.com

# Batch detect over a list
python scripts/detect_lims.py --batch ~/.gtm-mcp/projects/vivica/qualified.json

# Re-run only on companies whose previous detection was 'unknown'
python scripts/detect_lims.py --batch <file> --only-unknown
```

## What this skill does NOT do

- Does NOT extract people / emails (use Apollo via gtm-mcp)
- Does NOT write emails (that's `email-sequence` after we tag the vendor)
- Does NOT pull G2 reviews of detected vendor (that's `lims-pain-extractor`)
- Does NOT detect lab specialization (that's `clia-source` from CLIA codes)

## See also

- `scripts/detect_lims.py` — full pattern list
- `../lims-pain-extractor/SKILL.md` — what we do once we know the vendor
- `../../reference/battle-cards/` — vendor × persona matchups
