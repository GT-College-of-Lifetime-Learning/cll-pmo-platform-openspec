# Delta for Project Workspaces

## Purpose
Consistent places to collaborate and keep documents for approved work, linked from the
registry so anyone with access can find them.

## ADDED Requirements

### Requirement: Provisioning on approval
The system SHALL provision a collaboration space and document location from the standard template when a Tier 1 project is approved, and SHALL provision one for a Tier 2 project on request.

#### Scenario: Tier 1 approved
- GIVEN a Tier 1 project that has just been approved
- WHEN provisioning runs
- THEN a collaboration space and document location exist within one business day
- AND the lead and sponsor have access

### Requirement: Workspace linked in registry
The system SHALL store each workspace location on its registry item and display it on the item detail page.

#### Scenario: Finding project documents
- GIVEN an executive viewing a project's detail page
- WHEN they select the workspace link
- THEN they reach the project's document location

### Requirement: Standard templates
The system SHALL provide templates for project charter, risk and issue log, and closeout report, and SHALL require a charter link before a Tier 1 project becomes Active.

#### Scenario: Charter missing
- GIVEN a Tier 1 project with no charter link recorded
- WHEN its lead attempts to move it to Active
- THEN the change is blocked until a charter link is recorded

### Requirement: Closeout and retention
The system SHALL make a closed project's workspace read-only and retain it according to the institution's records retention schedule.

#### Scenario: Project closed
- GIVEN a project moved to Closed
- WHEN closeout completes
- THEN its workspace becomes read-only
- AND the applicable retention label is applied
