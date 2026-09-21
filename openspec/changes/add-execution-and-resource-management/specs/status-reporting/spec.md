# Delta for Status Reporting

## Purpose
Synced Tier 1 items stop re-keying what the execution tool already knows: their monthly
updates become confirm-or-edit drafts, and the cadence requirement recognizes the
sync-backed path.

## MODIFIED Requirements

### Requirement: Reporting cadence
The system SHALL expect one status update per monthly reporting period for every Active and On Hold item, and SHALL allow the TCC to set individual Tier 1 items to a biweekly cadence, and SHALL count a confirmed auto-populated draft as the period's update for a synced item.

#### Scenario: Monthly period
- GIVEN an Active Tier 2 project
- WHEN the monthly period closes
- THEN exactly one status update is expected for that period

#### Scenario: Synced item confirms a draft
- GIVEN a Tier 1 item with live sync
- WHEN its auto-populated draft for the period is confirmed by its lead
- THEN the confirmation is recorded as the period's update with the sync as its source

### Requirement: Standard status content
Each status update SHALL include overall status; status for schedule, scope, and resources; a progress summary; the next milestone and its forecast date; percent complete; and whether an executive decision or help is needed, and for a synced item the milestone, forecast, and percent-complete fields SHALL arrive pre-populated from the plan with the lead able to edit before confirming.

#### Scenario: Decision needed
- GIVEN a lead who needs a staffing decision
- WHEN they submit an update with Decision Needed selected
- THEN they must describe the ask
- AND the item appears on the Dean and governance Decisions Needed lists

#### Scenario: Pre-populated fields from the plan
- GIVEN a synced Tier 1 item with percent complete at 62 in its plan
- WHEN its lead opens the period's update draft
- THEN percent complete arrives pre-populated at 62 with its sync source named
- AND the lead can edit any field before confirming