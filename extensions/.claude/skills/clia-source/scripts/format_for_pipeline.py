"""
format_for_pipeline.py — produce gtm-mcp-compatible payloads.

This module exists as a separate import surface so other skills (e.g.
adlm-conference workflow) can reuse the same row → gtm-mcp company conversion
without re-importing pandas/argparse machinery.

The dict shape returned by `to_company_record` MUST stay aligned with what
gtm-mcp's `pipeline_save_contacts` accepts. If gtm-mcp updates its contact
schema, change this file.
"""

from datetime import datetime, timezone
from typing import Any


def to_company_record(
    name: str,
    domain: str | None,
    phone: str,
    address: str,
    city: str,
    state: str,
    zip_code: str,
    clia_number: str,
    certified_at: str | None,
    certificate_type: str,
    site_count: int,
    test_volume: int,
    classification_codes: list[str],
    segments: list[str],
    lab_type: str,
    russian_candidate: bool,
    extra: dict | None = None,
) -> dict[str, Any]:
    """
    Build a single company dict in the format gtm-mcp expects.

    `extra` is passed through verbatim — use it for tracking metadata
    (e.g. source run id, original CMS row index) without polluting the
    primary fields.
    """
    return {
        'name': name.strip(),
        'domain': domain,
        'phone': phone.strip() if phone else '',
        'address': address.strip(),
        'city': city.strip(),
        'state': state.strip(),
        'zip': zip_code.strip(),
        'clia_number': clia_number.strip(),
        'certified_at': certified_at,
        'certificate_type': certificate_type,
        'site_count': site_count,
        'test_volume': test_volume,
        'classification_codes': classification_codes,
        'segments': segments,
        'lab_type': lab_type,
        'russian_candidate': russian_candidate,
        'extra': extra or {},
    }


def build_source_payload(
    companies: list[dict],
    source_version: str,
    filter_params: dict,
) -> dict[str, Any]:
    """Wrap a list of companies into the master JSON envelope."""
    return {
        'source': 'clia_pos_file',
        'source_version': source_version,
        'filter_params': filter_params,
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'company_count': len(companies),
        'companies': companies,
    }
