#!/usr/bin/env python3
"""
filter_pos_file.py — convert CMS POS file into Vivica ICP company stream.

Reads the raw CSV from <https://qcor.cms.gov> bulk export, applies the Vivica
ICP filter (active + Compliance/Accreditation + non-hospital + has phone +
recent), tags each row with Vivica segments and lab type, and writes outputs
into the gtm-mcp project workspace in the format downstream tools expect.

Usage:
    python filter_pos_file.py \\
        --input /path/to/POS_File_CLIA_Q1_2026.csv \\
        --output ~/.gtm-mcp/projects/vivica/sources/ \\
        --since 2025-01-01 \\
        [--segment toxicology] \\
        [--max-results 10000]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from classify_by_clia_code import (
    classify_segments,
    classify_facility_type,
    infer_lab_type,
    mark_russian_candidate,
)

# CMS POS file column groups we actually use
USED_COLUMNS = [
    'FAC_NAME', 'ST_ADR', 'CITY_NAME', 'STATE_CD', 'ZIP_CD', 'PHNE_NUM',
    'CRTFCT_TYPE_CD', 'CRTFCTN_DT', 'PGM_TRMNTN_CD',
    'HOSP_LAB_EXCPTN_SW', 'PRVDR_NUM',
    'LAB_SITE_CNT', 'FORM_116_TEST_VOL_CNT',
    'GNRL_FAC_TYPE_CD',
] + [f'CLIA_LAB_CLASSIFICATION_CD_{i}' for i in range(1, 11)]

CERT_TYPE_NAMES = {
    '1': 'Compliance',
    '2': 'Waiver',
    '3': 'PPMP',
    '4': 'Accreditation',
    '9': 'Registration',
}


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--input', required=True, type=Path, help='Path to POS file CSV')
    p.add_argument('--output', required=True, type=Path, help='Output directory (typically ~/.gtm-mcp/projects/vivica/sources/)')
    p.add_argument('--since', default='2025-01-01', help='Only labs certified on or after this date (YYYY-MM-DD). Default 2025-01-01.')
    p.add_argument('--segment', help='Restrict output to one segment (e.g. toxicology). Default: all segments.')
    p.add_argument('--max-results', type=int, help='Cap output at N labs (for testing).')
    p.add_argument('--include-hospital-labs', action='store_true', help='Override default exclusion of hospital labs. Use with care.')
    return p.parse_args()


def load_pos_file(path: Path) -> pd.DataFrame:
    print(f'Loading {path} ...', file=sys.stderr)
    # Only read columns we actually need — saves memory on the 676k row file
    df = pd.read_csv(path, dtype=str, low_memory=False, usecols=USED_COLUMNS)
    print(f'  loaded {len(df):,} rows', file=sys.stderr)
    return df


def apply_icp_filter(df: pd.DataFrame, since: str, include_hospital: bool) -> pd.DataFrame:
    """Apply the standard Vivica ICP filter."""
    print(f'Applying ICP filter (since={since}, hospitals={"YES" if include_hospital else "no"}) ...', file=sys.stderr)

    df = df.copy()
    df['_cert_dt'] = pd.to_datetime(df['CRTFCTN_DT'], format='%Y%m%d', errors='coerce')

    cond = (
        # active
        (df['PGM_TRMNTN_CD'] == '00') &
        # compliance or accreditation only
        (df['CRTFCT_TYPE_CD'].isin(['1', '4'])) &
        # has phone (10+ digits)
        (df['PHNE_NUM'].notna()) &
        (df['PHNE_NUM'].astype(str).str.len() >= 10) &
        # certified on or after --since
        (df['_cert_dt'] >= pd.Timestamp(since))
    )

    if not include_hospital:
        cond &= (df['HOSP_LAB_EXCPTN_SW'] == 'N')

    filtered = df[cond].copy()
    print(f'  {len(filtered):,} labs match ICP', file=sys.stderr)
    return filtered


def collect_classification_codes(row) -> list:
    """Extract all non-empty CLIA classification codes from one row."""
    codes = []
    for i in range(1, 11):
        v = row.get(f'CLIA_LAB_CLASSIFICATION_CD_{i}')
        if v and str(v).strip() not in ('', '00', 'nan'):
            codes.append(str(v).strip())
    return codes


def row_to_company(row) -> dict:
    """Convert one DataFrame row to a gtm-mcp-compatible company dict."""
    codes = collect_classification_codes(row)
    segments = classify_segments(codes)
    gnrl_fac_type = str(row.get('GNRL_FAC_TYPE_CD') or '').strip().zfill(2)
    bucket, facility_name = classify_facility_type(gnrl_fac_type)
    lab_type = infer_lab_type(
        name=str(row.get('FAC_NAME', '')),
        site_count=int(row.get('LAB_SITE_CNT') or 0),
        test_volume=int(row.get('FORM_116_TEST_VOL_CNT') or 0),
        gnrl_fac_type_cd=gnrl_fac_type,
    )
    russian_candidate = mark_russian_candidate(
        name=str(row.get('FAC_NAME', '')),
        state=str(row.get('STATE_CD', '')),
    )

    cert_dt = row.get('_cert_dt')
    cert_dt_str = cert_dt.strftime('%Y-%m-%d') if pd.notna(cert_dt) else None

    return {
        'name': str(row.get('FAC_NAME', '')).strip(),
        'domain': None,  # CMS doesn't have this — populated downstream
        'phone': str(row.get('PHNE_NUM', '')).strip(),
        'address': str(row.get('ST_ADR', '')).strip(),
        'city': str(row.get('CITY_NAME', '')).strip(),
        'state': str(row.get('STATE_CD', '')).strip(),
        'zip': str(row.get('ZIP_CD', '')).strip(),
        'clia_number': str(row.get('PRVDR_NUM', '')).strip(),
        'certified_at': cert_dt_str,
        'certificate_type': CERT_TYPE_NAMES.get(str(row.get('CRTFCT_TYPE_CD', '')), 'Unknown'),
        'site_count': int(row.get('LAB_SITE_CNT') or 0),
        'test_volume': int(row.get('FORM_116_TEST_VOL_CNT') or 0),
        'classification_codes': codes,
        'segments': segments,
        'lab_type': lab_type,
        'cms_facility_type_code': gnrl_fac_type,
        'cms_facility_type_name': facility_name,
        'russian_candidate': russian_candidate,
    }


def write_outputs(companies: list, args, source_quarter: str):
    """Write the main JSON + per-segment CSV files."""
    out_dir: Path = args.output
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. master JSON (everything, even UNSUITABLE — caller may want to inspect)
    master_path = out_dir / f'clia_{source_quarter}.json'
    payload = {
        'source': 'clia_pos_file',
        'source_version': source_quarter,
        'filter_params': {
            'since': args.since,
            'certificate_types': ['1', '4'],
            'exclude_hospital_labs': not args.include_hospital_labs,
            'min_phone_length': 10,
            'restricted_segment': args.segment,
        },
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'company_count': len(companies),
        'companies': companies,
    }
    with master_path.open('w') as f:
        json.dump(payload, f, indent=2, default=str)
    print(f'Wrote master JSON: {master_path} ({len(companies):,} companies)', file=sys.stderr)

    # 2. per-bucket CSVs — these are what /launch consumes per segment
    seg_dir = out_dir / f'clia_{source_quarter}_segmented'
    seg_dir.mkdir(exist_ok=True)

    by_bucket: dict[str, list[dict]] = {}
    by_specialty: dict[str, list[dict]] = {}
    russian_candidates: list[dict] = []

    for c in companies:
        # 2a. by Vivica facility bucket (POL / PSC / REFERENCE / UNSUITABLE / OTHER)
        bucket = c['lab_type']
        by_bucket.setdefault(bucket, []).append(c)

        # 2b. by specialty (mostly 'unspecified' due to CMS data sparsity)
        for s in c['segments']:
            by_specialty.setdefault(s, []).append(c)

        # 2c. russian-speaking candidates (cross-cuts buckets)
        if c['russian_candidate']:
            russian_candidates.append(c)

    # Write facility-bucket CSVs
    print('\nFacility buckets:', file=sys.stderr)
    for bucket, rows in sorted(by_bucket.items()):
        if bucket == 'UNSUITABLE':
            print(f'  {bucket:<12} {len(rows):>5,} (excluded — hospitals/prison/pharmacy/insurance)', file=sys.stderr)
            continue
        csv_path = seg_dir / f'bucket_{bucket}.csv'
        df_out = _to_csv_friendly(rows)
        df_out.to_csv(csv_path, index=False)
        print(f'  {bucket:<12} {len(rows):>5,} → {csv_path.name}', file=sys.stderr)

    # Write specialty CSVs (if non-trivial)
    significant_specialties = {s: r for s, r in by_specialty.items() if s != 'unspecified' and len(r) >= 5}
    if significant_specialties:
        print('\nSpecialty segments (CMS classification codes):', file=sys.stderr)
        for seg, rows in sorted(significant_specialties.items()):
            csv_path = seg_dir / f'specialty_{seg}.csv'
            df_out = _to_csv_friendly(rows)
            df_out.to_csv(csv_path, index=False)
            print(f'  {seg:<25} {len(rows):>5,} → {csv_path.name}', file=sys.stderr)
    else:
        print('\nSpecialty segments: skipped (CMS classification codes mostly empty in this file)', file=sys.stderr)

    # Russian candidates
    if russian_candidates:
        csv_path = seg_dir / 'russian_candidates_nj.csv'
        df_out = _to_csv_friendly(russian_candidates)
        df_out.to_csv(csv_path, index=False)
        print(f'\nrussian_candidates_nj: {len(russian_candidates):,} → {csv_path.name}', file=sys.stderr)


def _to_csv_friendly(rows: list[dict]) -> 'pd.DataFrame':
    """Flatten list-of-list fields for CSV output."""
    df_out = pd.DataFrame(rows)
    if 'classification_codes' in df_out.columns:
        df_out['classification_codes'] = df_out['classification_codes'].apply(lambda x: '|'.join(x) if isinstance(x, list) else '')
    if 'segments' in df_out.columns:
        df_out['segments'] = df_out['segments'].apply(lambda x: '|'.join(x) if isinstance(x, list) else '')
    return df_out


def print_summary(companies: list):
    """Human-readable summary table."""
    df = pd.DataFrame(companies)
    print('\n=== ICP SUMMARY ===', file=sys.stderr)
    print(f'Total ICP labs: {len(df):,}', file=sys.stderr)
    print(f'\nBy state (top 10):', file=sys.stderr)
    print(df['state'].value_counts().head(10).to_string(), file=sys.stderr)
    print(f'\nBy lab type:', file=sys.stderr)
    print(df['lab_type'].value_counts().to_string(), file=sys.stderr)
    print(f'\nBy certificate type:', file=sys.stderr)
    print(df['certificate_type'].value_counts().to_string(), file=sys.stderr)
    seg_counts: dict[str, int] = {}
    for segs in df['segments']:
        for s in segs:
            seg_counts[s] = seg_counts.get(s, 0) + 1
    print(f'\nBy segment:', file=sys.stderr)
    for seg, count in sorted(seg_counts.items(), key=lambda x: -x[1]):
        print(f'  {seg:<25} {count:>6,}', file=sys.stderr)
    print(f'\nRussian-speaking candidates (NJ/NY/PA): {df["russian_candidate"].sum():,}', file=sys.stderr)
    print('===================\n', file=sys.stderr)


def main():
    args = parse_args()

    if not args.input.exists():
        sys.exit(f'ERROR: input file not found: {args.input}')

    # detect quarter from filename if possible (POS_File_CLIA_Q1_2026.csv → Q1_2026)
    stem = args.input.stem
    quarter = stem.split('_')[-2] + '_' + stem.split('_')[-1] if '_' in stem else 'unknown'

    df = load_pos_file(args.input)
    icp = apply_icp_filter(df, since=args.since, include_hospital=args.include_hospital_labs)

    print('Converting to gtm-mcp company format ...', file=sys.stderr)
    companies = [row_to_company(row) for _, row in icp.iterrows()]

    if args.segment:
        before = len(companies)
        companies = [c for c in companies if args.segment in c['segments']]
        print(f'  filtered to segment {args.segment}: {before:,} → {len(companies):,}', file=sys.stderr)

    if args.max_results:
        companies = companies[:args.max_results]
        print(f'  capped at --max-results {args.max_results}', file=sys.stderr)

    print_summary(companies)
    write_outputs(companies, args, quarter)
    print('Done.', file=sys.stderr)


if __name__ == '__main__':
    main()
