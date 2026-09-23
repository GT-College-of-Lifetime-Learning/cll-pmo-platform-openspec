# Capability: integrations — delta spec

Change: `implement-cll-pmo-platform-v1`
Requirements: INT-001 – INT-011 (11) · Acceptance criteria: 35
Contracts: `contracts/integration-data-contracts.md` · Ownership: `decisions/synchronization-ownership.md`

## ADDED Requirements

### Requirement: INT-001 — Workday Financials ingestion

The platform SHALL ingest budget, actual and encumbrance amounts from Workday
Financials nightly under contract C-INT-001, re-reading a trailing 90-day window
so that retroactive postings are captured, and SHALL treat Workday as the sole
master for all financial amounts.

Acceptance criteria:
- AC-INT-001-1: A nightly run completes by 03:30 ET on at least 99% of business days and records `run_id`, `contract_version`, window bounds, record count, reject count and status.
- AC-INT-001-2: Each run re-reads the trailing 90 calendar days and updates amounts for prior periods that remain open.
- AC-INT-001-3: Monthly totals reconcile to the Workday ledger at $0 variance in total and by ledger account.
- AC-INT-001-4: Any attempt to write a financial amount from within the platform is rejected and logged as an ownership violation.

#### Scenario: Retroactive posting in an open period
- **GIVEN** period FY2027-P03 is open and a $12,400 accrual is posted in Workday with a `posted_at` 21 days in the past
- **WHEN** the nightly Workday Financials run executes
- **THEN** the trailing-window re-read captures the accrual, the project's actual amount increases by $12,400, and the freshness timestamp advances

#### Scenario: Ledger variance blocks certification
- **GIVEN** the monthly reconciliation shows a $340 variance against the ledger
- **WHEN** a data steward attempts to certify the monthly snapshot
- **THEN** certification is refused with the variance detail and a blocking exception is raised

### Requirement: INT-002 — Workday HCM position and effort ingestion

The platform SHALL ingest position, worker and effort-allocation records from
Workday HCM weekly under contract C-INT-002, and SHALL treat position-level rows
as restricted data visible only to the `portfolio-admin` and `data-steward`
roles.

Acceptance criteria:
- AC-INT-002-1: The weekly run completes by 05:00 ET Monday and validates that each position's allocations for a period sum to no more than 1.000 FTE.
- AC-INT-002-2: Position-level rows are readable only by `portfolio-admin` and `data-steward`; all other roles receive project-level aggregates.
- AC-INT-002-3: Project-level effort aggregates covering fewer than 5 positions are suppressed and rendered as suppressed, not as zero.
- AC-INT-002-4: Every read of position-level data writes an audit entry identifying actor, role set and target.

#### Scenario: Pillar owner views effort
- **GIVEN** a user holding only `pillar-owner` opens a project with 3 allocated positions
- **WHEN** the effort panel renders
- **THEN** the panel shows "suppressed (below minimum cell size)" rather than an FTE value, and no position-level row is transmitted

### Requirement: INT-003 — Banner enrollment ingestion

The platform SHALL ingest aggregate enrollment measures derived from Banner
nightly under contract C-INT-003, and SHALL NOT receive, store or process any
student-identifiable record.

Acceptance criteria:
- AC-INT-003-1: The nightly run loads program x term x level aggregates by 05:00 ET and performs a full reload at term census.
- AC-INT-003-2: Any payload containing a student identifier, name or other direct identifier fails the run and is not written to the landing zone.
- AC-INT-003-3: Headcount reconciles to the IR published census within 0.5% per term.

#### Scenario: Identifiable field appears in payload
- **GIVEN** the warehouse view is altered to include a `student_id` column
- **WHEN** the nightly enrollment run executes
- **THEN** the run fails closed before landing, no payload is persisted, and a blocking exception naming the offending field is raised

### Requirement: INT-004 — Salesforce partner pipeline ingestion

The platform SHALL ingest partner opportunity records from Salesforce twice
daily under contract C-INT-004 using incremental extraction on
`SystemModstamp`, and SHALL link opportunities to registry projects where
`linked_project_code__c` resolves.

Acceptance criteria:
- AC-INT-004-1: Runs at 06:00 and 18:00 ET complete within 30 minutes and extract only records modified since the prior high-water mark.
- AC-INT-004-2: An opportunity whose `stage` is outside the agreed stage set is quarantined with the rule id, not loaded.
- AC-INT-004-3: An opportunity referencing an unknown project code is loaded as unlinked and reported on the data quality scorecard.

#### Scenario: Unknown stage value
- **GIVEN** Salesforce introduces stage `Pilot Scoping` without notice
- **WHEN** the 18:00 ET run ingests an opportunity in that stage
- **THEN** the row is quarantined under the stage-domain rule and appears in the exception queue for steward triage

### Requirement: INT-005 — Smartsheet plan synchronization

The platform SHALL synchronize project plans from Smartsheet four times daily
plus on webhook events under contract C-INT-005, and SHALL write back only
`project_name`, `lifecycle_state`, `gate_flag` and `platform_status_summary`.

Acceptance criteria:
- AC-INT-005-1: Milestone names, dates and percent complete are accepted from Smartsheet and are not editable within the platform.
- AC-INT-005-2: A webhook-signalled change is reflected in the platform within 15 minutes.
- AC-INT-005-3: A write-back attempt to any field outside the permitted four is rejected and logged as an ownership violation.

#### Scenario: Milestone date changed in Smartsheet
- **GIVEN** a project manager moves a milestone end date from 2027-03-15 to 2027-04-02 in Smartsheet
- **WHEN** the webhook fires
- **THEN** the platform milestone reflects 2027-04-02 within 15 minutes and the change is recorded in registry history

### Requirement: INT-006 — ServiceNow demand and incident intake

The platform SHALL ingest demand requests and incidents from ServiceNow hourly
under contract C-INT-006 and SHALL associate them with registry projects where a
linked project code is present.

Acceptance criteria:
- AC-INT-006-1: At least 99% of hourly runs complete within 10 minutes of start.
- AC-INT-006-2: Records are extracted incrementally on `sys_updated_on` with no duplicate loading of unchanged records.
- AC-INT-006-3: A record whose `resolved_at` precedes `opened_at` is quarantined as a temporal-validity failure.

#### Scenario: Hourly run overlaps a prior run
- **GIVEN** the 14:00 run is still executing when 15:00 arrives
- **WHEN** the scheduler evaluates the 15:00 trigger
- **THEN** the new run is skipped with a logged reason rather than executing concurrently against the same high-water mark

### Requirement: INT-007 — Canvas engagement ingestion

The platform SHALL ingest weekly aggregate course engagement measures from
Canvas under contract C-INT-007 and SHALL NOT ingest learner-level records.

Acceptance criteria:
- AC-INT-007-1: The weekly export is ingested by 06:00 ET Sunday at course x week grain.
- AC-INT-007-2: Cells with fewer than 5 active learners are suppressed and are not stored as values.
- AC-INT-007-3: `completion_rate` outside 0–100 quarantines the row.

#### Scenario: Small-cohort course
- **GIVEN** a course week with 3 active learners
- **WHEN** the Canvas feed is ingested
- **THEN** the engagement values for that cell are stored as suppressed and any KPI consuming them excludes the cell while flagging reduced completeness

### Requirement: INT-008 — Institutional Research warehouse conformance

The platform SHALL source conformed dimensions (`unit`, `program`, `term`,
`funding_source`) from the Institutional Research warehouse nightly under
contract C-INT-008, and SHALL enforce referential integrity of all other feeds
against those dimensions.

Acceptance criteria:
- AC-INT-008-1: Dimension members load nightly by 04:30 ET with effective dating preserved.
- AC-INT-008-2: A record from any feed referencing a dimension code absent from the warehouse is quarantined as a referential-integrity failure.
- AC-INT-008-3: Dimension ingestion runs before all dependent feeds; a failure holds dependent runs rather than running them on stale dimensions.

#### Scenario: New cost center not yet in the warehouse
- **GIVEN** Workday delivers actuals for cost center `CLL-0142` that IR has not yet published
- **WHEN** conformance validation runs
- **THEN** the affected rows quarantine with a referential-integrity rule id, and the remainder of the financial load proceeds

### Requirement: INT-009 — Entra ID identity and group provisioning

The platform SHALL synchronize users and role-bearing group memberships from
Entra ID at least every 60 minutes under contract C-INT-009, and SHALL derive
all role assignments exclusively from group membership.

Acceptance criteria:
- AC-INT-009-1: A group membership change is reflected in the platform within 60 minutes and at next token refresh.
- AC-INT-009-2: A platform role assignment without a corresponding current group membership is revoked at the next sync and reported as an orphan.
- AC-INT-009-3: A disabled Entra ID account results in terminated platform sessions within 15 minutes.

#### Scenario: Staff member leaves the College
- **GIVEN** a `pillar-owner` account is disabled in Entra ID at 09:12
- **WHEN** the revocation check next evaluates their active session
- **THEN** the session is terminated by 09:27 and the role assignment is removed at the next sync

### Requirement: INT-010 — Scheduling, retry and backfill

The platform SHALL schedule all ingestion runs in the fixed dependency order
defined in DR-SYNC-001.6, SHALL retry transient failures with bounded backoff,
and SHALL support operator-initiated backfill over an arbitrary date window
without re-reading the source.

Acceptance criteria:
- AC-INT-010-1: Runs execute in the declared order; a failed upstream dependency holds downstream runs and records the hold reason.
- AC-INT-010-2: Transient failures retry up to 3 times with exponential backoff, after which the run fails and alerts the on-call owner.
- AC-INT-010-3: A backfill over any window within landing-zone retention replays from landing without contacting the source system, producing identical results to the original run for unchanged data.

#### Scenario: Source SFTP unavailable
- **GIVEN** the Workday SFTP endpoint refuses connections at 02:00 ET
- **WHEN** the nightly financial run starts
- **THEN** the run retries at 02:05, 02:15 and 02:35, then fails, alerts the Data Engineering on-call, and holds the dependent conformance run

### Requirement: INT-011 — Contract versioning and deprecation

The platform SHALL validate every payload against a versioned data contract,
SHALL stamp each ingested record with the `contract_version` that validated it,
and SHALL require 30 calendar days notice plus a dual-run window before a
breaking contract version is retired.

Acceptance criteria:
- AC-INT-011-1: Every landed record carries the `contract_version` used to validate it, and historical records retain the version in force at ingestion.
- AC-INT-011-2: An unannounced breaking change fails the run, raises a blocking exception, and freezes snapshot certification for affected measures.
- AC-INT-011-3: A planned MAJOR version change runs both versions in parallel for the notice window and is retired only after reconciliation shows equivalence.

#### Scenario: Source removes a contracted field
- **GIVEN** contract C-INT-004 v1.0.0 requires `probability` and Salesforce removes the field without notice
- **WHEN** the next run validates the payload
- **THEN** the run fails closed, no partial data is promoted, and pipeline KPIs dependent on the feed are marked uncertified until the contract is amended
