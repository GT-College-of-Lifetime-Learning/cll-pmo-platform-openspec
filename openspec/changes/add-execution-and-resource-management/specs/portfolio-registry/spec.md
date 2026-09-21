# Delta for Portfolio Registry

## Purpose
The registry gains the execution-link fields sync needs, without changing its role as
the system of record.

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
- AND its synced fields are marked sync-enabled on the registry item