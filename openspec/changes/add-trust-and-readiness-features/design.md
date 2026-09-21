# Design: Trust and Readiness Features

## Context

Four features transfer proven patterns from the financial-ai Workday pipeline (fail-closed
publishing, cross-period finding escalation, manifest'd dashboard feed, visible
provenance) into CLL-SPM's demo and its port-to-M365 trajectory. Each implements an
*existing* spec requirement more deeply; none opens a new scope domain.

```
readiness gates ──> trust banner on every page ──> readiness page (renders blockers)
finding tracker ──> unit "Recurring" marks ──> governance escalation ──> closeout block
data feed ────────> demo/output/feed/*.csv + manifest.json ──> /api/feed ──> Power BI spine
provenance ───────> source/as-of/submitter visible on every KPI value
```

## Decisions

### D1. Readiness gates are computed queries, not a stored state
Gates re-evaluate on every readiness page load and every feed export from the live
database — no persistence to go stale. A gate is a named check with a value, threshold,
and state function. The gate list is data (a Python registry in `demo/readiness.py`),
not config, so adding a gate is a code change reviewed with everything else.

**Proposed defaults (open question 1; Strategic Ops calibrates):**

| Gate | WARN | BLOCKING |
|---|---|---|
| Status currency % | < 95% | < 90% (Phase 1 success criterion) |
| Stale active items | ≥ 1 | ≥ 10% of active items |
| Expired call-up windows unclosed | ≥ 1 | — |
| Decisions past SLA (5/10 business days) | ≥ 1 | ≥ 5 |
| Flow/form reachability | — | any core route unreachable |

**Why compute-don't-store:** a stored readiness flag would itself need freshness
monitoring (the recursion financial-ai avoided by making Close-Readiness a pure function
of the corpus). Pure-function readiness is always truthful about the moment you ask.

### D2. Readiness page renders blockers as content
Following Close-Readiness: the page is written *even when failing* — failing gates sort
first with their detail. Dashboards stay reachable but carry a degraded-trust banner
linking to readiness when any gate is BLOCKING. **Why not hard-block dashboards:** the
Dean needs to see the portfolio *and* its trust state together; hiding data entirely
would itself be a trust failure.

### D3. Findings: append-only records keyed by (type, affected)
Table `Findings` with `FindingId, Type, AffectedUnitId, AffectedItemId, Severity,
FirstSeenOn, LastSeenOn, Occurrences, Status(Open/Resolved), ResolvedBy, ResolvedOn`.
The daily hygiene run (F7 extension) is the writer. Keyed on (type + affected item) so
occurrences accumulate across cycles; resolution appends a status change — the row is
never edited or deleted (matching the Decisions list discipline already in the design).

**Escalation ladder** (from finding_tracker.py's 2/3/4 rule):

| Occurrences | Action |
|---|---|
| 2 | Recurring marker on the item in the unit view |
| 3 | Surfaces on governance view in needs-attention list |
| 4 | Stage gate blocks the affected item from moving to Closed |

The closeout-block reuses the existing stage-gate mechanism (the same gate that enforces
charter/closeout checks), adding one condition: no Open finding with 4+ occurrences on
the item. **Why not block earlier:** 2–3 occurrences are visibility tools for the unit
head; 4 is chronic and deserves a hard stop before an item escapes review at close.

### D4. Feed: files first, endpoint reads files
`demo/export_feed.py` writes `demo/output/feed/` — kpis.csv, rag-counts.csv,
currency.csv, intake-aging.csv, readiness.json, manifest.json — with FEED_VERSION = 1.
The `/api/feed` endpoint serves those files; the dashboard does NOT read them (it queries
the DB directly; the feed is for external consumers). Files are written even when empty
(headers only) and the manifest records per-file row counts.

**Injection guard:** any string cell starting with `=`, `+`, `-`, `@` is prefixed with
`'` (exact port of financial-ai's V-07 guard — numeric cells untouched).

**Why files-not-just-API:** the Power BI spine in the production design reads
SharePoint lists; the demo feed's file shape (stable filenames + manifest) is the contract
that maps 1:1 onto that spine. Tests assert the file contract, so the contract survives
implementation changes.

### D5. Provenance display uses data already captured
KpiValues already carries ValueNote + SubmittedBy; the strategy route already computes
data states. This change threads the source/as-of/submitter into the card detail and KPI
tables (tooltip in production Power BI; visible sub-label in the demo). No schema
change needed — the strategy-kpi-data spec already requires source on capture.

### D6. Planted-defect tests are part of every feature
Each feature ships with an adversarial test that plants a violating state in a scratch DB
and asserts the feature *catches* it: a currency gate that stays OK when items are stale
fails the test; a finding that doesn't increment across cycles fails; a feed that omits
empty files fails; a card that renders a value without provenance fails. The bar is
financial-ai's blind-round evidence standard: planted defects 10/10, false alarms 0.

## Data model additions

| Table | Fields |
|---|---|
| `Findings` | FindingId, Type, AffectedUnitId, AffectedItemId, Severity, FirstSeenOn, LastSeenOn, Occurrences, Status, ResolvedBy, ResolvedOn |

No other tables change. Readiness is computed (D1); feed is derived (D4); provenance is
display (D5).

## Production port map (demo → M365)

| Demo | Production |
|---|---|
| `demo/readiness.py` gates | A Power Automate "readiness" flow computing gates into a `ReadinessState` list, or Power BI measures computed at refresh |
| `Findings` table | SharePoint `Findings` list written by the F7 hygiene flow |
| Feed files + manifest | The SharePoint lists *are* the feed; the manifest concept becomes the freshness stamp (already specced) |
| Provenance sub-labels | Power BI tooltips bound to the same KpiValues columns |

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Gate thresholds miscalibrated → nagging or false trust | Thresholds are named data (D1), Strategic Ops calibrates; WARN before BLOCKING everywhere |
| Finding escalation becomes bureaucratic noise | Ladder starts at visibility (2), hard action only at 4; resolution resets counters |
| Feed consumers depend on demo file shape | FEED_VERSION + manifest; contract tested, versioned changes only |
| Readiness page used to *avoid* the dashboard | Trust banner links back; degraded ≠ hidden (D2) |
| Duplicate escalation paths (findings vs F7 notices) | F7 hygiene run is the single writer of findings; notices derive from the same records |

## Rollout

| Step | Milestone |
|---|---|
| 1 | Findings table + hygiene-writer + escalation ladder + stage-gate block; planted-defect tests |
| 2 | Readiness gates + page + trust banner on all pages; planted-defect tests |
| 3 | Feed exporter + endpoint + manifest; injection-guard + empty-file tests |
| 4 | Provenance display on Strategy 2035 cards and KPI tables; visibility tests |
| 5 | Full regression (routes, flows, visuals, hand-check) + adversarial battery run |