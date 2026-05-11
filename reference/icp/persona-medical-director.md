# Persona — Medical Director

The clinical authority of the lab. Sets policy on test methodology, reviews abnormal results, signs off on validations, and is the legal "responsible person" for compliance. Almost always an MD/DO with pathology or clinical pathology training. Less involved in software selection than Lab Director, but holds veto power on anything affecting clinical accuracy.

> **Source**: Vivica ICP Google Sheet, captured during 2026-Q2 kick-off call.

## Profile

| Attribute | Value |
|---|---|
| Title | Medical Director / Lab Director (clinical role) / CLIA Director / Pathologist |
| Background | MD/DO; usually board-certified in Clinical Pathology or Anatomic Pathology |
| Reports to | CEO/Owner; legally responsible to CMS/state |
| Lives in | EHR, microscopy slides, pathology committee meetings, occasional ASCP/CAP events |
| Tenure | Often 10+ years; sometimes covers multiple labs as a consulting director |

## Top goals

What this persona truly cares about:

1. **Patient safety** — no wrong result reaches a clinician, ever
2. **Defensible methodology** — every method validated, every validation documented, every change tracked
3. **Regulatory compliance** — CLIA, CAP, FDA-LDT (when applicable), state-specific rules
4. **Clinical interpretability** — the LIS must present results in a way that makes clinical sense, not just chemically correct values
5. **Their professional reputation** — their name is on every report; one major error and their malpractice exposure spikes

## KPIs they personally watch

- **Critical-value reporting compliance** — every critical value documented as communicated within minutes
- **Method validation completeness** — every test has accuracy, precision, linearity, reportable range, reference range docs
- **Proficiency testing performance** — CAP PT, AAB PT, state-required surveys
- **Amendment / correction rate** — how often results are corrected after release
- **Inspection findings** — especially anything in the "Phase II" CAP deficiency category
- **CME / continuing education hours** — for their own license

## Pain points

What worries them about most LIMS:

- **Audit trails are gappy** — when an inspector asks "who changed this reference range and when," the answer is "we'd have to ask the vendor"
- **E-signature workflows are clunky** — they sign off on dozens of validations a month, every signature shouldn't take three clicks
- **Result modifications are too easy** — a tech can edit a result without an automatic flag, that's a malpractice risk
- **Reflex testing logic is hardcoded** — they can't easily change "if X positive, also run Y" rules, every change is a vendor ticket
- **LIS can't represent complex test panels** — molecular oncology results need narrative interpretation, most LIMS treat results as numbers
- **No version control on validation docs** — they need to prove which version of a SOP was active on a given date

## Buying triggers

When they start pushing for a different system:

1. **CAP citation specifically about audit trail or e-signature**
2. **New test method introduction** that current LIMS can't represent (e.g., NGS panels, mass spec methods)
3. **Adding a new specialty** (cytology, molecular, toxicology) — different reporting needs
4. **Malpractice case** at this or a peer lab where the LIMS contributed to the error
5. **Regulatory change** — new CLIA rule, new CAP checklist requirement
6. **Hiring a junior pathologist** who pushes for modern tools

## Common objections

The exact words we hear (from ICP sheet):

- "**How do I know this meets compliance standards?**"
- "**These systems oversimplify clinical data.**"
- "**Our current methodology is validated — switching means re-validating everything.**"
- "**I won't sign off on a system I haven't personally vetted.**"
- "**Cloud means our data sits with someone else.**"
- "**What about HIPAA / business associate agreement?**"
- "**Has CAP looked at your platform specifically?**"

## Objection responses

| Objection | Response |
|---|---|
| "How do I know this meets compliance standards?" | "Vivica is built around CLIA / CAP / HIPAA controls. Every action — including yours — is logged with user, timestamp, prior value, new value, reason. Want a sample audit-trail export from a CAP-accredited customer?" |
| "Systems oversimplify clinical data." | "We support narrative reporting, structured fields, attached images, and version-controlled interpretation templates. Our anatomic-pathology customers (like Acure) use it for full surgical pathology reports, not just CBCs." |
| "Re-validating everything." | "Mirror phase imports your existing validation docs and links them to the methods. You're re-confirming, not re-validating from scratch. We've done this for ~50 method transitions; happy to share the spec." |
| "I won't sign off on a system I haven't vetted." | "That's exactly the right posture — and we expect it. Mirror phase gives you 30+ days of side-by-side use before any patient result is touched. Vet it on your real workflow, with your data." |
| "Cloud means data sits with someone else." | "Vivica is HIPAA-compliant, SOC 2 Type II, BAAs signed with every customer. Data lives in US-region AWS, encrypted at rest and in transit. Our customers control retention, access, and audit." |
| "Has CAP looked at your platform?" | "CAP doesn't certify LIMS vendors — they certify your lab. What CAP cares about is whether your LIMS gives you the controls to pass their checklist. We can walk you through Phase II checklist mapping. Acure passed inspection on Vivica in 2025 with zero deficiencies tied to the system." |

## How Vivica solves their problems

- **Immutable audit trail**: every event logged, every change reasoned, every export inspector-ready
- **E-signature with reason codes**: integrated into validation, amendment, and result-release workflows
- **Configurable result modification rules**: who can edit what, with mandatory reason codes and supervisor approval where needed
- **Reflex logic in user-editable rules engine**: Medical Director or designee can modify reflex panels without a vendor ticket
- **Rich result types**: numeric, qualitative, narrative, imaging, structured molecular — first-class
- **SOP versioning**: every protocol change tracked, point-in-time replay for any inspection date
- **HIPAA, SOC 2 Type II, BAA standard**: documented and shareable with their compliance team

## What works in the first email

- Subject referencing a **specific clinical-quality concern** (audit trail, e-sig, validation, complex test reporting)
- Open with an inspection finding pattern they'd recognize
- Mention Acure (anatomic pathology + reference) — credibility
- CTA: "Worth 10 minutes to walk through how Acure handles [specific scenario]?"

## What kills the email

- Treating them like a buyer (they're a vetoer; route around them at your peril)
- Cost talk (that's CEO; Medical Director cares about quality)
- Marketing language ("transform your lab")
- Mentioning "AI" without specifying what it does and how it's validated
- Russian-origin in-vitro case study (HIPAA panic — anonymize per `../playbooks/russian-segment.md`)

## Cross-references

- Battle card vs LabWare: `../battle-cards/labware_x_medical-director.md`
- Battle card vs Clinisys: `../battle-cards/clinisys_x_medical-director.md`
- Battle card vs lims.net (JTO): `../battle-cards/lims-net_x_medical-director.md`
- Three-phase migration framework: `../playbooks/three-phase-migration.md`
- Acure case study: `../case-studies/acure-reference-lab-nj.md`
