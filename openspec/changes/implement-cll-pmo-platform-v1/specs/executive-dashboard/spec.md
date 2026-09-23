# Capability: executive-dashboard — delta spec

Change: `implement-cll-pmo-platform-v1`
Requirements: EXD-001 – EXD-008 (8) · Acceptance criteria: 25

## ADDED Requirements

### Requirement: EXD-001 — Strategy 2035 portfolio health overview

The platform SHALL present a single overview showing health for every Strategy
2035 pillar, aggregating project status, schedule variance, financial variance
and open high-severity risks, scoped to the viewer's permitted projects.

Acceptance criteria:
- AC-EXD-001-1: The overview renders every pillar in the current Strategy 2035 taxonomy with a health indicator derived from published, documented rules.
- AC-EXD-001-2: Health indicators are computed only from projects within the viewer's scope, and the project count shown matches that scope.
- AC-EXD-001-3: Each indicator exposes the contributing measures on demand, so no indicator is an unexplained colour.
- AC-EXD-001-4: Pillars with no in-scope projects render as "no data in scope" rather than as healthy.

#### Scenario: Pillar owner opens the overview
- **GIVEN** a `pillar-owner` who owns 2 of 6 pillars
- **WHEN** they open the portfolio overview
- **THEN** their 2 pillars show computed health from their projects and the other 4 render as "no data in scope"

### Requirement: EXD-002 — KPI trend visualization

The platform SHALL display each KPI as a time series against its target and
threshold bands, labelled with the KPI definition version and measurement
cadence in force for each point.

Acceptance criteria:
- AC-EXD-002-1: Every KPI chart shows measured values, the target line and threshold bands over at least 8 prior measurement periods where data exists.
- AC-EXD-002-2: Points measured under a superseded definition version are visually distinguished and labelled with that version.
- AC-EXD-002-3: A KPI with no measurement for a period renders a gap, never an interpolated value.

#### Scenario: Definition changed mid-series
- **GIVEN** KPI `ENR-GROWTH` moved from definition v1 to v2 in FY2027-Q2
- **WHEN** a viewer opens its trend chart
- **THEN** pre-Q2 points are marked as v1 with a visible boundary at the version change, and the chart does not imply a continuous like-for-like series

### Requirement: EXD-003 — Pillar-to-project drill-down

The platform SHALL allow a viewer to navigate from a pillar indicator to the
objectives, then to the contributing projects, then to a single project record,
preserving filter context and applying row-level scoping at every level.

Acceptance criteria:
- AC-EXD-003-1: Each drill-down level preserves the active period and filter context from the level above.
- AC-EXD-003-2: Row-level scoping is applied at every level; a viewer never reaches a record outside their scope by drilling.
- AC-EXD-003-3: Any drill-down view is addressable by URL and reproduces the same state for a viewer with equivalent scope.

#### Scenario: Drill from pillar to project
- **GIVEN** a viewer filtered to FY2027-Q2 on the Workforce pillar
- **WHEN** they drill through an objective into a project
- **THEN** the project view opens with FY2027-Q2 still applied and the URL reproduces that exact state

### Requirement: EXD-004 — Risk and issue heat map

The platform SHALL present open risks and issues from the RAID log as a
probability-by-impact heat map, filterable by pillar, project and owner, with
navigation to the underlying items.

Acceptance criteria:
- AC-EXD-004-1: The heat map plots open risks and issues by their recorded probability and impact ratings.
- AC-EXD-004-2: Selecting a cell lists the contributing items with owner, age in days and next review date.
- AC-EXD-004-3: Items closed within the selected period are excluded from the map but remain reachable through a closed-items view.

#### Scenario: Escalation candidate
- **GIVEN** three high-probability, high-impact risks are open across two pillars
- **WHEN** the PMO Director selects the top-right cell
- **THEN** all three items are listed with owner and age, and each links to its RAID record and escalation history

### Requirement: EXD-005 — Financial burn and variance view

The platform SHALL present budget, actual, encumbrance and variance by project
and pillar for the selected period, sourced exclusively from Workday Financials,
and SHALL render suppressed effort values explicitly.

Acceptance criteria:
- AC-EXD-005-1: Budget, actual, encumbrance and variance (absolute and percentage) are shown for the selected period and fiscal year to date.
- AC-EXD-005-2: Displayed amounts equal the reconciled Workday values for closed periods with no platform-side adjustment.
- AC-EXD-005-3: Effort figures suppressed under the minimum cell size render as "suppressed", never as zero or blank.

#### Scenario: Closed period is immutable
- **GIVEN** FY2027-P02 is closed and was reported at $1,284,300 actual
- **WHEN** Workday later restates that period
- **THEN** the closed-period figure still displays $1,284,300 and a restatement notice links to the disclosure

### Requirement: EXD-006 — Milestone timeline view

The platform SHALL present milestones on a timeline by project and pillar,
distinguishing gate milestones, showing baseline versus current dates, and
flagging milestones overdue relative to the current date.

Acceptance criteria:
- AC-EXD-006-1: Gate milestones are visually distinguished from ordinary milestones.
- AC-EXD-006-2: Baseline and current dates are both shown where they differ, with the slip in days.
- AC-EXD-006-3: Milestones past their current end date and not complete are flagged as overdue.

#### Scenario: Slipped gate milestone
- **GIVEN** a gate milestone baselined at 2027-03-15 now scheduled for 2027-04-02 and incomplete on 2027-04-10
- **WHEN** the timeline renders
- **THEN** it shows an 18-day slip against baseline and flags the milestone as overdue

### Requirement: EXD-007 — Data freshness and completeness indicator

The platform SHALL display, on every dashboard view, the effective as-of
timestamp of the data shown and a completeness state reflecting failed,
held or quarantined upstream data.

Acceptance criteria:
- AC-EXD-007-1: Every view shows the as-of timestamp of the oldest contributing feed, not the newest.
- AC-EXD-007-2: When a contributing feed has failed or is held, the view shows a degraded-completeness state naming the affected source.
- AC-EXD-007-3: When quarantined records materially affect a displayed aggregate, the aggregate carries a completeness flag.

#### Scenario: Financial feed failed overnight
- **GIVEN** the Workday Financials run failed and the last success was 38 hours ago
- **WHEN** a viewer opens the financial burn view
- **THEN** the as-of timestamp reflects the 38-hour-old load and a degraded-completeness banner names Workday Financials

### Requirement: EXD-008 — Accessible and responsive presentation

The platform SHALL meet WCAG 2.2 Level AA for all dashboard views, SHALL be
operable by keyboard alone, and MUST NOT convey status by colour alone.

Acceptance criteria:
- AC-EXD-008-1: All dashboard views pass a WCAG 2.2 AA audit with no unresolved Level A or AA defects.
- AC-EXD-008-2: Every interactive element, including charts and drill-downs, is reachable and operable by keyboard with a visible focus indicator.
- AC-EXD-008-3: Status is conveyed by text or shape in addition to colour, and charts expose an accessible data table equivalent.

#### Scenario: Screen reader on the portfolio overview
- **GIVEN** a viewer using a screen reader
- **WHEN** they navigate the portfolio overview
- **THEN** each pillar indicator announces its health state as text, and each chart offers a navigable table equivalent of its data
