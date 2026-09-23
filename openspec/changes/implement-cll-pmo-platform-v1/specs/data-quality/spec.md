# Capability: data-quality — delta spec

Change: `implement-cll-pmo-platform-v1`
Requirements: DQA-001 – DQA-006 (6) · Acceptance criteria: 18

## ADDED Requirements

### Requirement: DQA-001 — Data quality rule catalog

The platform SHALL maintain a catalog of data quality rules, each with an
identifier, dimension (completeness, validity, consistency, timeliness,
uniqueness, referential integrity), severity (blocking or advisory), target
entity and owner.

Acceptance criteria:
- AC-DQA-001-1: Every rule records id, dimension, severity, target entity and field, expression and accountable owner.
- AC-DQA-001-2: Rules are versioned; a rule change records who changed it, when and why.
- AC-DQA-001-3: Every contracted feed has at least one blocking rule covering its key fields.

#### Scenario: New feed without rules
- **GIVEN** a new source contract is registered with no blocking rules defined
- **WHEN** the feed is promoted toward production
- **THEN** promotion is refused until at least one blocking rule covers its key fields

### Requirement: DQA-002 — Ingestion-time validation

The platform SHALL evaluate applicable rules at the boundary between the landing
and conformed zones, SHALL quarantine records failing a blocking rule, and MUST
NOT promote failing records into the portfolio model.

Acceptance criteria:
- AC-DQA-002-1: Every record entering the conformed zone is evaluated against all applicable rules, and results are recorded per run.
- AC-DQA-002-2: Records failing a blocking rule are quarantined with the rule id and the raw payload; advisory failures are promoted but flagged.
- AC-DQA-002-3: A run's outcome reports total evaluated, passed, quarantined and advisory-flagged counts.

#### Scenario: Batch with mixed failures
- **GIVEN** a Smartsheet run of 1,000 rows where 12 rows have an end date before the start date and 40 rows have a missing assignee
- **WHEN** validation executes
- **THEN** the 12 rows quarantine on the blocking temporal rule, the 40 promote with an advisory flag, and the run reports 1,000 evaluated / 948 clean / 12 quarantined / 40 flagged

### Requirement: DQA-003 — Reconciliation against source of record

The platform SHALL reconcile each material feed against its source of record on
the cadence and tolerance registered in DR-SYNC-001.5, and SHALL treat an
out-of-tolerance result as a blocking exception.

Acceptance criteria:
- AC-DQA-003-1: Reconciliations execute on their registered cadence and record variance in absolute and percentage terms.
- AC-DQA-003-2: A variance outside tolerance raises a blocking exception and prevents snapshot certification for affected measures.
- AC-DQA-003-3: Reconciliation results are retained as evidence for the reporting period.

#### Scenario: Monthly financial reconciliation passes
- **GIVEN** the monthly close reconciliation of platform actuals against the Workday ledger
- **WHEN** total and by-account variance is $0
- **THEN** the reconciliation passes, the result is retained as evidence, and snapshot certification for the period is permitted

### Requirement: DQA-004 — Data quality scorecard

The platform SHALL publish a scorecard per source and per entity showing pass
rate by quality dimension, quarantine volume and trend, with thresholds that
drive an overall trust state.

Acceptance criteria:
- AC-DQA-004-1: The scorecard reports pass rate by dimension per source per run and as a rolling 30-day trend.
- AC-DQA-004-2: A source falling below 98% blocking-rule pass rate over 7 days is marked degraded and surfaced on the dashboard freshness indicator.
- AC-DQA-004-3: Scorecard history is retained for at least 24 months.

#### Scenario: Degrading source
- **GIVEN** the ServiceNow feed's blocking pass rate falls to 96.4% over 7 days
- **WHEN** the scorecard recomputes
- **THEN** the source is marked degraded, the data steward is notified, and views consuming it show reduced completeness

### Requirement: DQA-005 — Exception triage and remediation

The platform SHALL route every blocking exception to a queue owned by a named
data steward, with severity, age and affected measures, and SHALL track it to
resolution.

Acceptance criteria:
- AC-DQA-005-1: Each exception records rule id, source, affected record count, affected measures, severity, owner and status.
- AC-DQA-005-2: Exceptions unresolved beyond their severity service level escalate to the Data Governance Lead.
- AC-DQA-005-3: Resolution records the remediation action taken and whether affected records were replayed.

#### Scenario: Referential integrity exception
- **GIVEN** 240 financial rows quarantined for an unknown cost center
- **WHEN** IR publishes the missing dimension member and the steward resolves the exception
- **THEN** the resolution records the action, the rows are replayed successfully, and the exception closes with a link to the replay run

### Requirement: DQA-006 — Quarantine and replay

The platform SHALL retain quarantined records with their raw payload and failure
context for the landing-zone retention period, and SHALL replay them after
remediation without re-reading the source system.

Acceptance criteria:
- AC-DQA-006-1: Quarantined records retain raw payload, rule id, run id and failure timestamp for the full landing retention period.
- AC-DQA-006-2: A replay reprocesses selected quarantined records through current rules and reports how many pass and how many remain quarantined.
- AC-DQA-006-3: Replay is idempotent: replaying the same records twice does not duplicate rows in the portfolio model.

#### Scenario: Double replay
- **GIVEN** 240 remediated records are replayed successfully
- **WHEN** an operator accidentally triggers the same replay again
- **THEN** no duplicate rows are created, the second run reports zero net changes, and both runs are recorded
