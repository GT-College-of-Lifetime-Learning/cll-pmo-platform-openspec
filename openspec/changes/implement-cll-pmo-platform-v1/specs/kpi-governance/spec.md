# Capability: kpi-governance — delta spec

Change: `implement-cll-pmo-platform-v1`
Requirements: KPI-001 – KPI-007 (7) · Acceptance criteria: 22

## ADDED Requirements

### Requirement: KPI-001 — KPI definition registry

The platform SHALL maintain a registry in which every KPI is defined as data —
name, business definition, formula, filter expression, unit, grain, cadence,
steward and version — and MUST NOT compute any reported KPI from logic that is
not registered.

Acceptance criteria:
- AC-KPI-001-1: Each KPI records name, plain-language definition, formula, filter expression, unit, grain, cadence, steward and version.
- AC-KPI-001-2: A KPI cannot be published without a named steward and an approved definition.
- AC-KPI-001-3: Any KPI rendered anywhere in the platform resolves to exactly one registry definition version.
- AC-KPI-001-4: Two views of the same KPI for the same period and scope return identical values.

#### Scenario: Same KPI in dashboard and board package
- **GIVEN** KPI `ENR-GROWTH` for FY2027-Q2 at college scope
- **WHEN** it is read from the executive dashboard and from the board package builder
- **THEN** both resolve the same definition version and return the same value

### Requirement: KPI-002 — Calculation lineage

The platform SHALL record, for every computed KPI value, the definition version,
input sources, contributing record counts, ingestion run ids and computation
timestamp, sufficient to reproduce the value.

Acceptance criteria:
- AC-KPI-002-1: Every `kpi_measurement` row stores definition version, contributing `run_id` values, input record counts and computation timestamp.
- AC-KPI-002-2: A user with appropriate role can trace any displayed KPI value to its contributing sources and runs.
- AC-KPI-002-3: Recomputing a value from its recorded lineage inputs reproduces the stored value exactly.

#### Scenario: Challenged KPI value
- **GIVEN** a pillar owner disputes a completion-rate value for FY2027-Q3
- **WHEN** a data steward opens the lineage for that measurement
- **THEN** the definition version, the Canvas and Banner run ids, and the contributing record counts are shown, and recomputation reproduces the same value

### Requirement: KPI-003 — Targets and thresholds

The platform SHALL store per-KPI targets and threshold bands with effective
dates, SHALL evaluate measured values against the bands in force for the
measurement period, and SHALL retain superseded targets.

Acceptance criteria:
- AC-KPI-003-1: Targets and thresholds carry effective-from and effective-to dates and may differ by period.
- AC-KPI-003-2: Status evaluation uses the bands in force for the measured period, not the current bands.
- AC-KPI-003-3: Superseded targets are retained and visible in history.

#### Scenario: Target raised for the new fiscal year
- **GIVEN** the FY2027 target is 8.0% and the FY2028 target is 10.0%
- **WHEN** an FY2027-Q4 measurement of 8.4% is evaluated
- **THEN** it is assessed against the 8.0% target and reported as on-target, regardless of the later FY2028 target

### Requirement: KPI-004 — Measurement cadence and snapshots

The platform SHALL compute each KPI on its registered cadence, SHALL write an
immutable measurement record per period and scope, and MUST NOT alter a
measurement for a closed period.

Acceptance criteria:
- AC-KPI-004-1: Measurements are produced on the registered cadence (monthly, quarterly or per term) for every in-scope combination.
- AC-KPI-004-2: A measurement for a closed period is immutable; corrections occur only through restatement.
- AC-KPI-004-3: A missing measurement is recorded as missing with a reason, rather than omitted silently.

#### Scenario: Late source data after period close
- **GIVEN** FY2027-Q2 is closed and additional Canvas data arrives for that quarter
- **WHEN** the KPI computation runs
- **THEN** the closed-period measurement is unchanged and a restatement candidate is raised for steward decision

### Requirement: KPI-005 — Ownership and stewardship

The platform SHALL assign every KPI a named steward accountable for its
definition, data quality and variance narrative, and SHALL prevent publication
of a KPI whose steward is inactive.

Acceptance criteria:
- AC-KPI-005-1: Every published KPI has exactly one accountable steward resolving to an active person.
- AC-KPI-005-2: A KPI whose steward becomes inactive is flagged and blocked from inclusion in a new board package until reassigned.
- AC-KPI-005-3: Steward changes are recorded with effective dates and retained.

#### Scenario: Steward leaves before the reporting cycle
- **GIVEN** the steward of 3 KPIs is offboarded two weeks before the quarterly cycle
- **WHEN** the package builder validates readiness
- **THEN** the 3 KPIs are blocked with a stewardship gap and the Data Governance Lead is notified

### Requirement: KPI-006 — Restatement and versioning

The platform SHALL version KPI definitions, SHALL require an explicit
restatement record when a change affects previously published values, and SHALL
disclose restatements wherever the affected periods are displayed.

Acceptance criteria:
- AC-KPI-006-1: A definition change creates a new version; prior versions remain readable and attached to their measurements.
- AC-KPI-006-2: A change affecting published periods requires a restatement record capturing reason, approver, affected periods and prior and new values.
- AC-KPI-006-3: Any view showing a restated period displays the restatement disclosure.

#### Scenario: Definition correction after publication
- **GIVEN** KPI `NC-COMPLETION` was published for FY2027-Q1 and its filter is found to exclude a valid program
- **WHEN** the steward publishes definition v2 and requests restatement
- **THEN** a restatement record captures prior 71.2% and corrected 73.8% with approver and reason, and every view of FY2027-Q1 shows the disclosure

### Requirement: KPI-007 — Variance narrative

The platform SHALL capture a written narrative for any KPI breaching its
threshold in a reporting period, attributed to the steward and dated, and SHALL
require the narrative before the period's board package can be approved.

Acceptance criteria:
- AC-KPI-007-1: A threshold breach creates a narrative requirement assigned to the KPI steward with a due date within the reporting calendar.
- AC-KPI-007-2: Narratives record author, timestamp, measured value, target and the periods covered.
- AC-KPI-007-3: Package approval is blocked while any required narrative is outstanding.

#### Scenario: Red KPI without explanation
- **GIVEN** 2 KPIs breached their lower threshold in FY2027-Q3 and one narrative is missing
- **WHEN** the PMO Director attempts to approve the board package
- **THEN** approval is blocked, naming the KPI and its steward, until the narrative is supplied
