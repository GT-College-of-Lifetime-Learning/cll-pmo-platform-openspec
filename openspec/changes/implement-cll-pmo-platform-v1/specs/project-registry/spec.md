# Capability: project-registry — delta spec

Change: `implement-cll-pmo-platform-v1`
Requirements: PRJ-001 – PRJ-008 (8) · Acceptance criteria: 25

## ADDED Requirements

### Requirement: PRJ-001 — Authoritative project record

The platform SHALL maintain exactly one authoritative record per Strategy 2035
project, identified by a platform-generated immutable `project_id`, and SHALL be
the system of record for project identity, name, description, lifecycle state
and strategic alignment.

Acceptance criteria:
- AC-PRJ-001-1: Creating a project issues an immutable `project_id` that is never reused or reassigned.
- AC-PRJ-001-2: A project record requires name, pillar, objective, owner, lifecycle state and funding source before it may leave `proposed`.
- AC-PRJ-001-3: Duplicate detection warns on creation when name or Smartsheet sheet id matches an existing active project.
- AC-PRJ-001-4: A rename in a downstream system is reverted on next synchronization and logged as an ownership violation.

#### Scenario: Duplicate project creation attempt
- **GIVEN** an active project "Lifetime Learning Credential Platform" exists
- **WHEN** a PMO staff member creates a project with the same name
- **THEN** the platform warns with the existing `project_id` and requires explicit confirmation before creating a second record

### Requirement: PRJ-002 — Project lifecycle states

The platform SHALL enforce the lifecycle `proposed → approved → active →
on-hold → closing → closed`, with `cancelled` reachable from any pre-closed
state, and MUST NOT permit undefined transitions.

Acceptance criteria:
- AC-PRJ-002-1: Only defined transitions are accepted; an undefined transition is rejected with the permitted set.
- AC-PRJ-002-2: Entering `approved` requires a recorded gate decision; entering `closed` requires a closure record with final actuals.
- AC-PRJ-002-3: Every transition records actor, timestamp, prior state, new state and reason.

#### Scenario: Skipping approval
- **GIVEN** a project in `proposed` with no gate decision
- **WHEN** a user attempts to move it directly to `active`
- **THEN** the transition is rejected, naming the missing gate decision, and the project remains `proposed`

### Requirement: PRJ-003 — Strategic alignment mapping

The platform SHALL map every project to exactly one Strategy 2035 pillar and at
least one objective, using the taxonomy owned by the Strategy Office, and SHALL
preserve alignment history when the taxonomy changes.

Acceptance criteria:
- AC-PRJ-003-1: Each project carries exactly one pillar and one or more objectives, validated against the current taxonomy.
- AC-PRJ-003-2: A taxonomy change preserves prior alignment with effective dates so historical reporting remains correct.
- AC-PRJ-003-3: Projects whose objectives are retired are flagged for realignment and listed for the Strategy Office.

#### Scenario: Objective retired mid-year
- **GIVEN** objective `WF-2.3` is retired effective 2027-07-01 with 4 projects aligned to it
- **WHEN** the taxonomy update is applied
- **THEN** the 4 projects retain `WF-2.3` for periods before that date, are flagged for realignment, and prior-period reports still resolve the objective

### Requirement: PRJ-004 — Ownership and RACI

The platform SHALL record for each project an accountable owner, a responsible
manager and consulted/informed parties, validated against current Workday HCM
persons, and SHALL prevent a project from remaining active without an
accountable owner.

Acceptance criteria:
- AC-PRJ-004-1: Owner and manager must resolve to active persons; terminated persons cannot be assigned.
- AC-PRJ-004-2: An active project whose owner becomes inactive raises an ownership-gap exception within one business day.
- AC-PRJ-004-3: Ownership changes are recorded with effective dates and retained in history.

#### Scenario: Owner departs
- **GIVEN** the accountable owner of an active project is terminated in Workday HCM
- **WHEN** the weekly HCM sync completes
- **THEN** an ownership-gap exception is raised to the PMO Portfolio Manager within one business day and the project is flagged on the overview

### Requirement: PRJ-005 — Milestone and deliverable tracking

The platform SHALL mirror milestones from Smartsheet, SHALL record a baseline
date set at approval, and SHALL compute slip against baseline without permitting
in-platform editing of source-owned milestone fields.

Acceptance criteria:
- AC-PRJ-005-1: Milestone name, dates and percent complete are read-only in the platform and sourced from Smartsheet.
- AC-PRJ-005-2: A baseline is captured at the approval gate and is immutable thereafter except by a recorded re-baseline decision.
- AC-PRJ-005-3: Slip in days is computed as current end date minus baseline end date and is available per milestone and per project.

#### Scenario: Re-baseline after approved change request
- **GIVEN** an approved change request authorising a new baseline
- **WHEN** the PMO applies the re-baseline
- **THEN** the prior baseline is retained in history, the new baseline takes effect from the decision date, and slip is computed against the new baseline going forward

### Requirement: PRJ-006 — RAID log

The platform SHALL maintain a risk, issue, decision and dependency log per
project, with severity, probability, impact, owner, due date and status, and
SHALL be the system of record for those items.

Acceptance criteria:
- AC-PRJ-006-1: Each RAID item records type, description, owner, status, and for risks a probability and impact rating on the published scale.
- AC-PRJ-006-2: Items overdue for review are flagged and surfaced to the item owner and the project manager.
- AC-PRJ-006-3: Closed items are retained with closure date and rationale, never deleted.

#### Scenario: Overdue risk review
- **GIVEN** a high-severity risk whose next review date passed 6 days ago
- **WHEN** the daily review check runs
- **THEN** the item is flagged overdue, the owner and project manager are notified, and it appears in the governance escalation queue

### Requirement: PRJ-007 — Funding linkage

The platform SHALL link each project to one or more funding sources and Workday
worktags, so that financial actuals resolve to projects, and SHALL report
unallocated spend that cannot be attributed to any project.

Acceptance criteria:
- AC-PRJ-007-1: Each project records at least one funding source and, where applicable, its Workday finance worktag.
- AC-PRJ-007-2: Financial rows whose worktag resolves to a project are attributed to it; rows with no resolvable worktag are reported as unallocated.
- AC-PRJ-007-3: Total attributed plus unallocated spend equals the total ingested spend for the period.

#### Scenario: Spend without a project worktag
- **GIVEN** $86,500 of Strategy 2035 cost-center spend arrives with a null `worktag_project`
- **WHEN** attribution runs
- **THEN** the amount appears in the unallocated bucket, is visible to the PMO, and the attributed-plus-unallocated total matches the ingested total exactly

### Requirement: PRJ-008 — Registry change history and audit trail

The platform SHALL retain a complete, queryable history of every change to a
project record, including field-level before and after values, actor, timestamp
and source, and MUST NOT permit history to be edited or deleted.

Acceptance criteria:
- AC-PRJ-008-1: Every field change records before value, after value, actor, timestamp (UTC) and originating source system or user interface.
- AC-PRJ-008-2: History is queryable to reconstruct the full state of any project as of any past date.
- AC-PRJ-008-3: No role, including `portfolio-admin`, can amend or delete a history entry.

#### Scenario: Reconstructing a project as of a board date
- **GIVEN** a Board question about a project's state on 2027-06-30
- **WHEN** a PMO analyst requests the record as of that date
- **THEN** the platform returns the field values in force on 2027-06-30 with the changes that produced them
