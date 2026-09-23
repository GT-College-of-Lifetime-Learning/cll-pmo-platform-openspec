# Decision Record: Synchronization and Data Ownership

**ID:** DR-SYNC-001
**Status:** Accepted
**Date:** 2026-09-23
**Deciders:** Data Engineering Lead (owner), Data Governance Lead, PMO Portfolio Manager, Smartsheet system owner
**Governs requirements:** INT-001 – INT-011, DQA-003, PRJ-001, PRJ-005, PRJ-007
**Gate:** must be Accepted before GATE-1 closes; write-back provisions before GATE-6

## Context

Design decision D2 states the platform is a system of reference, not a system of
record, for enterprise data. That principle only prevents dual-master problems
if ownership is decided **per field**, not per system. Two fields in the same
record can legitimately have different masters — a project's budget is owned by
Workday while its strategic pillar is owned by the platform.

## Decisions

### DR-SYNC-001.1 — Field-level ownership matrix

One writer per field. The platform rejects, and logs, any attempt to write a
field it does not own.

| Entity.field | Master | Direction | Cadence | Conflict rule |
|---|---|---|---|---|
| `project.project_id` | Platform | — | on create | Platform-generated, immutable |
| `project.name` | Platform | Platform → Smartsheet | on change | Platform wins; Smartsheet renames are reverted and logged |
| `project.lifecycle_state` | Platform | Platform → Smartsheet | on change | Platform wins |
| `project.pillar_id` / `objective_id` | Platform (Strategy Office taxonomy) | — | on change | Platform wins |
| `project.owner_person_id` | Platform | — | on change | Platform wins; validated against Workday HCM person |
| `project.smartsheet_id` | Smartsheet | Smartsheet → Platform | daily | Source wins |
| `milestone.*` (name, dates, % complete) | Smartsheet | Smartsheet → Platform | 4x daily | Source wins; platform edits blocked |
| `milestone.gate_flag` | Platform | Platform → Smartsheet | on change | Platform wins |
| `financial_actual.*` | Workday Financials | Workday → Platform | nightly | Source wins absolutely; no write-back |
| `project.budget_amount` | Workday Financials | Workday → Platform | nightly | Source wins |
| `effort_allocation.*` | Workday HCM | Workday → Platform | weekly | Source wins; no write-back |
| `person.*` | Workday HCM (worker) / Entra ID (identity) | Source → Platform | daily | HCM wins for employment attributes, Entra ID for identity and group |
| `enrollment_metric.*` | Banner via IR warehouse | Source → Platform | nightly | Source wins |
| `partner_opportunity.*` | Salesforce | Salesforce → Platform | 2x daily | Source wins |
| `demand_request.*` / `incident.*` | ServiceNow | ServiceNow → Platform | hourly | Source wins |
| `course_engagement.*` | Canvas LMS | Canvas → Platform | weekly | Source wins |
| `kpi.*` (definition, target, threshold) | Platform | — | on change | Platform is master; versioned per KPI-006 |
| `kpi_measurement.value` | Platform (computed) | — | per cadence | Recompute only within an open period; closed periods are immutable |
| `raid_item.*` | Platform | — | on change | Platform is master |
| `gate_decision.*` | Platform | — | on decision | Platform is master; immutable once recorded |
| `narrative.*` | Platform | Platform → SharePoint (package only) | per reporting cycle | Platform wins |
| `snapshot.*` | Platform | — | on creation | Immutable |

### DR-SYNC-001.2 — Write-back is limited to Smartsheet, and to four fields

The only write-back path in v1 is to Smartsheet: `project.name`,
`project.lifecycle_state`, `milestone.gate_flag` and a read-only status summary
cell. No write-back to Workday, Banner, Salesforce, ServiceNow or Canvas under
any circumstance.

**Why:** write-back multiplies failure modes and requires change control in the
upstream system. The four permitted fields are ones the platform originates and
that Smartsheet users need to see in place.

**Rejected:** bi-directional milestone sync — last-writer-wins on dates would
silently corrupt project plans.

### DR-SYNC-001.3 — Late-arriving and retroactive data

Workday routinely restates prior-period financials. Therefore:

- Financial ingestion re-reads a trailing 90-day window each night, not only new
  records.
- A restatement that changes a **closed** reporting period does not mutate the
  reported figure. It creates a restatement record surfaced by BRD-006 and
  KPI-006.
- Open periods absorb restatements silently; the freshness indicator (EXD-007)
  shows the effective as-of timestamp.

### DR-SYNC-001.4 — Deletes are never propagated as deletes

A record absent from a source feed is marked `inactive` with a
`last_seen_at` timestamp; it is never hard-deleted. Hard deletion happens only
through the retention policy (NFR-006).

**Why:** source feeds fail partially. A partial feed must not silently erase
portfolio history.

### DR-SYNC-001.5 — Reconciliation is mandatory and scheduled

Every source with a financial or reported-metric impact reconciles against the
source of record on a defined cadence (DQA-003):

| Reconciliation | Cadence | Tolerance | Owner |
|---|---|---|---|
| Financial actuals vs Workday ledger | Monthly at close | $0 variance on total, $0 by account | Data Engineering Lead |
| Project inventory vs Smartsheet | Weekly | 0 unmatched projects | PMO Portfolio Manager |
| Person/role vs Entra ID | Daily | 0 orphaned assignments | Security Architect |
| Enrollment metrics vs IR warehouse | Per term load | < 0.5% on headcount | Data Governance Lead |
| KPI values vs prior published package | Per reporting cycle | 0 undisclosed differences | Data Steward |

A reconciliation breach outside tolerance is a blocking exception (DQA-005) and
prevents snapshot certification for board reporting.

### DR-SYNC-001.6 — Ordering and dependency of runs

Ingestion order is fixed because conformance depends on dimensions being
current: Entra ID → Workday HCM (person) → Workday Financials → IR warehouse →
Banner-derived → Smartsheet → Salesforce → ServiceNow → Canvas. A failed
upstream dependency holds downstream runs rather than running them on stale
dimensions.

## Consequences

- Smartsheet remains the planning tool of record for dates; PMO process must
  route date changes there, not into the platform.
- Monthly close creates a hard reconciliation dependency on Finance's calendar;
  the reporting calendar (BRD-007) is built around it.
- The no-hard-delete rule grows storage; covered by the retention policy.

## Open items

- Banner access path (direct vs IR warehouse view) is unresolved; see proposal
  open question 2. The matrix assumes the IR warehouse path.
