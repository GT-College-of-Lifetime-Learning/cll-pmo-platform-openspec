# Design: Data Source Reconciliation

## Context

P1 (fabricated demo) is complete and is the schema contract. This change builds the P2
instrument (reconcile what we have vs. need) and the P3 pattern (integrate what we
have, incrementally; plan what must be built). The financial-ai patterns that transfer:
the intake advisor's needs-assessment (profile what exists against canonical needs) and
the input-coverage analyzer (does the corpus form a complete picture).

```
backwards map (done)  →  DataNeeds catalog  →  coverage view (truth per visual)
steward declarations  →  source states       →  matrix (generated, never hand-edited)
confirmed HAVE rows   →  tagged imports      →  provenance already displays origin
```

## Decisions

### D1. The catalog is a table in the working store
`DataNeeds` (table, later a SharePoint list): NeedId, Element, ConsumerView,
RequiredFields, Cadence, DefinitionState (defined/undefined-question-id), SourceState
(UNDEFINED/MISSING/PARTIAL/HAVE), SourceSystem, SourceFormat, SourceRefresh, Steward,
Notes. Seeded from the session's backwards map (~25 rows: 12 KPIs, 6 activity types,
capability-inventory fields, hub locations, GT holidays).

**Why a table and not the matrix doc:** the matrix is a *view*; if it were the source of
truth it would drift the moment someone hand-edits it (the spec's rejected-drift
scenario). One table, one generated document, one truth.

### D2. Declarations are data files with a capture flow
`source-declarations.csv` (steward-submitted, one row per source: Element, System,
Format, Refresh, Steward, Notes) + a loader that matches rows to catalog elements by
name (fuzzy on the KPI/element names the matrix publishes), records the match, and
holds unmatched declarations in a review queue instead of silently creating rows.
In production this becomes a declaration form (Forms + flow), same fields.

### D3. Origin tagging on the rows that carry values
`DataSource` column on the value-bearing tables already provenance-adjacent:
`KpiValues`, `StrategyActivity`, `Capabilities`, and the business-day calendar import
(`DataSource`: `demo-seed` default | `imported:<name>` | `manual:<owner>`). The
provenance display (strategy-kpi-data spec) already renders a source string; imports
write theirs there, demo rows say so honestly. **No visual changes needed** — the tag
rides the existing provenance line.

### D4. Imports are per-source loader scripts, not a generic importer
Each confirmed HAVE source gets a small loader (mirroring `seed_loader.py`):
declared fields → list fields, validation (type coercion, required fields, tie-outs
where the source has internal totals), then tagged insert. Generic CSV-import invites
schema drift; per-source loaders keep every mapping reviewable and portable to
production (each becomes a scheduled import or form in M365).

**First increment (agreed): the Institute holiday calendar** — smallest real source,
already REVIEW-flagged in `gen_business_days.py`, unblocks exact business-day math
everywhere (call-up windows, SLAs, readiness gates).

### D5. Coverage view is computed from the catalog, per consumer view
`/coverage` page + feed file: per row — sourced / partial / unsourced; grouped by
ConsumerView so each dashboard page states what it can truthfully show. Aggregates
flow into the readiness feed (`coverage.json` in `export_feed.py`) so external
consumers see coverage without scraping the page.

### D6. The matrix generator fails on drift
`demo/generate_matrix.py` renders `docs/data-source-matrix.md` from the catalog.
It compares its rendering against the committed file; if a hand edit exists, it
reports the drift and rewrites with catalog truth (spec scenario). CI-wise: the
test suite asserts the committed matrix equals the generator output.

## Data model additions

| Table | Fields |
|---|---|
| `DataNeeds` | NeedId, Element, ConsumerView, RequiredFields, Cadence, DefinitionState, SourceState, SourceSystem, SourceFormat, SourceRefresh, Steward, Notes |
| `SourceDeclarations` | DeclarationId, Element, System, Format, Refresh, Steward, Notes, MatchedNeedId, RecordedOn |

Plus `DataSource` column added to: `KpiValues`, `StrategyActivity`, `Capabilities`.
(The holiday import replaces the calendar file content — its origin is recorded in
the catalog row, not per-row.)

## Loader pattern (per-source, the P3 loop)

```
1. Steward declaration lands (D2) → catalog row flips to HAVE/PARTIAL
2. Loader script for that source: source file → validated mapping (D4)
3. Tagged import with origin (D3); tie-outs recorded in the loader output
4. Coverage view + feed reflect the new truth (D5)
5. Production port notes appended to the catalog row (which M365 mechanism)
```

## Production port map (demo → M365)

| Demo | Production |
|---|---|
| `DataNeeds` table | SharePoint `DataNeeds` list (Strategic Ops maintained) |
| Declaration CSV + loader | Declaration form (Forms) + capture flow (Power Automate) |
| Per-source loader scripts | Scheduled imports (Power Automate) or manual entry per source-build plan |
| `/coverage` view + feed file | Power BI coverage page reading the `DataNeeds` list |
| Matrix generator | Docs-as-code: same generator, catalog list source |

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Catalog rows go stale as visuals evolve | Backwards-map review is part of any new visual's task list; generator/test fails the matrix on drift |
| Steward declarations are wrong or overclaim | PARTIAL exists precisely for this; first import validates with tie-outs before the row is trusted |
| Real data contradicts demo data visually | Origin tags make the mixture explicit; coverage view states which rows are unsourced |
| UNDEFINED rows get built anyway (wasted work) | Spec routes UNDEFINED to the sponsor; coverage view lists them separately; no loader exists until a definition lands |
| One-at-a-time integration feels slow | Each increment is small, independent, and immediately visible in coverage; nothing blocks on a big-bang |

## Rollout

| Step | Milestone |
|---|---|
| 1 | `DataNeeds` + `SourceDeclarations` schema; catalog seeded from the backwards map (~25 rows) |
| 2 | `/coverage` view + feed coverage file; provenance DataSource tags |
| 3 | Matrix generator + drift test; `docs/data-source-matrix.md` committed |
| 4 | Declaration capture (CSV + loader + review queue); sample declaration walkthrough |
| 5 | First integration increment: confirmed GT holiday calendar → business days, tagged + tested |
| 6 | Planted-defect suite: undefined-routes-before-build, drift-rejection, masquerade-guard, coverage-truth |