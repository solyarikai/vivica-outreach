# Playbook — Three-Phase Migration Framework

Vivica's universal answer to the biggest objection in clinical-LIMS sales: **"switching is too risky."**

This playbook is the single most reused asset in outreach. Every persona references it. Every competitor's migration story uses it. When in doubt, fall back to this framework.

> **Status**: framework articulated in 2026-Q2 kick-off call. Concrete timelines and case-specific details to be confirmed by Chris.

## The framework in one paragraph

Most LIMS migrations fail because vendors force a **rip-and-replace**: turn off the old system, turn on the new one, hope for the best. Vivica doesn't. We run **three sequential phases** — Mirror, Proxy, Decommission — that let a lab keep operating throughout, validate at each step, and roll back any time before the cutover. The lab's operations never depend on a single irreversible flip.

## Phase 1 — Mirror

**Goal**: Vivica is configured to look exactly like the customer's current LIMS, but produces no live results yet.

**What happens**:
- Customer exports their current configuration: test catalog, client list, reference ranges, instrument profiles, report templates, user roles, validation docs
- Vivica integration team replicates this configuration in a customer tenant
- Historical results are imported (typically 5-15 years of result history, depending on lab)
- Validation documents are imported and linked to methods (re-confirming, not re-validating)
- The customer team logs in and walks through their workflows in Vivica — same screens, same steps, same results

**Customer effort**: ~8 hours of bench-team time total. Mostly answering "is this the right reference range?" and "should this report look like this?"

**Vivica effort**: 80-120 hours of integration team work, depending on complexity.

**Duration**: 2-4 weeks for typical POL/PSC; 4-8 weeks for Reference Labs.

**Exit criteria**:
- Test catalog matches 100%
- Reference ranges match 100%
- Sample reports generated from imported historical data match the originals byte-for-byte (or with documented approved differences)
- Customer Lab Director signs off

**Rollback**: trivial. Customer hasn't switched anything. Vivica tenant just gets archived.

## Phase 2 — Proxy

**Goal**: Vivica produces parallel results to the legacy LIMS for live work, but the legacy system remains the system of record. The two systems are compared daily.

**What happens**:
- Instrument data flows to **both** the legacy LIMS and Vivica simultaneously (HL7/ASTM split)
- Customer team enters orders in Vivica
- Results are released from the legacy LIMS (officially) and from Vivica (in shadow)
- A daily reconciliation report shows where the two systems differ
- Differences are investigated, root-caused, and resolved
- Customer team gets daily hands-on Vivica use without operational risk

**Customer effort**: minimal incremental — they're working in Vivica anyway, just reading results from the legacy LIMS for now. Daily 30-min reconciliation review by Lab Director.

**Vivica effort**: 24/7 monitoring, daily reconciliation analysis, on-call integration team for any divergence.

**Duration**: 30-60 days. Standard pattern: 30 days for low-complexity (single-specialty POL), 60 days for high-complexity (multi-specialty Reference Lab).

**Exit criteria**:
- Reconciliation report shows zero unexplained differences for 14 consecutive days
- Customer team reports daily-use confidence
- Lab Director and Medical Director both sign off
- All instrument integrations producing matched results
- All client report formats generating correctly

**Rollback**: still trivial. Customer is using legacy LIMS as system of record; Vivica is shadow. Cutting Vivica off has zero operational impact.

## Phase 3 — Decommission

**Goal**: Cutover by service line, not all at once. Each service line moves independently from "legacy primary, Vivica shadow" to "Vivica primary, legacy archive."

**What happens**:
- Service-line-by-service-line cutover. Typical sequence:
  1. **Routine clinical chemistry** first (highest volume, lowest complexity, easiest to validate)
  2. **Hematology** (similar profile)
  3. **Microbiology** (more complex result types)
  4. **Anatomic pathology** (narrative, attached images, complex result types)
  5. **Molecular / specialty** last (highest complexity, lowest volume)
- For each service line: 7-day final validation period, then cutover
- Legacy LIMS receives zero new orders for that service line; remains read-only for archive access
- Customer team handles cutover-day operations (Vivica integration team on standby)

**Customer effort**: 1-2 hours per cutover day per service line. Lab Director coordinates.

**Vivica effort**: on-call presence each cutover day; integration team available for fast resolution of any incident.

**Duration**: 4-12 weeks total, depending on number of service lines. POL with 2 service lines: 2-3 weeks. Multi-specialty Reference Lab: 8-12 weeks.

**Exit criteria**: all service lines on Vivica; legacy LIMS in read-only archive mode; final inspection-readiness audit passed.

**Rollback per service line**: possible but rare. If a service line shows issues post-cutover, revert that single service to legacy while keeping the rest on Vivica. Vivica integration team owns the rollback execution.

## Total timeline

| Lab type | Mirror | Proxy | Decommission | **Total** |
|---|---|---|---|---|
| POL (single specialty) | 2 weeks | 30 days | 2 weeks | **~8 weeks** |
| PSC (multi-test) | 3 weeks | 30 days | 3 weeks | **~10 weeks** |
| Reference Lab (multi-specialty) | 6 weeks | 60 days | 8 weeks | **~16 weeks** |

Compare to typical LabWare or Clinisys migrations of 12-24 months.

## How to use this in cold outreach

This framework is the **#1 most-reused asset** across email sequences. Every "switching is too risky" objection gets answered with it.

### In subject lines

- "incremental migration off [vendor]"
- "switching off [vendor] without the 12-month nightmare"
- "how Acure migrated in [X] weeks, not [Y] months"

### In email body

Use this 3-sentence pattern when introducing the framework:

> "Most labs switching from [vendor] are afraid of the 12-month migration horror story. We don't do that. We mirror your current LIMS in Vivica first, run shadow operations for 30-60 days, then cutover service-line by service-line — your legacy keeps running until you're confident."

### In follow-ups

When a prospect engages but stalls, use the timeline table verbatim. Specificity beats reassurance.

### In objection responses

The framework is the answer to:
- "We're fine with our current system" → "And it'll keep running through our 3-phase migration"
- "Our team is overworked" → "Mirror phase needs ~8 hours from your bench team total"
- "Migration will mess up our QA history" → "Mirror phase imports your full QA + competency + PT history"
- "Switching is a 12-month nightmare" → entire framework with the timeline table

## How skills use this framework

- **`email-sequence`** in gtm-mcp pulls this framework when the segment is competitor-conquest or "switching from legacy"
- **All 9 battle cards** in `../battle-cards/` reference this playbook
- All 3 personas in `../icp/` reference this playbook in their objection-response tables

## What NOT to claim

- ❌ Don't claim total migration time shorter than the table above. Promising 4 weeks to a Reference Lab is overcommitting.
- ❌ Don't promise zero customer effort. Be specific: ~8 hours from bench team.
- ❌ Don't promise rollback with zero cost in Phase 3. Rollback per-service is possible, not free — there's coordination overhead.
- ❌ Don't claim Acure went live in any specific number of weeks until Chris confirms.

## Cross-references

- Personas (all 3 reference this): `../icp/persona-ceo-owner.md`, `../icp/persona-lab-director.md`, `../icp/persona-medical-director.md`
- Battle cards (all 9 reference this): `../battle-cards/*.md`
- Acure case study (the proof point): `../case-studies/acure-reference-lab-nj.md`
- Vivica capability summary: `../company/vivica-intel.md`
- Glossary entry: `../../glossary.md` → "Three-phase migration framework"
