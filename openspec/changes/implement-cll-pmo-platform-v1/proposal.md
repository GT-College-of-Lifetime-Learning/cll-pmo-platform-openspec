# Proposal: implement-cll-pmo-platform-v1

**Change ID:** `implement-cll-pmo-platform-v1`
**Status:** Proposed (baseline approved for implementation)
**Created:** 2026-09-23
**Sponsor:** PMO Director, College of Lifetime Learning
**Change type:** Greenfield platform baseline (v1)

## Problem

The College of Lifetime Learning (CLL) committed to the Strategy 2035 portfolio
without a system of record for executing it. Today:

- Project status lives in individual Smartsheet plans, email threads and slide
  decks. There is no authoritative list of strategic projects, their owners, or
  their lifecycle state.
- KPI values are recomputed by hand each quarter. The same KPI is reported with
  different values in different decks because the definition, filter set and
  as-of date are not recorded anywhere.
- Stage-gate approvals happen in meetings. The decision, the approver and the
  evidence reviewed are not retained, so audit and board questions cannot be
  answered after the fact.
- Financial actuals are pulled from Workday manually, reconciled in spreadsheets
  and are stale by the time leadership sees them.
- Board reporting takes roughly three weeks of analyst effort per quarter and
  produces numbers that cannot be reproduced later because no point-in-time
  snapshot is kept.

The institutional risk is concrete: CLL cannot demonstrate, on demand and with
evidence, whether Strategy 2035 is on track.

## Solution

Stand up the **CLL Strategy 2035 PMO Platform**: a governed portfolio data
platform plus an executive experience, specified as 11 capabilities and
72 approved requirements, and implemented through 101 traceable tasks across
9 phases.

The platform delivers:

1. **Project Registry** (`project-registry`) — the authoritative record of every
   Strategy 2035 project: identity, lifecycle state, strategic alignment,
   ownership, milestones, RAID log, funding linkage and full change history.
2. **KPI Governance** (`kpi-governance`) — a registry of KPI definitions with
   calculation lineage, targets and thresholds, measurement cadence, named
   stewards, explicit restatement handling and variance narrative.
3. **Governance Workflow** (`governance-workflow`) — stage-gate approvals with
   codified approval sequences, delegation, change-request disposition,
   escalation SLAs, action item tracking and retained decision records.
4. **Integrations** (`integrations`) — contract-governed ingestion from eleven
   enterprise sources, with scheduling, retry, backfill and contract
   versioning.
5. **Security** (`security`) — Entra ID SSO, RBAC, row-level scoping,
   encryption, audit logging, secrets management and access recertification.
6. **Data Quality** (`data-quality`) — a rule catalog, ingestion-time checks,
   reconciliation to source of record, a scorecard, exception triage and a
   quarantine/replay path.
7. **Executive Dashboard** (`executive-dashboard`) — portfolio health, KPI
   trends, pillar-to-project drill-down, risk heat map, financial burn,
   milestone timeline, freshness indicator and accessible presentation.
8. **Board Reporting** (`board-reporting`) — a reproducible quarterly package
   built from point-in-time snapshots, with approved narrative, controlled
   distribution and disclosed restatements.
9. **Nonfunctional** (`nonfunctional`) — performance, availability, scalability,
   observability, accessibility, retention and maintainability targets.
10. **Verification** (`verification`) — the test strategy, evidence traceability
    and UAT sign-off model.
11. **Release Governance** (`release-governance`) — nine release gates with
    explicit entry criteria, approvers, deployment and rollback rules.

## Scope

### In scope

- All 72 requirements listed in `specs/` for the eleven capabilities above.
- The eleven source integrations catalogued in `registries/source-catalog.md`
  and contracted in `contracts/integration-data-contracts.md`.
- The Strategy 2035 portfolio only (strategic projects), not departmental or
  operational work intake.
- Read-mostly integration: the platform is a consumer of enterprise systems and
  writes back only to Smartsheet status fields (see
  `decisions/synchronization-ownership.md`).

### Out of scope for v1

- Resource capacity planning and time entry (deferred to v2).
- Grant and sponsored-research administration (owned by GTRC systems).
- Replacing Smartsheet as the project planning tool; the platform consumes plans
  rather than replacing them.
- Public-facing external dashboards.
- Predictive/AI forecasting of portfolio outcomes (explicitly deferred; v1
  reports measured values only).

## Affected capabilities

| Capability (spec directory) | Requirements | Acceptance criteria |
|---|---|---|
| `integrations` | INT-001 – INT-011 | 35 |
| `security` | SEC-001 – SEC-007 | 22 |
| `executive-dashboard` | EXD-001 – EXD-008 | 25 |
| `project-registry` | PRJ-001 – PRJ-008 | 25 |
| `kpi-governance` | KPI-001 – KPI-007 | 22 |
| `governance-workflow` | GOV-001 – GOV-006 | 19 |
| `data-quality` | DQA-001 – DQA-006 | 18 |
| `board-reporting` | BRD-001 – BRD-007 | 21 |
| `nonfunctional` | NFR-001 – NFR-007 | 21 |
| `verification` | VER-001 – VER-003 | 9 |
| `release-governance` | REL-001 – REL-002 | 6 |
| **Total** | **72** | **223** |

All eleven capabilities are **ADDED** by this change; nothing is modified,
removed or renamed, because this is the v1 baseline.

## Delivery shape

101 tasks across 9 phases, each phase closed by a release gate:

| Phase | File | Tasks | Gate |
|---|---|---|---|
| 00 Foundation | `tasks/phase-00-foundation.md` | T-001 – T-008 (8) | GATE-0 |
| 01 Source Alignment | `tasks/phase-01-source-alignment.md` | T-009 – T-017 (9) | GATE-1 |
| 02 Core Platform | `tasks/phase-02-core-platform.md` | T-018 – T-031 (14) | GATE-2 |
| 03 Security & Quality | `tasks/phase-03-security-quality.md` | T-032 – T-043 (12) | GATE-3 |
| 04 Dashboard | `tasks/phase-04-dashboard.md` | T-044 – T-055 (12) | GATE-4 |
| 05 Governance | `tasks/phase-05-governance.md` | T-056 – T-066 (11) | GATE-5 |
| 06 Integrations | `tasks/phase-06-integrations.md` | T-067 – T-080 (14) | GATE-6 |
| 07 Reporting & Operations | `tasks/phase-07-reporting-operations.md` | T-081 – T-091 (11) | GATE-7 |
| 08 Verification & Release | `tasks/phase-08-verification-release.md` | T-092 – T-101 (10) | GATE-8 |

## Impact

- **Users:** PMO staff move off spreadsheets; pillar owners self-serve status;
  the Board receives a reproducible package.
- **Data:** a new governed portfolio data model becomes the reporting source of
  truth; source systems remain systems of record for their own domains.
- **Security:** new institutional data flows require the decisions recorded in
  `decisions/security-and-identity.md` before GATE-3 can close.
- **Operations:** a new production service with availability, observability and
  recovery obligations (NFR-002, NFR-004).
- **Effort:** estimated 3 quarters of delivery with the ownership model in
  `registries/ownership.md`.

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Source contracts change without notice | Broken ingestion, stale board numbers | INT-011 contract versioning + deprecation notice period; DQA-003 reconciliation |
| KPI definitions contested by pillar owners | Reporting stalls | KPI-001/KPI-005 force definition + steward sign-off before GATE-5 |
| Institutional data exposure | Severe | SEC-001 – SEC-007, security decision record, GATE-3 blocks progress |
| Smartsheet write-back conflicts | Data loss in planning tool | Field-level ownership matrix in `decisions/synchronization-ownership.md` |
| Board deadline pressure forces gate skipping | Unverifiable reporting | REL-001 gate criteria are approval-bound; no conditional gate closure without a logged waiver |

## Open questions

1. Does the Board require restated prior-period figures in the package itself,
   or as an appendix? (Affects BRD-006 presentation; not the data model.)
2. Is Banner enrollment available as a warehouse view, or must the platform read
   Banner directly? (Affects INT-003 and INT-008 sequencing.)

## Success criteria

- All 72 requirements verified against their 223 acceptance criteria with
  evidence recorded in `registries/evidence-catalog.md`.
- GATE-0 through GATE-8 closed with named approvers.
- One full quarterly board package produced from the platform, reproducible
  from a snapshot after the fact (BRD-003).
- Board package analyst effort reduced from ~3 weeks to under 3 days.
