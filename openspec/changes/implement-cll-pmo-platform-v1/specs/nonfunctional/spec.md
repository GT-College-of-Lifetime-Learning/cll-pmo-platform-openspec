# Capability: nonfunctional — delta spec

Change: `implement-cll-pmo-platform-v1`
Requirements: NFR-001 – NFR-007 (7) · Acceptance criteria: 21

## ADDED Requirements

### Requirement: NFR-001 — Performance

The platform SHALL render the portfolio overview within 3.0 seconds at the 95th
percentile and 5.0 seconds at the 99th percentile with 150 concurrent users, and
SHALL return API reads within 800 milliseconds at the 95th percentile.

Acceptance criteria:
- AC-NFR-001-1: Under a 150-concurrent-user load test against production-scale data, overview first meaningful paint is p95 ≤ 3.0 s and p99 ≤ 5.0 s.
- AC-NFR-001-2: API read endpoints return p95 ≤ 800 ms and p99 ≤ 2.0 s under the same load.
- AC-NFR-001-3: Drill-down navigation between levels completes p95 ≤ 1.5 s.

#### Scenario: Board-week peak load
- **GIVEN** 150 concurrent users during board preparation week against 500 projects and 5 years of history
- **WHEN** the load profile runs for 30 minutes
- **THEN** p95 overview render stays at or below 3.0 s with no error rate above 0.1%

### Requirement: NFR-002 — Availability and recovery

The platform SHALL achieve 99.5% monthly availability during business hours
07:00–19:00 ET, with a recovery point objective of 4 hours and a recovery time
objective of 8 hours.

Acceptance criteria:
- AC-NFR-002-1: Monthly availability during business hours is at least 99.5%, measured by synthetic health checks at 1-minute intervals.
- AC-NFR-002-2: Backups support an RPO of 4 hours or better, verified by a restore test at least quarterly.
- AC-NFR-002-3: A documented recovery runbook restores service within 8 hours, demonstrated in an annual recovery exercise.

#### Scenario: Quarterly restore test
- **GIVEN** the scheduled quarterly restore exercise
- **WHEN** the team restores the platform into the recovery environment
- **THEN** data loss is no more than 4 hours, service is available within 8 hours, and the result is retained as evidence

### Requirement: NFR-003 — Scalability

The platform SHALL support at least 500 active projects, 250 registered KPIs,
5 years of monthly measurement history and 2,000 registered users without
breaching the performance targets in NFR-001.

Acceptance criteria:
- AC-NFR-003-1: Performance targets hold at 500 projects, 250 KPIs and 5 years of monthly history.
- AC-NFR-003-2: Ingestion completes within its SLA window at 150% of current expected daily volume.
- AC-NFR-003-3: Capacity headroom is reported monthly against these ceilings.

#### Scenario: Volume surge
- **GIVEN** a nightly financial load at 150% of expected volume (~67,500 rows)
- **WHEN** the run executes
- **THEN** it completes before the 03:30 ET SLA with no degradation of the morning dashboard

### Requirement: NFR-004 — Observability and alerting

The platform SHALL emit structured run records and application telemetry for
every ingestion run, computation and export, and SHALL alert a named on-call
owner on failure or SLA breach.

Acceptance criteria:
- AC-NFR-004-1: 100% of ingestion runs, KPI computations and exports emit a structured record with id, start, end, status and counts.
- AC-NFR-004-2: Failures and SLA breaches alert the registered on-call owner within 5 minutes.
- AC-NFR-004-3: Telemetry is queryable for at least 13 months to support trend analysis.

#### Scenario: Silent failure is impossible
- **GIVEN** an ingestion run that terminates without writing a completion record
- **WHEN** the watchdog evaluates runs past their expected completion window
- **THEN** it raises a missing-completion alert to the on-call owner within 5 minutes

### Requirement: NFR-005 — Accessibility conformance

The platform SHALL conform to WCAG 2.2 Level AA across all user-facing surfaces,
including exported PDF artifacts, and SHALL be validated by audit before each
major release.

Acceptance criteria:
- AC-NFR-005-1: An accessibility audit before each major release reports no unresolved Level A or AA defects.
- AC-NFR-005-2: Exported PDFs are tagged, have a reading order and include alternative text for figures.
- AC-NFR-005-3: Automated accessibility checks run in CI and fail the build on new Level A defects.

#### Scenario: New Level A defect introduced
- **GIVEN** a change that removes a form label
- **WHEN** the CI accessibility check runs on the pull request
- **THEN** the build fails naming the defect, and the change cannot merge

### Requirement: NFR-006 — Retention and archival

The platform SHALL retain certified snapshots, audit logs and governance
decisions for 7 years, landing-zone payloads for 400 days, and telemetry for
13 months, and SHALL purge only through the documented retention process.

Acceptance criteria:
- AC-NFR-006-1: Retention periods are enforced automatically per data class, with purge events logged.
- AC-NFR-006-2: No ad-hoc deletion path exists for snapshots, audit logs or governance decisions.
- AC-NFR-006-3: Data purged at end of retention is unrecoverable and the purge is recorded with class, volume and date.

#### Scenario: Landing payload ages out
- **GIVEN** landing payloads from 401 days ago
- **WHEN** the retention process runs
- **THEN** those payloads are purged, the purge is logged with class and volume, and related certified snapshots are untouched

### Requirement: NFR-007 — Maintainability and environment parity

The platform SHALL maintain development, test and production environments with
equivalent configuration and schema, SHALL deploy exclusively through automated
pipelines, and MUST NOT permit manual production changes outside the documented
emergency procedure.

Acceptance criteria:
- AC-NFR-007-1: All three environments share schema and configuration structure, differing only in documented, parameterised values.
- AC-NFR-007-2: Every production deployment is produced by the automated pipeline and is traceable to a commit and a release record.
- AC-NFR-007-3: Emergency manual changes require documented approval and a follow-up pipeline reconciliation within 5 business days.

#### Scenario: Emergency hotfix applied manually
- **GIVEN** an approved emergency change applied directly to production
- **WHEN** 5 business days elapse
- **THEN** the change must be present in source control and deployed via the pipeline, or it is flagged as unreconciled drift to the Release Manager
