# Proposal: Trust and Readiness Features
### Readiness gates, recurring-finding escalation, a consumable data feed, and value provenance

**Requested by:** Kevin (session decision, drawing on the financial-ai repo's proven patterns)
**Owner:** Strategic Operations · **Audience:** Dean, TCC, unit leaders, dashboard consumers
**Decision this enables:** before anyone opens a dashboard, the system answers "is this
data trustworthy right now?" — and every number shown can say where it came from.

## Why

The Phase 1 and Strategy 2035 changes specify *display* honesty (RAG badges, Live/Stale
states, freshness stamps) but nothing behind them verifies the *system's own* health, and
nothing escalates problems that recur. A sibling pipeline (the financial-ai Workday
reporting system) solved these exact problems in production and its patterns transfer
directly:

- **Fail-closed publishing** — its Close-Readiness gate blocks the monthly pack when a
  blocking condition exists, and writes the gate report even when failing so the blockers
  are readable. CLL dashboards have no equivalent: a stale or broken cycle still renders
  as if fine.
- **Cross-period finding tracking** — findings keyed by type+source escalate on recurrence
  (2+ recurring → flagged, 3+ → escalated, 4+ → blocks approval). CLL specs describe this
  behavior for stale updates (reminders, unit-head escalation) but the demo implements it
  only as one-shot notices.
- **Dashboard feed with manifest** — its dashboard consumes versioned CSVs with a manifest
  (generated-at, source, row counts), written even when empty so consumers render "no
  data" instead of guessing. CLL-SPM has no external feed; publishing one also gives the
  future Power BI model a stable contract.
- **Value provenance, made visible** — every financial figure carries a trust level
  (corroborated / single-source / discrepancy). The strategy-kpi-data spec already
  *requires* source + submitter on every KPI value ("Value provenance" requirement) but
  no surface displays it.

## What Changes

Four features, each an implementation-deepening of an **existing spec requirement** — no
new scope domains:

1. **Cycle readiness gates** (implements status-reporting's currency requirements + the
   refresh-failure honesty in executive-dashboards' Data freshness)
   - A readiness check that answers "can we trust this cycle's dashboard?": status
     currency %, stale-item count, forms/flows reachable, call-up windows expired,
     decisions awaiting action past SLA.
   - Each gate reports OK / WARN / BLOCKING; the readiness page renders *even when
     failing* — blockers are the content, not an error state.
   - Linked from every dashboard page; the Dean sees trust status before portfolio status.

2. **Recurring-finding tracker** (implements F7 hygiene + status-reporting escalation)
   - Findings keyed by type (stale-update, red-without-resolution, unaligned-item,
     triage-overdue, decision-overdue) + affected unit/item.
   - Escalation ladder on occurrence count: 2+ → Recurring flag on the unit view;
     3+ → escalated to governance (appears in TCC Decisions Needed); 4+ → blocks the
     affected item from closing out until resolved.
   - Findings are append-only; resolution clears the counter with a recorded resolution.

3. **Consumable data feed** (implements executive-dashboards' Data freshness for external consumers)
   - A versioned feed (`/api/feed` + JSON/CSV files) carrying headline KPIs, RAG counts
     by priority, currency %, intake aging, readiness summary.
   - `manifest.json` with generated-at, source DB build, row counts; **files are written
     even when empty** (headers only) so consumers render explicit "no data" states.
   - CSV-injection guard on any string cell beginning with `=`, `+`, `-`, `@`.

4. **Value provenance surface** (implements strategy-kpi-data's Value provenance)
   - Every KPI value displayed carries its source, as-of date, and submitter/method —
     surfaced as a tooltip/detail on the Strategy 2035 cards and KPI tables.
   - Values missing a source are already rejected by spec; this change makes the presence
     and identity of the source *visible* to viewers.

## Capabilities

### New Capabilities
- `cycle-readiness` — the readiness gate: checks, OK/WARN/BLOCKING states, page-before-trust linking
- `finding-tracker` — finding types, occurrence counting, escalation ladder, resolution record
- `data-feed` — versioned feed files + manifest, empty-state discipline, injection guard

### Modified Capabilities
- `strategy-kpi-data` — the existing Value provenance requirement gains display-surface scenarios

## Scope

**In scope:** the four features above, implemented in the demo (SQLite + FastAPI flow
engine) with the same shape ready to port to Power Automate/Power BI artifacts.

**Out of scope:**
- LLM/natural-language querying of portfolio data (financial-ai's chat layer — noted for Phase 2+)
- Offline guards, hardware tiers, socket-level privacy proofs (financial-ai's
  privacy hardening is for real financial data; demo data is fabricated)
- Adaptive intake profiling of arbitrary spreadsheets (worth doing later for task 2.10's
  backfill import; deliberately deferred to keep this change cohesive)
- Power BI implementation of any feed visual (feed contract only)

## Success Criteria

| Measure | Target |
|---|---|
| Readiness page renders with all gates OK on a healthy build | Yes, with seeded data |
| Readiness page renders blockers (not an error) when a gate fails | Demonstrated by planted-defect test |
| Escalation ladder fires at 2/3/4 occurrences | Scenario-tested end-to-end |
| Feed manifest present with row counts; empty feed renders "no data" not garbage | Verified |
| Every KPI value shown displays source + as-of | Verified on Strategy 2035 cards and KPI tables |
| Planted spec-violations are caught by the test suite (not just happy paths) | 100% of planted defects |

## Impact

- **Licensing:** none. Demo is local; the same features port to included M365 capability.
- **Tenant:** nothing required from OIT for the demo. (Production Power Automate versions
  of the readiness/finding flows would run on standard connectors already in the design.)
- **People:** Strategic Operations reviews readiness before each monthly cycle; findings
  resolution is recorded by whoever clears them.
- **Testing:** each feature ships with adversarial "planted defect" tests — a defect
  planted in a scratch state must be *caught* by the feature, following financial-ai's
  blind-round evidence pattern (10/10 planted defects, 0 false alarms as the bar).

## Open Questions (none blocking)

| # | Question | Owner | Needed by |
|---|---|---|---|
| 1 | Which gate thresholds (currency % floor, stale count) constitute WARN vs BLOCKING? | Strategic Ops | During implementation; proposed defaults in design |
| 2 | Should the feed be public to all app roles or executive-only? | Dean | Feed ships demo-open; flag exists for production |