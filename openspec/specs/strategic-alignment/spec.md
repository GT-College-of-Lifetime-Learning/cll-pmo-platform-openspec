# Strategic Alignment Specification

## Purpose
Connects registered work and KPIs to CLL's strategic priorities (Strategy 2035) so leadership
can see where effort goes and whether it moves the measures that matter.

## Requirements

### Requirement: Priorities managed as data
The system SHALL maintain strategic priorities as records with an identifier, title, description, executive owner, effective dates, and a Provisional flag, and SHALL retain retired priorities for history.

#### Scenario: Priority retired
- GIVEN a priority that leadership retires
- WHEN its end date is set
- THEN it is no longer offered for new alignment
- AND items already aligned to it keep that alignment in their history

#### Scenario: Provisional priorities are labeled
- GIVEN priorities seeded as Provisional
- WHEN they appear on any dashboard
- THEN each is labeled Provisional until the Dean's office confirms it

### Requirement: Strategic objectives
The system SHALL maintain objectives beneath each priority with their own identifiers, and SHALL let items and KPIs reference a primary objective that belongs to their primary priority.

#### Scenario: Item aligned to an objective
- GIVEN a project whose primary priority is SP-05
- WHEN its lead selects objective SO-5.3
- THEN the project appears under both SP-05 and SO-5.3 in the priority detail view

#### Scenario: Objective from a different priority
- GIVEN a project whose primary priority is SP-03
- WHEN someone selects SO-5.3 as its primary objective
- THEN the selection is rejected because SO-5.3 belongs to SP-05

### Requirement: Mandatory alignment
Every registered item SHALL be aligned to exactly one primary strategic priority or be categorized as Operational or Compliance with a written justification; secondary priorities MAY be added.

#### Scenario: Unaligned item flagged
- GIVEN an item with neither a primary priority nor a category
- WHEN dashboards refresh
- THEN the item appears on the Unaligned exception list for its unit and for governance

#### Scenario: Compliance work counted, not penalized
- GIVEN a project required to maintain regulatory compliance, such as SEVIS reporting changes
- WHEN it is categorized Compliance with a justification
- THEN it counts as aligned
- AND it is reported separately from strategic investment

### Requirement: KPI definitions
The system SHALL record each KPI with an identifier, definition, owner, unit of measure, desired direction, baseline, target, target date, reporting frequency, data source, and collection method.

#### Scenario: KPI without a baseline
- GIVEN a KPI with no baseline value
- WHEN it is displayed
- THEN it shows "Baseline pending" instead of progress toward target

### Requirement: KPI value capture
The system SHALL capture KPI values per reporting period with the period, value, and submitter, and SHALL flag values not received within 15 business days after the period ends.

#### Scenario: Manual KPI is late
- GIVEN a quarterly, manually reported KPI
- WHEN no value is recorded 15 business days after quarter end
- THEN the KPI owner is reminded
- AND the KPI shows as Late on dashboards

### Requirement: Cascading view without vendor hierarchies
The system SHALL show each priority with its KPIs and aligned items, filterable by unit, without depending on any vendor-specific scorecard hierarchy feature.

#### Scenario: Unit view of a priority
- GIVEN a priority with aligned items from four units
- WHEN a unit leader filters to their unit
- THEN only that unit's aligned items and unit-scoped KPIs are shown

### Requirement: Alignment coverage
The system SHALL report, per priority, the number of active aligned items, their status distribution, and their estimated effort, and SHALL report the share of total active effort that is Strategic, Operational, and Compliance.

#### Scenario: Priority with no active work
- GIVEN a priority with no active aligned items
- WHEN the Dean overview is viewed
- THEN the priority is highlighted as having no active work
