"""
classify_by_clia_code.py — map CMS POS file fields to Vivica segments,
infer lab type, and flag russian-speaking candidates.

Two segmentation axes:

1. **Specialty** (toxicology / pathology / molecular / etc.) — comes from
   CLIA_LAB_CLASSIFICATION_CD_1..10. WARNING: in practice, these fields are
   mostly populated as '00' (no specialty declared) for newly-certified labs
   in the CMS POS file. Only ~1% of records have meaningful classification
   codes. Treat specialty segments as "bonus signal" — most labs will fall
   into 'unspecified' until enriched downstream.

2. **Facility type** (POL / PSC / Reference / etc.) — comes from
   GNRL_FAC_TYPE_CD per the CMS POS layout (Sep 2022 spec).

Source: https://data.cms.gov/sites/default/files/2022-10/eb7b11f8-f79b-4229-a365-a69cd27f69a3/Layout%20Sep%2022%20CLIA.pdf
"""

import re

# CLIA classification code → Vivica segment(s)
# A single code can map to multiple segments if the specialty crosses categories.
CODE_TO_SEGMENTS: dict[str, list[str]] = {
    # Anatomic pathology cluster
    '100': ['anatomic_pathology'],            # histopathology
    '110': ['anatomic_pathology'],            # oral pathology
    '120': ['anatomic_pathology', 'cytology'],  # cytology
    '130': ['anatomic_pathology'],            # cytogenetics

    # Molecular & genetics
    '250': ['molecular_diagnostics'],         # molecular biology / molecular pathology
    '260': ['molecular_diagnostics'],         # molecular oncology

    # Clinical chemistry
    '310': ['clinical_chemistry'],            # routine chemistry
    '320': ['clinical_chemistry'],            # automated chemistry / endocrinology
    '330': ['clinical_chemistry', 'urinalysis'],  # urinalysis
    '340': ['clinical_chemistry'],            # general chemistry

    # Hematology
    '400': ['hematology'],                    # hematology

    # Microbiology cluster
    '500': ['microbiology'],                  # bacteriology
    '510': ['microbiology'],                  # mycobacteriology
    '520': ['microbiology'],                  # mycology
    '530': ['microbiology'],                  # parasitology
    '540': ['microbiology', 'virology'],      # virology

    # Immunology / serology
    '600': ['immunology'],                    # diagnostic immunology / general immunology
    '610': ['immunology'],                    # syphilis serology

    # Toxicology — Vivica's premium segment per Andrew's note
    '800': ['toxicology'],                    # toxicology (general)
    '810': ['toxicology', 'forensic'],        # forensic toxicology

    # Radiobioassay (rare but kept for completeness)
    '900': ['radiobioassay'],
}


def classify_segments(codes: list[str]) -> list[str]:
    """Map a list of CLIA classification codes to a deduplicated list of Vivica segments."""
    out: list[str] = []
    seen: set[str] = set()
    for code in codes:
        for seg in CODE_TO_SEGMENTS.get(code, []):
            if seg not in seen:
                seen.add(seg)
                out.append(seg)
    if not out:
        out = ['unspecified']
    return out


# CMS POS file GNRL_FAC_TYPE_CD values (Sept 2022 spec).
# These are the AUTHORITATIVE facility-type segments — much more reliable
# than the CLIA_LAB_CLASSIFICATION codes which are mostly '00'.
GNRL_FAC_TYPE_NAMES: dict[str, str] = {
    '01': 'ambulance',
    '02': 'ambulatory_surgery_center',
    '03': 'ancillary_test_site',
    '04': 'assisted_living',
    '05': 'blood_bank',
    '06': 'community_clinic',
    '07': 'comprehensive_outpatient_rehab',
    '08': 'esrd_dialysis',
    '09': 'fqhc',  # Federally Qualified Health Center
    '10': 'health_fair',
    '11': 'hmo',
    '12': 'home_health',
    '13': 'hospice',
    '14': 'hospital',
    '15': 'independent',  # Independent lab — REFERENCE in our taxonomy
    '16': 'industrial',
    '17': 'insurance',
    '18': 'icf_iid',
    '19': 'mobile_lab',
    '20': 'pharmacy',
    '21': 'physician_office',  # POL in our taxonomy — biggest segment
    '22': 'other_practitioner',
    '23': 'prison',
    '24': 'public_health_lab',
    '25': 'rural_health_clinic',
    '26': 'school_student_health',
    '27': 'snf_nursing',
    '28': 'tissue_bank',
    '29': 'other',
}


# Vivica's targeting taxonomy maps CMS facility types to our 4 buckets:
#   POL = Physician Office Lab
#   PSC = Patient Service Center / standalone diagnostic
#   REFERENCE = independent reference lab, multi-site, public health
#   UNSUITABLE = hospital, prison, pharmacy, insurance — skip these
#   OTHER = small footprint, low priority
VIVICA_BUCKET: dict[str, str] = {
    '21': 'POL',           # Physician Office — primary target
    '22': 'POL',           # Other Practitioner — treat as POL-like
    '15': 'REFERENCE',     # Independent — main Reference Lab category
    '03': 'PSC',           # Ancillary Test Site
    '24': 'REFERENCE',     # Public Health Lab
    '06': 'PSC',           # Community Clinic — treat as PSC-like
    '09': 'PSC',           # FQHC — treat as PSC-like
    '25': 'PSC',           # Rural Health Clinic
    '14': 'UNSUITABLE',    # Hospital — Epic/Cerner lock-in, skip
    '23': 'UNSUITABLE',    # Prison
    '20': 'UNSUITABLE',    # Pharmacy
    '17': 'UNSUITABLE',    # Insurance
    '08': 'UNSUITABLE',    # ESRD dialysis
    '12': 'OTHER',         # Home health
    '13': 'OTHER',         # Hospice
    '27': 'OTHER',         # SNF / nursing
    '04': 'OTHER',         # Assisted living
    '18': 'OTHER',         # ICF/IID
    '26': 'OTHER',         # School/student health
    '28': 'OTHER',         # Tissue bank
    '01': 'OTHER',         # Ambulance
    '02': 'OTHER',         # Ambulatory surgery center
    '05': 'OTHER',         # Blood bank
    '07': 'OTHER',         # Comprehensive outpatient rehab
    '10': 'OTHER',         # Health fair
    '11': 'OTHER',         # HMO
    '16': 'OTHER',         # Industrial
    '19': 'OTHER',         # Mobile lab
    '29': 'OTHER',         # Other
}


def classify_facility_type(gnrl_fac_type_cd: str) -> tuple[str, str]:
    """
    Map a CMS GNRL_FAC_TYPE_CD to (vivica_bucket, facility_name).

    Returns:
        ('POL', 'physician_office')
        ('REFERENCE', 'independent')
        ('PSC', 'community_clinic')
        ('UNSUITABLE', 'hospital')
        ('OTHER', 'home_health')
    """
    code = str(gnrl_fac_type_cd or '').strip().zfill(2)
    facility_name = GNRL_FAC_TYPE_NAMES.get(code, 'unknown')
    bucket = VIVICA_BUCKET.get(code, 'OTHER')
    return bucket, facility_name


# Patterns that mark a Physician Office Lab — name contains a physician identifier.
POL_NAME_PATTERNS = re.compile(
    r'\b(?:M\.?D\.?|D\.?O\.?|DR\.?|P\.?C\.?|PLLC|MEDICAL\s+ASSOCIATES|'
    r'FAMILY\s+MEDICINE|INTERNAL\s+MEDICINE|PEDIATRIC|UROLOGY|CARDIOLOGY)\b',
    re.IGNORECASE,
)

# Patterns that mark a Patient Service Center / standalone diagnostic.
PSC_NAME_PATTERNS = re.compile(
    r'\b(?:LAB(?:ORATORY|ORATORIES)?|DIAGNOSTIC|PATIENT\s+SERVICE|TESTING\s+CENTER|CLINIC)\b',
    re.IGNORECASE,
)


def infer_lab_type(
    name: str,
    site_count: int,
    test_volume: int,
    gnrl_fac_type_cd: str | None = None,
) -> str:
    """
    Detect lab type using CMS GNRL_FAC_TYPE_CD when available, then naming
    heuristics, then volume/site fallback.

    Returns one of: POL, PSC, REFERENCE, UNSUITABLE, OTHER, UNKNOWN.

    Priority:
    1. GNRL_FAC_TYPE_CD if present and not '29' (other) — authoritative
    2. Heuristics on lab name + size for refining 'OTHER' category
    """
    if gnrl_fac_type_cd:
        bucket, _ = classify_facility_type(gnrl_fac_type_cd)
        if bucket != 'OTHER':
            return bucket

    # Fallback heuristics for ambiguous cases
    if test_volume >= 50_000 or site_count > 1:
        return 'REFERENCE'

    if site_count == 1:
        if POL_NAME_PATTERNS.search(name):
            return 'POL'
        if PSC_NAME_PATTERNS.search(name):
            return 'PSC'

    return 'OTHER'


# Patterns indicating possible russian-speaking ownership.
# Used as a CANDIDATE filter only — final attribution requires Andrew's review.
RU_CANDIDATE_PATTERNS = re.compile(
    # Common naming patterns of russian/eastern-european-owned medical practices in NY/NJ/PA
    r'\b(?:medical|diagnostic|laboratories|associates|wellness|family\s+health)\b',
    re.IGNORECASE,
)

# States with significant russian-speaking medical-practice density (per kick-off call)
RU_TARGET_STATES = {'NJ', 'NY', 'PA'}


def mark_russian_candidate(name: str, state: str) -> bool:
    """
    Returns True if the lab is a candidate for russian-speaking-owner outreach.

    This is INTENTIONALLY noisy — it marks too many candidates rather than too few.
    The russian_segment.md playbook describes the manual review process Andrew follows.
    """
    if state not in RU_TARGET_STATES:
        return False
    if not RU_CANDIDATE_PATTERNS.search(name):
        return False
    return True
