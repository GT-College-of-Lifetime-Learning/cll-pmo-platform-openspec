# Delta for Executive Dashboards

## Purpose
Extends the executive surface: capacity joins the Dean overview and schedule-risk
indicators join Tier 1 item reporting, both respecting the existing access rules.

## MODIFIED Requirements

### Requirement: Dean overview
The system SHALL provide a college-wide overview showing items needing executive decisions, status by strategic priority, executive milestones due in the next 90 days, KPI progress against target, portfolio-wide status currency, and college-level capacity utilization by unit.

#### Scenario: Preparing for a leadership meeting
- GIVEN the Dean opens the overview
- WHEN it loads
- THEN items with Decision Needed appear first with their asks
- AND each priority shows counts of Green, Amber, Red, and Stale items

#### Scenario: Staffing question at a glance
- GIVEN the Dean opens the overview
- WHEN it loads
- THEN the capacity summary names any over-allocated units for the current period
- AND selects through to the units' driving items

### Requirement: Item drill-through
The system SHALL let authorized viewers drill from any summary to an item detail showing its status history, milestones, KPIs, decisions, workspace link, and — for a Tier 1 item with a linked execution plan — its schedule-risk indicator and recent sync state.

#### Scenario: Drill from a Red count
- GIVEN the Dean sees two Red items under a priority
- WHEN the Dean selects that count
- THEN the two items are listed
- AND each opens to its detail page

#### Scenario: Tier 1 schedule risk visible on detail
- GIVEN a synced Tier 1 item whose next milestone has slipped past its baseline twice
- WHEN its detail page is opened
- THEN the schedule-risk indicator shows the slip with text, not color alone
- AND the sync state with its last successful time is shown