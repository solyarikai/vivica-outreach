---
name: lims-pain-extractor
description: Extract the top 2-3 most painful complaints about competitor LIMS vendors from public review sites (G2, Capterra, SourceForge, ITQlick, TrustRadius). Use this skill whenever you need to write a competitor-conquest email sequence, build a battle card, or update the competitor pain corpus that the email-sequence skill draws on. Triggers include any mention of LabWare, LabVantage, QBench, CrelioHealth, LigoLab, Clinisys, CloudLIMS, lims.net (also called JTO), competitor pains, G2 reviews, Capterra reviews, what users dislike about, or "find the top complaints about". Do not run this skill for marketing/positive content — it is specifically for extracting negative signal that justifies migration to Vivica.
---

# lims-pain-extractor — public competitor-pain corpus for Vivica

## Why this skill exists

The default `email-sequence` skill in gtm-mcp generates emails using 12 generic rules. It does not know — and cannot know without external data — what real Lab Directors are complaining about with respect to a specific competing LIMS vendor.

For Vivica's competitor-conquest sequences (e.g. "you're on LabWare, here's why people leave it"), we need real, attributable, recent complaints. Not made up. Not paraphrased to the point of being unrecognizable.

This skill produces a structured corpus of competitor pains that:
- The `email-sequence` skill can pull from when writing competitor-conquest sequences
- The `battle-cards` reference materials can cite directly with a quoted source
- A human reviewer can verify because each complaint is anchored to a public URL

## When to use this skill

Use it when:
- A new competitor is added to the target list (we currently track 8)
- Quarterly refresh of the competitor pain corpus (reviews accumulate, freshness matters)
- Before launching a new competitor-conquest campaign
- A user asks "what do people hate about <vendor>?"

Do NOT use this skill:
- For positive marketing content (use the vendor's own marketing page instead)
- To write the email itself (that's `email-sequence`'s job, this only feeds it)
- To detect which LIMS a specific lab uses (that's `lims-detector`'s job)

## Sources, in priority order

| Priority | Site | Why | URL pattern |
|---|---|---|---|
| 1 | G2 | Best signal — "What do you dislike" is a structured field | `g2.com/products/<vendor-slug>/reviews` |
| 2 | Capterra | Cross-validates G2; same Gartner Digital Markets data lake | `capterra.com/p/<id>/<vendor>/reviews/` |
| 3 | SourceForge | More small/mid-market voices vs G2's enterprise skew | `sourceforge.net/software/product/<vendor>/` |
| 4 | ITQlick | Independent review site, often catches niche LIMS | `itqlick.com/<vendor>` |
| 5 | TrustRadius | Long-form reviews, useful for nuance | `trustradius.com/products/<vendor>/reviews` |
| 6 | Reddit | Unfiltered honesty when present | `reddit.com/search/?q=<vendor>+lims` |

The full URL list per vendor lives in `references/vendor_review_urls.yaml`.

## What "pain" means here

A pain is a **specific, recent, attributable complaint** about a vendor that:
1. Comes from a public review site (URL provable)
2. Is dated 2024 or later (freshness matters — older complaints may have been fixed)
3. Falls into one of 8 standard themes (see below)
4. Has at least one direct quote of ≤15 words (copyright-safe paraphrasing rule)

We classify each complaint into one of these 8 themes:

| Theme | Examples |
|---|---|
| `ux` | Cluttered interface, too many clicks, slow navigation |
| `performance` | Crashes, freezes, slow load times, system hangs |
| `integration` | Hard to connect to instruments, brittle HL7/FHIR, vendor lock-in |
| `support` | Slow response, paid-only support, knowledge gaps |
| `reporting` | Inflexible reports, BO/Crystal pain, can't customize |
| `migration` | Hard to import data, data loss during onboarding |
| `pricing` | Hidden costs, per-user pricing surprises, mandatory consulting |
| `compliance` | Audit trail gaps, e-sig issues, version control |

Each pain in the corpus has these fields:

```yaml
- vendor: labware
  theme: integration
  count: 14                      # how many distinct reviews mention this
  intensity: 4.2                 # average severity, 1-5 scale
  most_recent: 2025-09           # most recent review month touching this theme
  quote: "Integration with other instrument software needed more efforts."
  quote_length_words: 9          # copyright safety check — must be ≤15
  source_url: https://www.g2.com/products/labware-lims/reviews/labware-lims-review-6945687
  source_site: g2
```

## Output structure

```
~/.gtm-mcp/projects/vivica/competitor_pains/
├── corpus.json                  # all vendors, all themes, machine-readable
├── refreshed_at.txt             # ISO date of last refresh
└── per_vendor/
    ├── labware.md               # human-readable digest per vendor
    ├── labvantage.md
    ├── qbench.md
    ├── creliohealth.md
    ├── ligolab.md
    ├── clinisys.md
    ├── cloudlims.md
    └── lims_net.md              # also known as JTO
```

The per-vendor markdown files are also copied into this repo at
`reference/competitors/<vendor>.md` so the email-sequence skill and battle-cards
can read them as part of the version-controlled repo.

## Workflow

```
1. For each vendor in references/vendor_review_urls.yaml:
     For each source URL:
       - web_fetch the page (paginate if needed)
       - extract structured fields:
         - reviewer name (anonymized)
         - star rating
         - "What do you dislike" text (or equivalent dislike field)
         - review date
       - dedupe across sites by hash(reviewer_name + vendor)
       - filter to reviews dated 2024+

2. For each vendor, cluster the dislike texts by theme:
     - prompt the LLM with the 8 standard themes
     - one review can map to multiple themes
     - keep the original raw quote alongside the theme tag

3. Score each (vendor, theme) cluster:
     - count: number of reviews mentioning it
     - intensity: avg(1 to 5) where 1=minor nitpick, 5=blocker
     - most_recent: max(review_date) in the cluster

4. Pick top 3 themes per vendor by (count × intensity × recency_decay).

5. For each top theme, pick ONE representative quote ≤15 words.
   If the natural quote is longer, paraphrase to ≤15 words but keep
   the source URL for attribution.

6. Write corpus.json + per-vendor markdown.
```

## Copyright safety — non-negotiable

Every quote in the corpus MUST be:
- ≤15 words from any single review
- Attributed to a public source URL
- Used at most once per source (no stringing multiple quotes from one review)

If a complaint can only be expressed by quoting more than 15 words, **paraphrase it entirely** and drop the quote. The source URL stays so a human can verify.

## How email-sequence uses this corpus

The `email-sequence` skill, when generating a competitor-conquest email for vendor X, reads `~/.gtm-mcp/projects/vivica/competitor_pains/corpus.json`, picks the top theme for vendor X, and inserts the quote naturally:

> Subject: that LabWare integration headache  
> Hey {{firstName}},  
>
> A Lab Director wrote on G2 about LabWare: *"Integration with other instrument software needed more efforts."*  
> Most clinical labs that migrated to Vivica from LabWare cite this exact pain. Worth a 10-min look at how we handle it for {{specialization}}-focused workflows?

The quote does the persuasion. We provide the platform, not the opinion.

## Refresh cadence

- **First run**: when the project is initialized (now)
- **Quarterly**: re-run to capture fresh reviews
- **Ad-hoc**: when a new competitor is added or a campaign reports low reply rates that suggest pains are stale

## Usage

```bash
# Full corpus refresh, all 8 vendors
python scripts/extract_pains.py \\
    --vendors-file references/vendor_review_urls.yaml \\
    --output ~/.gtm-mcp/projects/vivica/competitor_pains/ \\
    --repo-mirror ~/code/vivica-outreach/reference/competitors/

# Single vendor refresh (e.g. just QBench)
python scripts/extract_pains.py \\
    --vendor qbench --output <dir> --repo-mirror <dir>
```

## What this skill does NOT do

- Does NOT modify the email-sequence skill or its 12 rules
- Does NOT write emails directly — only feeds the corpus that email-sequence reads
- Does NOT detect which LIMS a lab uses (use `lims-detector`)
- Does NOT scrape positive content or feature comparisons (only pains)

## See also

- `references/vendor_review_urls.yaml` — full URL list per vendor
- `references/theme_guide.md` — how to classify reviews into the 8 themes
- `../../reference/battle-cards/` — where the corpus is consumed
