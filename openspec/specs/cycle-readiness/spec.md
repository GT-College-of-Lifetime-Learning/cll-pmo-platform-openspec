# Cycle Readiness Specification

## Purpose
Before anyone consumes a dashboard, the system answers whether the data behind it is
trustworthy this cycle — and shows what's blocking if not.

## Requirements

### Requirement: Readiness check
The system SHALL, on demand and at each refresh, evaluate a defined set of readiness gates and report each as OK, WARN, or BLOCKING.

#### Scenario: Healthy cycle
- GIVEN a build where all active items have current updates and no flow failures
- WHEN readiness is evaluated
- THEN every gate reports OK
- AND the readiness page states the cycle is ready to consume

#### Scenario: Gate definitions are published
- GIVEN any viewer opening the readiness page
- WHEN it renders
- THEN each gate's name, current value, threshold, and state are listed in text

### Requirement: Readiness gates
The system SHALL evaluate at minimum these gates: status currency percentage against its threshold, count of stale active items, unrecoverable flow or form failures, expired call-up windows not yet closed, and decisions awaiting action past their service level.

#### Scenario: Currency below threshold
- GIVEN status currency of 82% against a 90% threshold
- WHEN readiness is evaluated
- THEN the currency gate reports BLOCKING
- AND the page names the threshold and the actual value

#### Scenario: Expired call-up window open
- GIVEN a Tier 2 approval whose 10-business-day call-up window has passed
- WHEN readiness is evaluated
- THEN the call-up gate reports WARN until the window is closed by hygiene

### Requirement: Blocking gates are visible, not fatal
The system SHALL render the readiness page even when gates fail, and SHALL present the failing gates and their details as the page's content rather than an error state.

#### Scenario: Readiness with blockers
- GIVEN a build where the currency gate is BLOCKING
- WHEN the readiness page is opened
- THEN the page renders with the BLOCKING gate listed first with its detail
- AND the dashboard remains reachable with its trust state labeled degraded

### Requirement: Trust state linked from dashboards
Every dashboard page SHALL display or link the current readiness summary, and SHALL label itself degraded when any BLOCKING gate exists.

#### Scenario: Dean opens a degraded dashboard
- GIVEN a BLOCKING readiness gate
- WHEN the Dean opens the overview
- THEN the page shows a degraded-trust indicator linking to the readiness page
