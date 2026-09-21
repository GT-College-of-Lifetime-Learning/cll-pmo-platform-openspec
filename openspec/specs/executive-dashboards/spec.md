# Executive Dashboards Specification

## Purpose
Role-specific views that let the Dean, the TCC, and unit leaders
see portfolio health, strategic alignment, KPIs, and needed decisions without requesting
manual reports.

## Requirements

### Requirement: Dean overview
The system SHALL provide a college-wide overview showing items needing executive decisions, status by strategic priority, executive milestones due in the next 90 days, KPI progress against target, and portfolio-wide status currency.

#### Scenario: Preparing for a leadership meeting
- GIVEN the Dean opens the overview
- WHEN it loads
- THEN items with Decision Needed appear first with their asks
- AND each priority shows counts of Green, Amber, Red, and Stale items

### Requirement: Governance view
The system SHALL provide a TCC governance view showing the intake pipeline by stage and age, requests awaiting decision with scores, Tier 2 approvals open for call-up, recent decisions, and cross-unit items.

#### Scenario: Aging requests
- GIVEN requests awaiting decision for more than 30 days
- WHEN the governance view is opened
- THEN those requests are highlighted as aging

### Requirement: Unit view
The system SHALL provide each unit leader a view of their unit's items, overdue updates, upcoming milestones, and unaligned items.

#### Scenario: Unit leader finds gaps
- GIVEN a unit with two overdue updates and one unaligned project
- WHEN the unit leader opens the unit view
- THEN all three appear in an Action Needed section

### Requirement: Item drill-through
The system SHALL let authorized viewers drill from any summary to an item detail showing its status history, milestones, KPIs, decisions, and workspace link.

#### Scenario: Drill from a Red count
- GIVEN the Dean sees two Red items under a priority
- WHEN the Dean selects that count
- THEN the two items are listed
- AND each opens to its detail page

### Requirement: Role-based data access
The system SHALL restrict item detail by role: executive roles see all items; other users see their own unit's items in full — including their own unit's Confidential items — and non-confidential Tier 1 items college-wide; Confidential items are visible in detail only to executive roles and their own unit, and to all other viewers only as masked counts in aggregates.

#### Scenario: Another unit's Tier 2 work
- GIVEN a unit leader from Unit A
- WHEN they view dashboards
- THEN Unit B's Tier 2 items are not shown in detail

### Requirement: Data freshness
Every dashboard page SHALL display when its data was last refreshed, and data SHALL refresh at least once per business day.

#### Scenario: Refresh failure
- GIVEN a scheduled refresh that fails
- WHEN a viewer opens a dashboard
- THEN the last successful refresh time is shown
- AND the portfolio analyst has been notified of the failure

### Requirement: Accessibility and mobile use
Dashboards SHALL conform to WCAG 2.1 AA, SHALL NOT convey status by color alone, and SHALL provide a phone-optimized layout for the Dean overview.

#### Scenario: Status without color
- GIVEN a viewer who cannot distinguish red from green
- WHEN they view status indicators
- THEN each status is also conveyed by a text label or shape

### Requirement: Meeting-ready export
The system SHALL allow authorized viewers to export the Dean overview and governance view for meeting packets.

#### Scenario: Export for a TCC packet
- GIVEN the portfolio analyst preparing a TCC meeting
- WHEN they export the governance view
- THEN the export reflects current filters and shows the refresh timestamp
