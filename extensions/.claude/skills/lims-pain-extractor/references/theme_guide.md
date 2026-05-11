# Theme Classification Guide — lims-pain-extractor

How to classify a single LIMS review's "dislike" text into one or more of 8 standard themes. Used by `extract_pains.py` when it asks an LLM (Claude in Claude Code, or Anthropic API in standalone mode) to classify reviews.

## The 8 themes

A review can map to **multiple themes**. Pick all that apply.

### `ux`
**Trigger**: complaints about how the interface looks or feels to use.

Includes:
- Cluttered interface, too many menus
- Too many clicks to do common tasks
- Slow / unresponsive navigation
- Unintuitive layouts, hard to find features
- Looks dated / "1990s" / "Windows XP era"
- Different modules feel inconsistent

Excludes:
- "It crashes" → that's `performance`
- "I can't customize the layout" → that's `reporting` (if reports) or `ux` (if general)

### `performance`
**Trigger**: the system breaks or stalls.

Includes:
- Crashes, freezes, app hangs
- Slow load times, slow page rendering
- Database queries timeout
- System unresponsive under load
- Memory leaks, requires restart

Excludes:
- "It's slow because the menu is too deep" → `ux`
- "Reports take forever to generate" → could be `performance` OR `reporting` (use both)

### `integration`
**Trigger**: connecting to external systems is hard.

Includes:
- Hard to connect to instrument analyzers
- HL7 / FHIR / ASTM brittle or partially supported
- Vendor lock-in via proprietary interfaces
- Integration to LIS / EHR / billing requires custom dev work
- Integration breaks after vendor updates

Excludes:
- "Their API is undocumented" → `support` (knowledge gap) + `integration`
- "Their pricing for integrations is high" → `pricing` + `integration`

### `support`
**Trigger**: getting help is slow, expensive, or low-quality.

Includes:
- Slow response time on tickets
- Paid-only support / mandatory premium tier
- Knowledge gaps in support team
- Onboarding/training resources thin
- Documentation outdated or missing
- Forced to escalate to consulting fees

Excludes:
- "Their support is in the wrong time zone" → `support` (most likely) but flag if it's specifically a regional / language issue (relevant for lims.net / JTO)

### `reporting`
**Trigger**: getting data out for clients, regulators, or internal use.

Includes:
- Inflexible report templates
- BO / Crystal Reports complexity
- Can't customize report layout without vendor / consultant
- Limited export formats
- New client report formats require change orders
- Hard to schedule recurring reports

Excludes:
- "I can't export raw data" → `integration` (data egress) + `reporting`
- "Reports are slow to render" → `performance` + `reporting`

### `migration`
**Trigger**: getting data IN, OUT, or AROUND the system is hard.

Includes:
- Hard to import historical data during onboarding
- Data loss during migration
- Painful transitions from previous LIMS
- Hard to leave (export your own data)
- Backup / restore complicated

Excludes:
- "Day-to-day data entry is hard" → `ux`
- "Integration with instruments is brittle" → `integration`

### `pricing`
**Trigger**: cost surprises or perceived value problems.

Includes:
- Hidden costs (true cost much higher than list price)
- Per-user pricing surprises (charged for inactive users, etc.)
- Mandatory consulting fees on every change
- License model unclear / opaque
- Expensive professional services required
- Annual increases beyond expectation
- ROI questioned / "not worth the price"

Excludes:
- "Customizations cost extra" → `pricing` AND `integration` if customization is around integrations

### `compliance`
**Trigger**: regulatory / quality / audit issues.

Includes:
- Audit trail gaps
- E-signature workflow problems
- Version control gaps on SOPs / methods
- Result modification controls weak
- HIPAA / SOC 2 / CLIA / CAP feature gaps
- Hard to pass inspections / audits
- Validation documentation thin

Excludes:
- "I can't generate the audit report I want" → `reporting`
- "Compliance requires me to log in differently" → `ux` (login flow)

## Multi-theme examples

Real review text often hits multiple themes. Examples:

| Review text | Themes |
|---|---|
| "Customizations cost a fortune and take months" | `pricing`, `support` (vendor friction), `integration` (if it's integration customization) |
| "Reports are slow and hard to customize" | `performance`, `reporting` |
| "Audit trail exists but exporting it for inspection is painful" | `compliance`, `reporting` |
| "Their support is great when they respond, but you wait days" | `support` (treat as moderate negative — quality is fine, latency isn't) |
| "Login screen freezes once a week and IT has to restart it" | `performance`, `ux` (login experience) |

## Intensity scoring (1-5)

For each theme assigned, score intensity:

| Score | Meaning | Example language |
|---|---|---|
| 1 | Minor nitpick | "I wish they'd update the icon set" |
| 2 | Mild annoyance | "The menu structure could be better" |
| 3 | Real complaint | "Reports take longer than they should" |
| 4 | Significant pain | "We've considered switching because of how brittle integrations are" |
| 5 | Blocker / dealbreaker | "We had to rebuild our entire reporting layer because their tool is unusable" |

## Tone calibration

Reviewers often use understatement (especially in pharma / regulated industries). Read past surface politeness:

- "Could be better" → score 3, not 1, in this domain
- "We make it work" → likely score 3-4 (they tolerate, don't endorse)
- "It's fine for what it is" → backhanded, often score 3
- Direct negative ("terrible", "unusable") → trust the language, score 4-5

## Output format

```yaml
- vendor: labware
  theme: integration  # one entry per (vendor, theme) cluster
  count: 14           # how many reviews mention this theme
  intensity: 4.2      # average intensity across reviews in cluster
  most_recent: 2025-09  # most recent review in cluster
  quote: "Integration with other instrument software needed more efforts."
  quote_length_words: 9  # MUST be ≤15
  source_url: https://www.g2.com/products/labware-lims/reviews/...
  source_site: g2
```

## Cross-references

- Skill: `../SKILL.md`
- Vendor URL list: `vendor_review_urls.yaml`
- Code: `../scripts/extract_pains.py` (`THEME_GUIDE` constant)
- Glossary: `../../../../../glossary.md` → "Theme classification"
