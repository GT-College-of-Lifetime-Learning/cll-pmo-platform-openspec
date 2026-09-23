# Design: implement-cll-pmo-platform-v1

## Context

The platform sits downstream of eleven enterprise sources and upstream of two
audiences with very different tolerances: PMO staff who need working data daily,
and the Board of Advisors who need numbers that are defensible a year later.

That split drives the central design constraint: **operational views may be
live; board-facing views must be snapshot-backed and reproducible.**

## Architecture overview

```
  Enterprise sources (11)            Platform                       Consumers
  ------------------------           --------                       ---------
  Workday Financials  ─┐
  Workday HCM         ─┤
  Banner              ─┤   ┌─────────┐   ┌──────────┐   ┌─────────┐
  Salesforce          ─┼─►│ Landing │─►│ Conformed│─►│ Portfolio│─► Executive
  Smartsheet          ─┤   │ (raw)   │  │ (typed,  │  │ model    │   dashboard
  ServiceNow          ─┤   │ immutable│ │  quality- │ │ (facts + │─► Board
  Canvas LMS          ─┤   │  by run) │ │  checked) │ │  snapshots)│  package
  IR warehouse        ─┤   └─────────┘  └──────────┘  └─────────┘─► API
  Entra ID            ─┤        │            │              │
  SharePoint (board)  ─┘        └── quarantine ┘── audit log ─┘
```

Four zones:

1. **Landing** — raw payload per run, immutable, retained per NFR-006. Enables
   replay (DQA-006) and backfill (INT-010) without re-reading the source.
2. **Conformed** — typed, deduplicated, quality-checked entities. Data quality
   rules (DQA-001/DQA-002) execute on entry to this zone; failures are
   quarantined rather than dropped.
3. **Portfolio model** — the governed star-shaped model: `project`, `kpi`,
   `kpi_measurement`, `milestone`, `raid_item`, `financial_actual`,
   `gate_decision`, plus conformed dimensions (`pillar`, `objective`, `unit`,
   `person`, `funding_source`, `period`).
4. **Snapshot store** — immutable, labelled point-in-time captures of the
   portfolio model used by board reporting (BRD-003) and restatement disclosure
   (BRD-006, KPI-006).

## Key decisions

### D1 — Snapshot-backed board reporting rather than live queries

**Decision:** every board-facing figure is read from a labelled snapshot, never
from the live model.

**Why:** the board question that matters is "what did we report and why", asked
months later. Live queries cannot answer it once upstream data mutates.

**Rejected:** (a) live queries with an as-of filter — fails when a source
retroactively edits history, which Workday does routinely for accruals;
(b) exporting to static files only — loses queryability and lineage.

**Cost:** storage growth and an explicit snapshot lifecycle (NFR-006).

### D2 — Source of record stays upstream; the platform is a system of reference

**Decision:** the platform does not become the system of record for finance, HR,
student or CRM data. It is authoritative only for portfolio constructs it
originates: project registry entries, KPI definitions, gate decisions, RAID
items and narrative.

**Why:** dual-master data is the most common failure mode in PMO platforms.

**Consequence:** reconciliation (DQA-003) is a first-class requirement, and
write-back is deliberately narrow — see
`decisions/synchronization-ownership.md`.

### D3 — KPI definitions are versioned data, not code

**Decision:** a KPI is a registry row with a definition, filter expression,
unit, cadence, steward and version. Calculation logic references the registry;
changing a definition creates a new version and triggers restatement handling
(KPI-006).

**Why:** KPI definitions are contested and change more often than code ships.
Encoding them in code makes every definition change a release.

**Rejected:** hard-coded metric logic per dashboard tile — the current failure
mode, where the same KPI differs per deck.

### D4 — Access control enforced in the data layer, not the presentation layer

**Decision:** RBAC roles (SEC-002) plus row-level scoping predicates (SEC-003)
are applied where the query executes. The dashboard and the API receive
already-scoped results.

**Why:** three consumers (dashboard, API, export) means presentation-layer
filtering would be implemented three times and would drift.

### D5 — Contract-first integration with explicit versioning

**Decision:** each source integration has a written data contract
(`contracts/integration-data-contracts.md`) specifying fields, types, keys,
cadence, volume, SLA and breaking-change policy. Ingestion validates payloads
against the contract and fails closed.

**Why:** silent schema drift produces wrong board numbers, which is worse than
a missing feed.

**Consequence:** INT-011 requires a 30-day deprecation notice and dual-running
of contract versions.

### D6 — Fail closed, quarantine, never silently drop

**Decision:** records failing a blocking quality rule are quarantined with the
rule id and raw payload, and are replayable after remediation (DQA-005,
DQA-006). Aggregates computed over incomplete data carry a completeness flag
surfaced by EXD-007.

**Why:** a visibly stale dashboard is recoverable; a confidently wrong one is
not.

### D7 — Phase gating tied to release gates, not calendar dates

**Decision:** GATE-0 … GATE-8 close on evidence, with named approvers
(`registries/release-gates.md`, `registries/approval-sequences.md`). Schedule
pressure is handled by descoping requirements, not by skipping gates.

## Data model sketch

| Entity | Grain | Authoritative source |
|---|---|---|
| `project` | one strategic project | Platform (PRJ-001) |
| `project_state_history` | one state transition | Platform (PRJ-002, PRJ-008) |
| `pillar` / `objective` | Strategy 2035 taxonomy | Strategy Office (PRJ-003) |
| `milestone` | one dated deliverable | Smartsheet, mirrored (INT-005) |
| `raid_item` | one risk/issue/decision/dependency | Platform (PRJ-006) |
| `kpi` | one KPI definition version | Platform (KPI-001, KPI-006) |
| `kpi_measurement` | KPI x period x scope | Computed (KPI-002, KPI-004) |
| `financial_actual` | account x period x project | Workday Financials (INT-001) |
| `effort_allocation` | position x period x project | Workday HCM (INT-002) |
| `gate_decision` | one gate x one project | Platform (GOV-001) |
| `snapshot` | one labelled capture | Platform (BRD-003) |

## Cross-cutting decision records

- `decisions/security-and-identity.md` — identity, roles, scoping, audit,
  secrets, recertification (governs SEC-001 – SEC-007).
- `decisions/synchronization-ownership.md` — per-field ownership, write-back
  direction, conflict resolution and cadence (governs INT-001 – INT-010,
  DQA-003).

## Nonfunctional posture

| Concern | Target | Requirement |
|---|---|---|
| Dashboard first paint | p95 ≤ 3.0 s, p99 ≤ 5.0 s at 150 concurrent users | NFR-001 |
| Availability | 99.5% monthly, business hours 07:00–19:00 ET | NFR-002 |
| Recovery | RPO ≤ 4 h, RTO ≤ 8 h | NFR-002 |
| Scale | 500 projects, 250 KPIs, 5 years of monthly history | NFR-003 |
| Observability | 100% of ingestion runs emit structured run records | NFR-004 |
| Accessibility | WCAG 2.2 AA | NFR-005, EXD-008 |
| Retention | Snapshots 7 years; landing 400 days | NFR-006 |

## Migration and rollout

1. Phases 00–01 establish environments and source alignment with no user-facing
   surface.
2. Phase 02 loads the registry from the existing Smartsheet inventory; the PMO
   runs old and new in parallel for one reporting cycle.
3. Phase 04 opens the dashboard to PMO staff, then pillar owners, then the
   leadership team.
4. Phase 07 produces one shadow board package alongside the manual package; the
   manual process is retired only after the two reconcile (DQA-003 evidence).

## Alternatives considered and rejected

| Alternative | Why rejected |
|---|---|
| Buy a commercial PPM suite outright | Cannot express Strategy 2035 pillar taxonomy or the institutional KPI governance model; integration cost comparable |
| Build on Smartsheet dashboards alone | No snapshotting, no row-level institutional access control, no lineage |
| Warehouse-only (BI semantic layer, no application) | Cannot capture gate decisions, RAID or narrative — these originate in the platform |
| Event-driven streaming ingestion | Sources are batch-oriented; streaming adds operational burden without improving quarterly reporting |
