# Delta for Execution Integration

## Purpose
Connect the registry to the tools where Tier 1 work actually executes, so the registry
reflects task-level reality without leads re-keying it, while the registry remains the
system of record.

## ADDED Requirements

### Requirement: Tier 1 standard execution tool
The system SHALL designate one standard execution tool for Tier 1 projects, SHALL record each Tier 1 item's plan link, and SHALL record any unit's continued use of its own tool for Tier 2 work without penalty.

#### Scenario: Tier 1 approved with the standard tool
- GIVEN a Tier 1 project approved for activation
- WHEN its workspace is provisioned
- THEN its plan is created in the standard execution tool and the link recorded on the registry item

#### Scenario: Unit tool remains valid for Tier 2
- GIVEN a unit that manages tasks in its own tool
- WHEN it registers a Tier 2 project
- THEN registration succeeds with the tool name and link recorded

### Requirement: One-way sync into the registry
The system SHALL sync milestones and percent complete from a Tier 1 item's execution plan into the registry, and SHALL NOT push registry fields back to the plan except on explicit command, and the registry SHALL remain the system of record for status reporting.

#### Scenario: Milestone completed in the plan
- GIVEN a Tier 1 item with a linked plan
- WHEN a milestone is marked complete in the plan
- THEN the registry's milestone record for that item updates within one business day
- AND the item's percent complete updates

#### Scenario: Registry remains authoritative
- GIVEN a synced item whose plan data and a lead-entered update disagree
- WHEN the status is reported
- THEN the registry's record with its as-of date is what dashboards show
- AND the disagreement is surfaced, not silently resolved

### Requirement: Sync failure honesty
The system SHALL detect when a plan's data has not synced within its expected window, SHALL mark the item's synced fields as stale on every surface where they appear, and SHALL NOT present unsynced values as current.

#### Scenario: Plan link broken
- GIVEN a Tier 1 item whose plan link no longer resolves
- WHEN the sync window passes
- THEN the item shows a sync-failed indicator with the last successful sync time
- AND its milestones and percent complete display the staleness, not just the values

### Requirement: Roadmap view for portfolio leads
The system SHALL provide a roadmap view of programs and portfolios ordered by timeline, reading registry data, and SHALL NOT require the portfolio tooling for any reporting that the dashboards provide.

#### Scenario: Portfolio lead reviews the roadmap
- GIVEN a portfolio with five programs across three units
- WHEN the portfolio lead opens the roadmap view
- THEN programs appear on a timeline with their current stages
- AND each opens to its registry detail

## MODIFIED Requirements

### Requirement: Execution tool independence
The system SHALL record the tool each project uses for day-to-day execution and a link to it, SHALL designate the standard execution tool for Tier 1 projects, and SHALL NOT require a specific execution tool for Tier 2 work.

#### Scenario: Unit keeps its existing tool
- GIVEN a unit that manages tasks in its own tool
- WHEN it registers a project
- THEN registration succeeds with the tool name and link recorded

#### Scenario: Tier 1 item uses the standard tool
- GIVEN a Tier 1 project being activated
- WHEN its execution link is recorded
- THEN the link points to its plan in the standard execution tool