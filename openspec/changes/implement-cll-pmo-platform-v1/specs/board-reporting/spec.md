# Capability: board-reporting — delta spec

Change: `implement-cll-pmo-platform-v1`
Requirements: BRD-001 – BRD-007 (7) · Acceptance criteria: 21

## ADDED Requirements

### Requirement: BRD-001 — Quarterly board reporting package

The platform SHALL assemble a quarterly Strategy 2035 board package containing
portfolio health, KPI performance against target, financial position, milestone
status, top risks and approved narrative, built entirely from a single certified
snapshot.

Acceptance criteria:
- AC-BRD-001-1: The package contains all six required sections, each traceable to the snapshot from which it was built.
- AC-BRD-001-2: Every figure in the package resolves to the same `snapshot_id`; no section reads live data.
- AC-BRD-001-3: Package assembly is refused if the snapshot is uncertified or if any blocking data quality exception is open for a contributing measure.

#### Scenario: Assembly with an open blocking exception
- **GIVEN** a blocking reconciliation exception is open on financial actuals
- **WHEN** the analyst attempts to assemble the FY2027-Q3 package
- **THEN** assembly is refused, naming the exception and affected section, and no partial package is produced

### Requirement: BRD-002 — Narrative capture and approval

The platform SHALL capture written commentary per section and per exception KPI,
SHALL route it through the registered approval sequence, and MUST NOT publish a
package containing unapproved narrative.

Acceptance criteria:
- AC-BRD-002-1: Narrative records author, section, timestamp and the reporting period it covers.
- AC-BRD-002-2: Narrative requires approval by the PMO Director and, for KPI exception commentary, the KPI steward.
- AC-BRD-002-3: Publication is blocked while any narrative in the package is unapproved.

#### Scenario: Late edit after approval
- **GIVEN** approved narrative for the financial section
- **WHEN** an analyst edits the text after approval
- **THEN** the narrative returns to pending, the prior approved version is retained, and publication is blocked until re-approval

### Requirement: BRD-003 — Point-in-time snapshots

The platform SHALL create labelled, immutable snapshots of the portfolio model
for each reporting period, SHALL certify them through a data steward, and SHALL
retain them for 7 years so that any published figure can be reproduced.

Acceptance criteria:
- AC-BRD-003-1: A snapshot records `snapshot_id`, reporting period, creation timestamp, contributing run ids and certification status.
- AC-BRD-003-2: A certified snapshot is immutable; no process may alter its contents.
- AC-BRD-003-3: Any published figure can be re-derived from its snapshot and returns the identical value on re-derivation.

#### Scenario: Reproducing a figure a year later
- **GIVEN** the FY2027-Q2 package reported 12,840 active learners
- **WHEN** an analyst re-derives that figure from `snapshot_id` in October 2028
- **THEN** the value returned is exactly 12,840, regardless of subsequent source changes

### Requirement: BRD-004 — Board-ready exports

The platform SHALL export the approved package as PDF and PPTX for distribution
and as XLSX/CSV for supporting data, each stamped with reporting period,
snapshot id, generation timestamp and a content checksum.

Acceptance criteria:
- AC-BRD-004-1: PDF and PPTX exports reproduce the approved package content without manual editing.
- AC-BRD-004-2: Every export is stamped with reporting period, `snapshot_id`, generation timestamp and SHA-256 checksum.
- AC-BRD-004-3: Supporting data exports contain the underlying values for every figure shown in the package.

#### Scenario: Verifying a circulated file
- **GIVEN** a PDF circulated to the Board
- **WHEN** its checksum is compared against the recorded export checksum
- **THEN** a match confirms the file is the published artifact, and a mismatch identifies it as altered

### Requirement: BRD-005 — Distribution and access control

The platform SHALL distribute approved packages only to the registered
distribution list through the permissioned SharePoint library, and SHALL log
every publication and access event.

Acceptance criteria:
- AC-BRD-005-1: Publication occurs only after approval and only to the registered library, within 30 minutes of approval.
- AC-BRD-005-2: Distribution list membership is registered and reviewed each reporting cycle.
- AC-BRD-005-3: Publication and subsequent access events are written to the audit log with actor and timestamp.

#### Scenario: Unapproved publication attempt
- **GIVEN** a package whose narrative approval is pending
- **WHEN** a user attempts to publish it to the board library
- **THEN** the upload is refused because no approval record exists, and the attempt is logged

### Requirement: BRD-006 — Prior-period comparison and restatement disclosure

The platform SHALL present prior-period comparatives drawn from the snapshots as
originally published, and SHALL disclose any restatement affecting a comparative
figure with reason, approver and prior value.

Acceptance criteria:
- AC-BRD-006-1: Comparatives are read from the originally published snapshot, not recomputed from current data.
- AC-BRD-006-2: A restated comparative is displayed with both the originally published and restated values plus the restatement reason and approver.
- AC-BRD-006-3: A package containing an undisclosed difference from a prior published figure cannot be approved.

#### Scenario: Restated comparative in the package
- **GIVEN** FY2027-Q1 completion rate was published at 71.2% and restated to 73.8%
- **WHEN** the FY2027-Q2 package shows the Q1 comparative
- **THEN** both values appear with the restatement reason and approver attached

### Requirement: BRD-007 — Reporting calendar and readiness

The platform SHALL maintain a reporting calendar aligned to the Finance close
and Board meeting dates, and SHALL publish a readiness checklist showing
outstanding blockers ahead of each cycle.

Acceptance criteria:
- AC-BRD-007-1: The calendar records, per cycle, the close date, snapshot date, narrative due date, approval date and Board meeting date.
- AC-BRD-007-2: The readiness checklist shows every outstanding blocker — open exceptions, missing narrative, stewardship gaps, failed reconciliations — with owner.
- AC-BRD-007-3: Readiness status is available at least 10 business days before the Board meeting date.

#### Scenario: Readiness review ten days out
- **GIVEN** the Board meets 2027-11-12 and readiness is reviewed 2027-10-29
- **WHEN** the checklist is generated
- **THEN** it lists 2 missing narratives and 1 open reconciliation exception with named owners and due dates
