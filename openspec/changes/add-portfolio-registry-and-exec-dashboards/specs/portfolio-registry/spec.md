# Delta for Portfolio Registry

## Purpose
The system of record for all registered CLL work — strategic priorities, portfolios, programs,
and projects — with the minimum data leadership needs to see, compare, and steer it.

## ADDED Requirements

### Requirement: Portfolio hierarchy
The system SHALL organize registered work as Strategic Priority → Portfolio → Program → Project, where a project MAY belong directly to a portfolio without a program.

#### Scenario: Project without a program
- GIVEN a project registered under a portfolio with no parent program
- WHEN the portfolio is viewed
- THEN the project appears in the portfolio's totals

#### Scenario: Program summarizes its projects
- GIVEN a program with three child projects
- WHEN one child project's latest status is Red
- THEN the program summary shows one Red child project

### Requirement: Stable identifiers
The system SHALL assign each registered item a unique, human-readable identifier at creation and SHALL NOT change or reuse identifiers.

#### Scenario: Identifier assigned at registration
- GIVEN an approved intake request
- WHEN its project record is created
- THEN the project receives the next identifier in the form `CLL-<YY>-<NNNN>`
- AND that identifier appears on every dashboard and notification referencing the project

#### Scenario: Cancelled item keeps its identifier
- GIVEN a cancelled project
- WHEN later projects are registered
- THEN the cancelled project's identifier is never reassigned

### Requirement: Registration tiers
The system SHALL classify every registered project as Tier 1 (Strategic) or Tier 2 (Unit) using published threshold criteria, and SHALL NOT require registration of work below the Tier 2 threshold.

#### Scenario: Cross-unit work is Tier 1
- GIVEN a proposed project involving two or more CLL units
- WHEN it is classified
- THEN it is Tier 1 regardless of size

#### Scenario: Small operational work is not registered
- GIVEN work below the Tier 2 effort and duration thresholds
- WHEN a unit checks whether it must be registered
- THEN the published criteria identify it as operational work that is not registered

### Requirement: Required data before activation
The system SHALL prevent an item from entering the Active stage until its title, lead unit, lead, sponsor, tier, alignment, start date, and target end date are recorded.

#### Scenario: Missing sponsor blocks activation
- GIVEN an approved project with no sponsor recorded
- WHEN someone attempts to move it to Active
- THEN the change is rejected with a message naming the missing field

### Requirement: Lifecycle stages
The system SHALL track each item through the stages Proposed, Approved, Active, On Hold, Closing, Closed, and Cancelled, recording the date and actor of every stage change.

#### Scenario: Closing requires a closeout summary
- GIVEN an Active Tier 1 project
- WHEN its lead moves it to Closed
- THEN a closeout summary covering outcomes, KPI effect, and lessons learned is required
- AND the stage change is recorded with date and actor

### Requirement: Execution tool independence
The system SHALL record the tool each project uses for day-to-day execution and a link to it, and SHALL NOT require a specific execution tool.

#### Scenario: Unit keeps its existing tool
- GIVEN a unit that manages tasks in its own tool
- WHEN it registers a project
- THEN registration succeeds with the tool name and link recorded

### Requirement: Confidential items
The system SHALL allow an item to be marked Confidential, limiting its details to executive roles and the item's own unit, while still counting it in aggregate totals for all other viewers.

#### Scenario: Confidential item outside executive roles
- GIVEN a Confidential project led by Unit A
- WHEN a user without an executive role and not in Unit A views any dashboard
- THEN the project's title and details are not shown
- AND aggregate counts still include it as "Confidential"

#### Scenario: Own unit sees its Confidential item
- GIVEN a Confidential project led by Unit A
- WHEN a Unit A leader with a Unit role views dashboards
- THEN the project appears in full detail alongside Unit A's other items

#### Scenario: Masked aggregate counting
- GIVEN two Confidential projects aligned to priority SP-03
- WHEN a viewer without access to their details views the SP-03 health summary
- THEN the counts include both projects, shown as "+2 Confidential"
- AND no title, identifier, or drillable detail for either project is available

### Requirement: Backfill of in-flight work
The system SHALL support bulk registration of work already underway without routing it through intake, marking each such item as backfilled.

#### Scenario: Pilot unit loads existing projects
- GIVEN a pilot unit with in-flight projects listed in a spreadsheet
- WHEN the portfolio analyst imports them
- THEN each receives an identifier and is marked Backfilled

#### Scenario: Backfilled item still incomplete
- GIVEN a backfilled item missing required activation data
- WHEN 30 days have passed since import
- THEN the item is flagged on the unit's Action Needed list
