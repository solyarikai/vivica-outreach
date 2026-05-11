#!/usr/bin/env python3
"""
detect_lims.py — fingerprint a clinical lab's current LIMS vendor.

Workflow per lab:
  1. Find the patient portal page (try common paths)
  2. Extract iframe srcs and script srcs
  3. Match against IFRAME_PATTERNS and JS_BUNDLE_PATTERNS
  4. Optional: DNS lookup of result/portal subdomains
  5. Compute confidence, write current_lims field

Usage:
    python detect_lims.py --domain acmelab.com
    python detect_lims.py --batch ~/.gtm-mcp/projects/vivica/qualified.json
    python detect_lims.py --batch <file> --only-unknown
"""

import argparse
import json
import re
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse


# ────────────────────────────────────────────────────────────────────────
#  Vendor patterns
# ────────────────────────────────────────────────────────────────────────

IFRAME_PATTERNS: list[tuple[str, str, str]] = [
    # (regex, slug, display_name)
    (r'\.labware(?:-online)?\.com', 'labware', 'LabWare LIMS'),
    (r'\.labvantage\.com|\.lvportal\.com', 'labvantage', 'LabVantage'),
    (r'\.qbench\.(?:com|io)', 'qbench', 'QBench'),
    (r'\.creliohealth\.(?:com|in)', 'creliohealth', 'CrelioHealth'),
    (r'\.ligolab\.com', 'ligolab', 'LigoLab'),
    (r'\.clinisys\.com|\.sunquestinfo\.com', 'clinisys', 'Clinisys'),
    (r'\.cloudlims\.com', 'cloudlims', 'CloudLIMS'),
    (r'\.lims\.net|\.limseo\.eu', 'lims_net', 'lims.net'),
]

JS_BUNDLE_PATTERNS: list[tuple[str, str, str]] = [
    (r'cdn\.qbench\.com|qbench\.io/widget', 'qbench', 'QBench'),
    (r'static\.creliohealth\.com', 'creliohealth', 'CrelioHealth'),
    (r'cdn\.cloudlims\.com', 'cloudlims', 'CloudLIMS'),
    (r'assets\.labware\.com', 'labware', 'LabWare LIMS'),
    (r'cdn\.ligolab\.com', 'ligolab', 'LigoLab'),
]

# Common path candidates where a patient portal lives
PORTAL_PATH_CANDIDATES = [
    '/patient-portal', '/portal', '/results', '/lab-results',
    '/patient', '/login', '/myresults', '/patient-results',
]

# Subdomains to try DNS-CNAME lookup on
DNS_SUBDOMAIN_CANDIDATES = ['results', 'portal', 'lab', 'patient', 'lims']


# ────────────────────────────────────────────────────────────────────────
#  HTTP & DNS
# ────────────────────────────────────────────────────────────────────────

def fetch(url: str, timeout: int = 10) -> str:
    """GET a URL, return body text or empty string on failure."""
    try:
        import requests  # type: ignore
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; vivica-lims-detector/1.0)'}
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass
    return ''


def cname_lookup(hostname: str) -> str | None:
    """
    Resolve CNAME chain for a hostname. Falls back to A-record host string.
    Returns None on resolution failure.
    """
    try:
        # socket doesn't expose CNAMEs directly. We use getaddrinfo and
        # also peek at canonical name when available.
        info = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM, 0, socket.AI_CANONNAME)
        if info:
            canonical = info[0][3]
            if canonical and canonical != hostname:
                return canonical
    except socket.gaierror:
        return None
    return None


# ────────────────────────────────────────────────────────────────────────
#  Detection signals
# ────────────────────────────────────────────────────────────────────────

def find_portal_page(domain: str) -> tuple[str | None, str]:
    """
    Try the homepage first, then well-known portal paths.
    Returns (portal_url, html) or (None, '').
    """
    base = f'https://{domain}'
    home = fetch(base)
    if home:
        # Search homepage for portal links
        link_match = re.search(
            r'<a[^>]+href="([^"]*(?:portal|results|patient)[^"]*)"',
            home, re.IGNORECASE,
        )
        if link_match:
            portal_url = urljoin(base, link_match.group(1))
            portal_html = fetch(portal_url)
            if portal_html:
                return portal_url, portal_html

    # Direct path probe
    for path in PORTAL_PATH_CANDIDATES:
        url = base + path
        html = fetch(url)
        if html and len(html) > 500:
            return url, html

    # Fall back to homepage if non-empty
    if home:
        return base, home
    return None, ''


def detect_via_iframe(html: str) -> tuple[str, str, str] | None:
    """Match iframe src patterns. Returns (slug, display_name, iframe_src) or None."""
    iframes = re.findall(r'<iframe[^>]+src="([^"]+)"', html, re.IGNORECASE)
    for src in iframes:
        for pattern, slug, display in IFRAME_PATTERNS:
            if re.search(pattern, src, re.IGNORECASE):
                return slug, display, src
    return None


def detect_via_js_bundle(html: str) -> tuple[str, str, str] | None:
    """Match script/link srcs. Returns (slug, display_name, src) or None."""
    srcs = re.findall(r'<(?:script|link)[^>]+(?:src|href)="([^"]+)"', html, re.IGNORECASE)
    for src in srcs:
        for pattern, slug, display in JS_BUNDLE_PATTERNS:
            if re.search(pattern, src, re.IGNORECASE):
                return slug, display, src
    return None


def detect_via_dns(domain: str) -> tuple[str, str, str] | None:
    """Try CNAME lookups on common LIMS subdomains."""
    for sub in DNS_SUBDOMAIN_CANDIDATES:
        host = f'{sub}.{domain}'
        cname = cname_lookup(host)
        if not cname:
            continue
        for pattern, slug, display in IFRAME_PATTERNS:
            if re.search(pattern, cname, re.IGNORECASE):
                return slug, display, f'CNAME {host} → {cname}'
    return None


def looks_self_hosted(html: str, domain: str) -> bool:
    """Heuristic: portal exists but no third-party CDN, runs on lab's own domain."""
    if not html:
        return False
    iframes = re.findall(r'<iframe[^>]+src="([^"]+)"', html, re.IGNORECASE)
    for src in iframes:
        host = urlparse(src).hostname or ''
        if domain not in host and host not in ('', 'about:blank'):
            return False  # third-party iframe → not self-hosted
    # If we see lab-specific paths but no vendor signal, likely self-hosted
    return bool(re.search(r'patient|results|login', html, re.IGNORECASE))


# ────────────────────────────────────────────────────────────────────────
#  Main detection
# ────────────────────────────────────────────────────────────────────────

CONFIDENCE_TABLE = {
    ('iframe',): 0.85,
    ('iframe', 'js'): 0.95,
    ('js',): 0.65,
    ('dns',): 0.75,
    ('iframe', 'dns'): 0.92,
    ('iframe', 'js', 'dns'): 0.99,
    ('iframe', 'js', 'dns', 'jobs'): 0.99,
}


def detect_lims_for_domain(domain: str) -> dict:
    """Run full detection workflow on one domain. Returns current_lims dict."""
    portal_url, html = find_portal_page(domain)

    if not html:
        return {
            'vendor': 'none_detected',
            'vendor_display_name': None,
            'confidence': 0.0,
            'detected_via': [],
            'evidence': [],
            'detected_at': datetime.now(timezone.utc).isoformat(),
            'note': 'No portal page reachable',
        }

    detections = []
    evidence = []

    iframe_hit = detect_via_iframe(html)
    if iframe_hit:
        detections.append('iframe')
        evidence.append({
            'signal': 'iframe_src',
            'value': iframe_hit[2],
            'scraped_from': portal_url,
        })

    js_hit = detect_via_js_bundle(html)
    if js_hit:
        detections.append('js')
        evidence.append({
            'signal': 'js_bundle',
            'value': js_hit[2],
            'scraped_from': portal_url,
        })

    # DNS only if iframe/js didn't already give us a clear answer
    dns_hit = None
    if not iframe_hit:
        dns_hit = detect_via_dns(domain)
        if dns_hit:
            detections.append('dns')
            evidence.append({
                'signal': 'dns_cname',
                'value': dns_hit[2],
                'scraped_from': None,
            })

    primary = iframe_hit or js_hit or dns_hit

    if primary:
        slug, display, _ = primary
        confidence = CONFIDENCE_TABLE.get(tuple(detections), 0.7)
        return {
            'vendor': slug,
            'vendor_display_name': display,
            'confidence': confidence,
            'detected_via': detections,
            'evidence': evidence,
            'detected_at': datetime.now(timezone.utc).isoformat(),
        }

    if looks_self_hosted(html, domain):
        return {
            'vendor': 'custom_self_hosted',
            'vendor_display_name': 'Custom / self-hosted',
            'confidence': 0.6,
            'detected_via': ['heuristic'],
            'evidence': [{'signal': 'no_vendor_iframe', 'scraped_from': portal_url}],
            'detected_at': datetime.now(timezone.utc).isoformat(),
        }

    return {
        'vendor': 'unknown',
        'vendor_display_name': None,
        'confidence': 0.0,
        'detected_via': [],
        'evidence': [],
        'detected_at': datetime.now(timezone.utc).isoformat(),
    }


# ────────────────────────────────────────────────────────────────────────
#  CLI
# ────────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--domain', help='Single domain to detect')
    g.add_argument('--batch', type=Path, help='JSON file with companies array')
    p.add_argument('--only-unknown', action='store_true', help='In batch mode, re-run only on companies whose previous detection was unknown')
    p.add_argument('--rate-limit', type=float, default=0.5, help='Sleep between domains (seconds)')
    p.add_argument('--output', type=Path, help='Output JSON path (default: overwrite input in batch mode)')
    return p.parse_args()


def main():
    args = parse_args()

    if args.domain:
        result = detect_lims_for_domain(args.domain)
        print(json.dumps(result, indent=2))
        return

    # Batch mode
    with args.batch.open() as f:
        data = json.load(f)
    companies = data['companies'] if 'companies' in data else data
    print(f'Processing {len(companies)} companies ...', file=sys.stderr)

    for i, c in enumerate(companies):
        if args.only_unknown:
            existing = c.get('current_lims', {}).get('vendor')
            if existing not in (None, 'unknown', 'none_detected'):
                continue
        if not c.get('domain'):
            continue
        print(f"  [{i+1}/{len(companies)}] {c['domain']} ...", file=sys.stderr)
        c['current_lims'] = detect_lims_for_domain(c['domain'])
        time.sleep(args.rate_limit)

    out_path = args.output or args.batch
    if 'companies' in data:
        data['companies'] = companies
    else:
        data = companies
    with out_path.open('w') as f:
        json.dump(data, f, indent=2)
    print(f'Wrote {out_path}', file=sys.stderr)


if __name__ == '__main__':
    main()
