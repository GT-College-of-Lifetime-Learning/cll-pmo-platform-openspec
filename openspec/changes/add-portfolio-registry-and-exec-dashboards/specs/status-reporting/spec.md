# Delta for Status Reporting

## Purpose
A light, predictable status rhythm that gives leadership current, comparable information on
every active item without manual data calls.

## ADDED Requirements

### Requirement: Reporting cadence
The system SHALL expect one status update per monthly reporting period for every Active and On Hold item, and SHALL allow the TCC to set individual Tier 1 items to a biweekly cadence.

#### Scenario: Monthly period
- GIVEN an Active Tier 2 project
- WHEN the monthly period closes
- THEN exactly one status update is expected for that period

### Requirement: Standard status content
Each status update SHALL include overall status; status for schedule, scope, and resources; a progress summary; the next milestone and its forecast date; percent complete; and whether an executive decision or help is needed.

#### Scenario: Decision needed
- GIVEN a lead who needs a staffing decision
- WHEN they submit an update with Decision Needed selected
- THEN they must describe the ask
- AND the item appears on the Dean and governance Decisions Needed lists

### Requirement: Standard RAG definitions
The system SHALL apply published definitions — Green: on track; Amber: at risk, recovery within the lead's control; Red: off track or needs help beyond the lead's authority — and SHALL require a path to green or a decision ask with any Red status.

#### Scenario: Red without a path forward
- GIVEN a lead selecting Red overall status
- WHEN both path-to-green and decision ask are empty
- THEN the update is rejected with an explanation

### Requirement: Low-burden submission
The system SHALL let a lead submit an update from a link that pre-identifies the item, and a typical update SHOULD take no more than 15 minutes.

#### Scenario: Update from reminder link
- GIVEN a reminder for project CLL-26-0042
- WHEN the lead opens the link in the reminder
- THEN the update form is already associated with CLL-26-0042

### Requirement: Reminders and escalation
The system SHALL remind leads before an update is due, remind them again when it is overdue, and notify the unit head when an update is 5 business days overdue.

#### Scenario: Escalation to unit head
- GIVEN an update 5 business days past due
- WHEN the daily check runs
- THEN the lead's unit head receives a notice listing the overdue items

### Requirement: Status currency
The system SHALL label each active item's status Current, Due, or Stale — Stale meaning no update within the period plus 5 business days — and SHALL NOT present a stale status as current.

#### Scenario: Stale item on the Dean overview
- GIVEN a project last updated seven weeks ago
- WHEN the Dean overview is viewed
- THEN the project shows as Stale with its last update date

### Requirement: Status history
The system SHALL retain every submitted update as append-only history per item.

#### Scenario: Trend available
- GIVEN a project with six monthly updates
- WHEN its detail page is viewed
- THEN all six statuses appear in date order
