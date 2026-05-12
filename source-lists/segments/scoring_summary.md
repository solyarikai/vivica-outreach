# Vivica Score Distribution — Reference Labs Contacts

**Source**: `final_contacts_tiered.csv` (344) × `bucket_REFERENCE.csv` (1849)
**Date**: 2026-05-12
**Script**: `score_contacts.py`

## Scoring model (max ~120)

Calibrated to actual signal distribution in the data. CLIA age and cert type
were dropped — on the Q1 2026 cohort all contacts are ≤6 months old and 99%
are Compliance certificates, so these signals don't discriminate.

| Signal | Source | Weights |
|--------|--------|---------|
| Facility type | `cms_facility_type_name` | independent +30 / public_health +15 / non-lab -30 |
| Test volume | `test_volume` | 1k-50k +25 / 50k-500k +15 / 1-999 +10 / 500k+ 0 / 0 -10 |
| Site count | `site_count` | 0-1 +10 / 2-5 0 / 6+ -10 |
| Persona | `persona` | CEO/Owner +20 / Lab Dir +15 / Med Dir +10 |
| LinkedIn | `contact_linkedin` non-empty | +5 |
| Petr's tier | `tier` | S+ +30 / S +20 / A +10 / B +5 / D/E -50 |

## Bucket distribution

| Bucket | Threshold | Count | % | Action |
|--------|-----------|-------|---|--------|
| HOT | ≥75 | 188 | 54.7% | First wave in SmartLead |
| WARM | 50-74 | 97 | 28.2% | Main pool |
| COOL | 25-49 | 26 | 7.6% | Top-up wave |
| COLD | <25 | 33 | 9.6% | Skip or last resort |

## Top 20 scored contacts

| # | Score | Bucket | Lab | Persona | Facility | Vol | Sites | Tier |
|---|-------|--------|-----|---------|----------|-----|-------|------|
| 1 | 120 | HOT | CASCADE PATHOLOGY SERVICES - ALLENMORE | ceo_owner | independent | 12050 | 0 | S+ |
| 2 | 95 | HOT | PANOME BIO, INC | ceo_owner | independent | 100 | 0 | S |
| 3 | 95 | HOT | NIGHTINGALE HEALTH UNITED STATES, INC, | ceo_owner | independent | 1 | 0 | S |
| 4 | 95 | HOT | REGENERON CLINICAL GENOMICS LABORATORY | ceo_owner | independent | 1 | 0 | S |
| 5 | 95 | HOT | MOUNT SINAI DERMATOPATHOLOGY LABORATOR | ceo_owner | independent | 1 | 0 | S |
| 6 | 95 | HOT | NYU LANGONE HEALTH - PENN DISTRICT LAB | ceo_owner | independent | 1 | 0 | S |
| 7 | 90 | HOT | MOUNT SINAI DERMATOPATHOLOGY LABORATOR | lab_director | independent | 1 | 0 | S |
| 8 | 90 | HOT | LABORATORY CORPORATION OF AMERICA HOLD | ceo_owner | independent | 9926 | 0 | — |
| 9 | 90 | HOT | BIRMINGHAM GASTROENTEROLOGY ASSOC PC | ceo_owner | independent | 12200 | 0 | — |
| 10 | 90 | HOT | QUEST DIAGNOSTICS | ceo_owner | independent | 47530 | 0 | — |
| 11 | 90 | HOT | CELLNETIX PATHOLOGY ALASKA REGIONAL HO | ceo_owner | independent | 8000 | 0 | — |
| 12 | 90 | HOT | SAGIS | ceo_owner | independent | 4000 | 0 | — |
| 13 | 90 | HOT | CND LIFE SCIENCES R&D LAB | ceo_owner | independent | 1500 | 0 | — |
| 14 | 90 | HOT | AEL - CONWAY | ceo_owner | independent | 17315 | 0 | — |
| 15 | 90 | HOT | HRC FERTLITY MANAGEMENT, LLC | ceo_owner | independent | 1700 | 0 | — |
| 16 | 90 | HOT | DAVID J BARNETTE JR MD | ceo_owner | independent | 12000 | 0 | — |
| 17 | 90 | HOT | UNIVERSITY OF CALIFORNIA IRVINE, | ceo_owner | independent | 2185 | 0 | — |
| 18 | 90 | HOT | OMNIPATHOLOGY SOLUTIONS | ceo_owner | independent | 16305 | 0 | — |
| 19 | 90 | HOT | ORANGE COUNTY LABS INC | ceo_owner | independent | 14000 | 0 | — |
| 20 | 90 | HOT | NAVJYOT GUJRAL MD | ceo_owner | independent | 3000 | 0 | — |

## Bottom 10 (likely skip)

| # | Score | Bucket | Lab | Persona | Facility | Vol | Sites | Tier |
|---|-------|--------|-----|---------|----------|-----|-------|------|
| 1 | -5 | COLD | ONSPOT -FL, LLC | medical_director | mobile_lab | 600 | 2 | — |
| 2 | -5 | COLD | BILLINGS CLINIC MED FLIGHT BILLINGS | medical_director | ambulance | 520 | 2 | — |
| 3 | -5 | COLD | OPTIMUMEDICINE | medical_director | ambulance | 58 | 2 | — |
| 4 | -5 | COLD | DHART - MANCHESTER | medical_director | ambulance | 150 | 2 | — |
| 5 | -5 | COLD | BERNALILLO HEALTH CARE CORP | ceo_owner | ambulance | 60 | 67 | — |
| 6 | -5 | COLD | AEROMD | medical_director | ambulance | 30 | 2 | — |
| 7 | -15 | COLD | OCHSNER LSU HEALTH SHREVEPORT REGIONAL | ceo_owner | ambulatory_surgery_center | 0 | 3 | — |
| 8 | -15 | COLD | RIVERSTONE HEALTH MOBILE UNIT | ceo_owner | mobile_lab | 0 | 2 | — |
| 9 | -20 | COLD | OCHSNER LSU HEALTH SHREVEPORT REGIONAL | lab_director | ambulatory_surgery_center | 0 | 3 | — |
| 10 | -25 | COLD | WOMEN'S & MEN'S HEALTH SERVICES OF THE | medical_director | mobile_lab | 0 | 2 | — |

## Average contribution per signal

| Signal | Avg points | Max possible |
|--------|------------|--------------|
| facility_type | +19.4 | 30 |
| test_volume | +15.8 | 25 |
| site_count | +8.3 | 10 |
| persona | +17.2 | 20 |
| halinkedin | +5.0 | 5 |
| petr_tier | +0.6 | 30 |

## Cross-check: Vivica bucket × Petr's tier

| | S+ | S | A | B | C | D | E | — | Total |
|---|----|---|----|----|----|----|----|----|-------|
| HOT | 1 | 9 | 0 | 1 | 0 | 0 | 0 | 177 | 188 |
| WARM | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 97 | 97 |
| COOL | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 26 | 26 |
| COLD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 33 | 33 |

## Facility type breakdown across pool

| Facility type | Count | Avg score |
|---------------|-------|-----------|
| independent | 236 | 79.9 |
| other | 39 | 44.0 |
| public_health_lab | 37 | 57.3 |
| ambulance | 13 | 3.1 |
| mobile_lab | 7 | -0.7 |
| hmo | 4 | 16.2 |
| ambulatory_surgery_center | 4 | -2.5 |
| blood_bank | 2 | 17.5 |
| tissue_bank | 1 | 10.0 |
| hospice | 1 | 5.0 |
