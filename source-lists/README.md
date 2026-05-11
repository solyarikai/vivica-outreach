# source-lists/

Company lists at every lifecycle stage: raw external dumps → enrichment runs → final merged segments.

See [[AGENTS]] § Enrichment Run Convention for the rules.

## Layout

```
source-lists/
  <source-name>/                                  # raw external data, immutable
    e.g. clia-q1-2026/                            # CMS POS Q1 2026 + segmented buckets
  enrichment-runs/                                # one folder per data operation
    <YYYY-MM-DD>_<segment>_<tool>/
      input.csv
      output.csv
      stages/                                     # optional, for multi-step runs
      manifest.md                                 # mandatory: what/why/counts/status
  segments/                                       # final merged artifacts → downstream pipeline
```

## Rules (short version)

1. **Raw is immutable.** Anything in `<source-name>/` (e.g. `clia-q1-2026/`) is source-of-truth — don't edit, don't overwrite.
2. **Every data op gets its own run folder** — date-prefixed, with `manifest.md`. No flat dumps.
3. **Append, don't edit.** Bad run? Supersede with a new run folder, mark old `status: superseded-by-<run-id>` in its manifest.
4. **Log every run** in `tracking/data-log.md` with one line + pointer to manifest.
5. **Final merged outputs** go to `segments/`, never to `enrichment-runs/`.

## Current runs

See [[data-log]] for the full append-only journal.
