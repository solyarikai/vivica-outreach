# Lab Universe — US Labs 12mo Scored (2026-05-12)

> Reference documentation for the Google Sheet **"Vivica — US Lab Universe (12mo, scored)"**.
> Built by Petr. Covers May 2025 → May 2026 (12-month window).
> 8,256 unique US labs from 3 federal datasets, deduped by NPI + CLIA # + fuzzy name.

---

## Dataset Sources

Three federal datasets merged and deduplicated:

| Code | Source | What it means |
|---|---|---|
| **C** | CMS POS — CLIA register | Active lab license (CLIA-certified) |
| **N** | NPPES — NPI registry | Federal NPI, lab taxonomy 291U / 2919 |
| **M** | Medicare PPEF | Already billing Medicare for lab services |

### Combined signals

| Sources value | Interpretation |
|---|---|
| `C` | CLIA only — licensed lab, no NPI match |
| `N` | NPI only — pre-license or join miss |
| `M` | Medicare only — established pre-window operator |
| `CN` | CLIA + NPI — bullseye: licensed + billing-ready |
| `CNM` | All three — fully commercially set up. Freshness cohort determines priority (see Tiers) |

---

## Freshness Cohorts

The 12-month window is split into two cohorts based on when CLIA or NPI was issued:

| Cohort | When issued | Signal |
|---|---|---|
| **A** (`A_fresh_le_6mo`) | ≤ 6 months ago | HOTTEST — pre-LIMS-buy window |
| **B** | 6–12 months ago | Still likely pre-LIMS |

### Why Medicare enrollment ≠ "already chose LIMS"

Medicare enrollment (Form 855B) is a 60–90 day paperwork process that happens **after** CLIA approval. It signals billing readiness, not LIMS purchase.

- A lab with CLIA ≤ 6mo + NPI + Medicare = aggressive operator going fast, **still spinning up**
- They are still buying tools, including LIMS
- Example: **QUASAR LABORATORY (TX)** — CLIA 110d ago, NPI 126d ago, Medicare-enrolled → Tier S+

CNM labs are differentiated purely by cohort:
- CNM in Cohort A (≤ 6mo) → typically S+/S/A
- CNM with unknown cohort (no fresh CLIA/NPI) → C/D/E

---

## Tier Definitions

| Tier | Count | Plain English | Filter recipe |
|---|---|---|---|
| **S+** | 21 | Brand-new lab, CLIA + NPI both ≤ 6mo, agent-verified standalone, fresh + commercial intent | `Sources IN (CN, CNM) AND Tier='S+' AND Cohort='A_fresh_le_6mo'` |
| **S** | 183 | CLIA-licensed in last 12mo with Compliance or Accreditation cert | `Tier='S'` |
| **A** | 1,124 | CLIA-licensed in last 12mo with Registration/PPM cert, single-source verification | `Tier='A'` |
| **B** | 541 | Federal NPI with lab taxonomy but no matching CLIA — pre-license or join miss | `Tier='B'` |
| **C** | 5,967 | Medicare-only — established pre-window operator. Probably has LIMS already | `Tier='C'` |
| **D** | 48 | Net-positive freshness BUT yellow flag: subsidiary or virtual mailbox | `Tier='D'` |
| **E** | 372 | Hard blocklist: top-20 brand (LabCorp/Quest/etc) OR agent-flagged established operator | `Tier='E'` |

**Actionable universe:** S+/S/A/B = **1,869 labs**. HOT (S+/S) = **204 labs**.

---

## Google Sheet — Tab Guide

| Tab | Contents | When to use |
|---|---|---|
| **All Targets** | Every lab (8,256), sorted Tier → Score desc | Custom analysis, ad-hoc filters |
| **Cohort A (≤6mo)** | 990 labs — CLIA/NPI issued in last 180 days | Freshest candidates regardless of source signal |
| **Cohort B (6-12mo)** | 1,240 labs — issued 180–365 days ago | Second-wave outreach |
| **HOT (S+/S)** | 204 highest-priority labs | **Open this first** — this-week outreach candidates |
| **MEDIUM (A/B)** | 1,675 strong candidates, single-source verified | Second wave, quick-verify each |
| **LOW (C)** | 5,967 mostly Medicare-only established labs | Reference only |
| **DEPRIORITIZE (D/E)** | 420 hard-skip labs | Blocklist |
| **_summary** | Counts by tier × cohort × source | Universe sanity check |
| **_methodology** | Every scoring code with delta and description | Why a lab got the score it did |
| **_filter_recipes** | Copy-paste filter recipes for common questions | Slicing the data |

---

## Website Verification Methodology

For each priority lab, the agent:

1. WebSearch `<facility name> <city> <state>` + `<facility name> laboratory`
2. Filter out 60+ directory domains (npidb, opennpi, yelp, healthgrades, dnb, zoominfo, …)
3. For top 1–3 non-directory candidates, fetch the page
4. **STRICT verification**: distinctive name token in title AND (phone verbatim OR street-address words verbatim OR Authorized Official name) in body
5. Pass → fill `Website (verified)` column. Fail → empty cell

> **Important:** An empty `Website (verified)` cell does NOT mean "no website exists." It means the agent couldn't 100%-prove this website belongs to this specific lab. Always cross-check before assuming.

---

## Flags & Patterns Observed During Verification

Notable fraud/quality signals caught by agents during the batch verification run (2026-05-12):

- **CO LLC shell network**: 4 CO LLCs (names ending -vion/-ureon/-irium/-vora) share directors — clear shell network
- **NY charity fraud**: NY children's charities registered as Houston labs
- **Phone farm**: 4 unrelated entities sharing 1 phone (Calabasas CA)
- **Mass-agent farms**: WY batch showed pattern of factory-registered labs

These labs are flagged in Tier D or E.

---

## Column Reference

| Column | Description |
|---|---|
| Facility Name | Official CLIA/NPPES name |
| NPI | National Provider Identifier |
| CLIA # | CLIA certificate number |
| Sources | Which datasets matched (C/N/M/CN/CNM) |
| Cohort | A (≤6mo) or B (6–12mo) |
| Tier | S+/S/A/B/C/D/E |
| Score | Numeric score driving sort order |
| State | US state |
| City | City |
| Phone | CLIA/NPPES phone |
| Authorized Official | Contact person from CLIA POS |
| Certificate Type | CLIA cert type (Registration, Compliance, Accreditation, PPM) |
| CLIA Issue Date | When CLIA was issued |
| NPI Issue Date | When NPI was issued |
| Medicare Enrolled | Whether lab appears in PPEF |
| Website (verified) | Verified lab website — empty = unverified, not "no website" |

---

## Links

- Sheet built by: Petr (2026-05-12)
- Raw CLIA source: [[source-lists/clia-q1-2026]]
- Scoring methodology detail: `_methodology` tab in the sheet
- Decisions on segment prioritization: [[decisions-log]]
