# Finding Tracker Specification

## Purpose
Problems that recur are the ones that matter: the system counts findings across periods
and escalates by occurrence, so chronic staleness or unresolved Reds surface to governance
instead of repeating as one-shot notices.

## Requirements

### Requirement: Finding records
The system SHALL record findings typed by problem class (stale update, red without resolution, unaligned item, triage overdue, decision overdue), each with the affected unit or item, severity, first-seen and last-seen dates, and an occurrence count, and SHALL NOT delete findings; resolution appends a record.

#### Scenario: First occurrence recorded
- GIVEN a unit's item with no update this period
- WHEN the daily hygiene check runs
- THEN a finding of type stale-update is recorded for that unit with occurrence count 1

#### Scenario: Resolution appended, not deleted
- GIVEN a recurring stale-update finding
- WHEN the unit submits the missing update
- THEN a resolution record is appended naming the resolver and date
- AND the original finding history remains visible

### Requirement: Escalation ladder
The system SHALL escalate a finding as its occurrence count grows: at 2 occurrences it SHALL flag the finding Recurring on the affected unit's view; at 3 occurrences it SHALL surface the finding on the governance view as needing decision; at 4 occurrences it SHALL block the affected item from moving to Closed until the finding is resolved.

#### Scenario: Recurring flag
- GIVEN a stale-update finding seen in two consecutive cycles
- WHEN the unit leader opens the unit view
- THEN the item appears with a Recurring marker

#### Scenario: Escalation to governance
- GIVEN the same stale-update finding seen in three consecutive cycles
- WHEN the governance view is opened
- THEN the finding appears in the items-needing-attention list with its occurrence history

#### Scenario: Closeout blocked
- GIVEN a finding with 4 occurrences whose affected item is otherwise ready to close
- WHEN its lead attempts to move it to Closed
- THEN the change is rejected with a message naming the unresolved finding

#### Scenario: Counter resets after resolution
- GIVEN a finding resolved and closed by the ladder
- WHEN the same problem recurs later
- THEN a new finding record starts at occurrence count 1

### Requirement: Findings respect access rules
Finding details SHALL follow the same role-based access rules as the items they concern, and SHALL NOT expose Confidential item details to viewers who could not see the item.

#### Scenario: Confidential item's finding
- GIVEN a Confidential item generating a stale-update finding
- WHEN a leader from another unit views findings
- THEN the finding's affected item is masked, counted only in aggregate
