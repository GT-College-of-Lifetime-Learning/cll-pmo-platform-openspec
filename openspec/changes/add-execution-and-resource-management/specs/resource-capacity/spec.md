# Delta for Resource Capacity

## Purpose
Answer the question Phase 1 cannot: does CLL have the people to deliver what it has
committed to? Allocations per item per period roll up to unit capacity, over-allocation
is visible before work is approved, and the answer respects privacy decisions.

## ADDED Requirements

### Requirement: Allocations per item
The system SHALL record, for each active registered item, an allocation of effort per reporting period — expressed as a percentage of a full-time contribution or in hours, at the granularity the Dean selects (named person or role) — with the unit head accountable for keeping allocations current.

#### Scenario: Unit head allocates
- GIVEN an active Tier 1 project in Unit A
- WHEN the unit head records an allocation of 30 percent for the month
- THEN the allocation is stored against that item and month with the allocator recorded

#### Scenario: Allocation granularity matches the privacy decision
- GIVEN the Dean has selected role-level granularity
- WHEN a unit head allocates
- THEN the form offers roles, and individual people are not addressable

### Requirement: Unit capacity
The system SHALL compute each unit's committed capacity per period as the sum of its items' allocations, SHALL compare it against the unit's stated available capacity, and SHALL express the result as utilization with the states unallocated, allocated, at capacity, and over-allocated.

#### Scenario: Heatmap cell
- GIVEN a unit committed to 1.2 full-time-equivalents of allocations against one available
- WHEN the capacity heatmap is viewed
- THEN that unit-period cell reads over-allocated at 120 percent with a text label, not color alone

#### Scenario: Quiet month
- GIVEN a unit with no active allocations for a month
- WHEN the heatmap is viewed
- THEN that cell reads unallocated

### Requirement: Over-allocation visibility
The system SHALL surface over-allocated unit-periods to the unit head when recorded, to governance when the over-allocation involves cross-unit work, and SHALL link each over-allocation to the items driving it.

#### Scenario: Over-allocation warning on entry
- GIVEN a unit already at capacity
- WHEN its unit head records another allocation
- THEN the response shows the over-allocation with the driving items listed
- AND the allocation is stored — visibility, not prevention

#### Scenario: Cross-unit over-allocation reaches governance
- GIVEN an over-allocated unit whose largest driving item is cross-unit
- WHEN the governance view is opened
- THEN the over-allocation appears with the cross-unit items named

### Requirement: Capacity in executive reporting
The system SHALL include a college-level capacity view in executive dashboards showing utilization by unit and period, and SHALL let the Dean drill from an over-allocated unit to its driving items.

#### Scenario: Dean checks staffing before approving
- GIVEN a Tier 1 request awaiting TCC decision
- WHEN the Dean views the capacity heatmap for its lead unit
- THEN current utilization, remaining capacity, and the committed pipeline are visible alongside the request

### Requirement: Allocation currency
The system SHALL flag allocations not reviewed by the unit head within the monthly cycle as stale, and SHALL NOT compute capacity for a unit-period from stale allocations without labeling the result.

#### Scenario: Stale allocations labeled
- GIVEN a unit whose allocations were last reviewed two cycles ago
- WHEN capacity is computed
- THEN the unit's utilization carries a stale label with the review date

### Requirement: Privacy of granularity
The system SHALL enforce the selected allocation granularity (named person or role) at entry and in every view, and SHALL NOT expose person-level allocation anywhere when role-level is selected.

#### Scenario: Person-level view under role-level policy
- GIVEN role-level granularity selected
- WHEN any capacity or allocation view is opened
- THEN no screen addresses allocation by individual person