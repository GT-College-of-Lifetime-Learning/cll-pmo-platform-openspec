# Delta for Strategy Success Dashboard

## Purpose
The top-level Strategy 2035 view the Dean asked for: how far CLL is through the 2026–2035
window and whether each goal is on pace, on one screen, with a path down to the work behind it.

## ADDED Requirements

### Requirement: Strategy timeline
The system SHALL display the strategy window (Jan 1, 2026 – Dec 31, 2035), time elapsed and remaining as percentages, calendar days remaining, business days remaining, the target year, the as-of date, and an expected-progress-by-today marker, recalculated at every refresh.

#### Scenario: Mid-August 2026
- GIVEN an as-of date of Aug 16, 2026
- WHEN the timeline is displayed
- THEN it shows 6.2% elapsed, 93.8% remaining, and 3,425 calendar days remaining

#### Scenario: Institute holidays excluded from business days
- GIVEN an Institute holiday that falls on a weekday
- WHEN business days remaining are calculated
- THEN that day is not counted

### Requirement: One card per goal
The system SHALL show one card for each strategic goal, in goal order, with the goal number and short name in text, its headline KPI value, the target, and progress toward target, and SHALL show all goals even when a goal has no data.

#### Scenario: Goal with a live headline KPI
- GIVEN Goal 2 with 18 hubs recorded against a target of 200
- WHEN the page loads
- THEN the Goal 2 card reads "Global Learning Hubs" with 18 of 200 and a progress bar at 9%

#### Scenario: Goal with no data
- GIVEN Goal 3 whose headline KPI has no definition yet
- WHEN the page loads
- THEN the Goal 3 card still appears, showing "Definition pending"

### Requirement: Pace indicator
The system SHALL show, for each headline KPI, the actual value against the expected value for the as-of date and a pace status of On pace, Behind, Well behind, or Not yet measurable, and SHALL label the pace "Linear pace (unapproved)" when no approved trajectory exists.

#### Scenario: Behind an approved trajectory
- GIVEN an approved trajectory expecting 30 hubs by the as-of date and 24 recorded
- WHEN the Goal 2 card is displayed
- THEN its pace status is Behind (80% of expected)

#### Scenario: No approved trajectory
- GIVEN a headline KPI with only the generated linear trajectory
- WHEN its card is displayed
- THEN the pace marker is labeled "Linear pace (unapproved)"

### Requirement: Secondary metric
The system SHALL show a secondary KPI with its progress toward target on any card whose goal has a KPI designated Secondary.

#### Scenario: Goal 1 secondary metric
- GIVEN KPI-003 designated Secondary for Goal 1
- WHEN the Goal 1 card is displayed
- THEN it shows Fortune 500 leaders credentialed against the target of 50

### Requirement: Signature visual per goal
The system SHALL show the goal-specific visual defined for each card — progress ring and term trend (Goal 1), hub map and hub timeline (Goal 2), credential trend (Goal 3), expenditure trend and funding gauge (Goal 4), maturity ladder and capability heatmap (Goal 5) — and SHALL provide a text or table alternative for each.

#### Scenario: Hub map
- GIVEN hubs recorded with locations
- WHEN the Goal 2 card is displayed
- THEN each hub appears as a map bubble
- AND the same hubs are available as a table for screen-reader users

### Requirement: Recent activity
The system SHALL show the three most recent activity entries for each goal with date and value, and SHALL NOT display learner-level information.

#### Scenario: Recent grants
- GIVEN five grant entries for Goal 4
- WHEN the Goal 4 card is displayed
- THEN the three most recent grants appear with award date and amount

### Requirement: Data honesty
The system SHALL NOT display placeholder or sample values in production; each metric SHALL appear as Live, Stale, Pending source, or Pending definition, and every displayed value SHALL show its as-of date and source.

#### Scenario: Source not connected
- GIVEN a headline KPI with an owner but no values yet
- WHEN its card is displayed
- THEN it shows "Data source pending" and the owner's name instead of a number

#### Scenario: Stale value
- GIVEN a quarterly KPI whose last value is two quarters old
- WHEN its card is displayed
- THEN the value is greyed and labeled with its as-of date

### Requirement: Drill-through to goal detail
The system SHALL let a viewer open any goal card into the priority detail view showing that goal's objectives, all of its KPIs, and its aligned projects, subject to the viewer's access.

#### Scenario: Drill from Goal 5
- GIVEN the Dean viewing the Goal 5 card
- WHEN the Dean selects it
- THEN the priority detail for SP-05 opens with its objectives, KPIs, and aligned projects

### Requirement: Aligned work summary
The system SHALL be able to show on each card the number of active projects and contributing units aligned to that goal, controlled by a configuration setting, with counts respecting the viewer's access rules.

#### Scenario: Summary enabled
- GIVEN the setting is on and 12 active projects from 4 units align to Goal 3
- WHEN an executive views the Goal 3 card
- THEN it shows "Active work: 12 projects · 4 units" linking to that list

### Requirement: Landing page and presentation
The page SHALL be the first page of the CLL SPM app, SHALL show only college-level aggregates, SHALL convey goal identity and status in text as well as color, and SHALL provide a phone layout.

#### Scenario: Opening the app on a phone
- GIVEN the Dean opens the app on a phone
- WHEN it loads
- THEN the Strategy 2035 page appears first with the timeline above stacked goal cards
