# Strategy KPI Data Specification

## Purpose
The data the Strategy 2035 page needs beyond Phase 1's KPI definitions and values: which KPI
leads each card, how pace is measured, recent activity, and the Goal 5 maturity index.

## Requirements

### Requirement: Dashboard roles
Each strategic goal SHALL have exactly one KPI designated Headline and MAY have one designated Secondary; all other KPIs SHALL be designated Detail.

#### Scenario: Second headline rejected
- GIVEN Goal 1 already has KPI-001 as Headline
- WHEN someone designates KPI-002 as Headline for Goal 1
- THEN the change is rejected until KPI-001 is reassigned

### Requirement: KPI basis and counting start
Each KPI SHALL declare a basis of Cumulative, Annual, Point-in-time, or Index, and each Cumulative KPI SHALL declare a counting start date from which values accumulate.

#### Scenario: Cumulative count from the window start
- GIVEN KPI-007 is Cumulative with a counting start of Jan 1, 2026
- WHEN credentials issued in December 2025 are reported
- THEN they are excluded from KPI-007

### Requirement: Trajectories
The system SHALL store expected values by period for each Headline and Secondary KPI with approval status, approver, and date, and SHALL generate a linear trajectory marked unapproved when none has been approved.

#### Scenario: Back-loaded trajectory approved
- GIVEN KPI-001 with a linear default
- WHEN the owner and the Dean approve milestones that stay near zero until degrees launch in 2029
- THEN pace for KPI-001 is measured against the approved milestones
- AND the "unapproved" label is removed

### Requirement: Strategy activity entries
The system SHALL record activity entries typed as term graduates, hub opening, start-up adopted, credential issued, grant awarded, or capability delivered, each with goal, title, date, value, source, and submitter, and SHALL NOT accept learner identities.

#### Scenario: Credential activity entry
- GIVEN a KPI owner recording credentials issued for a program
- WHEN they open the entry form
- THEN it asks for the credential name, the date, and a count
- AND it has no field for individual learners

### Requirement: Digital Transformation Maturity Index
The system SHALL maintain an inventory of CLL capabilities, each rated 1–5 against a published rubric with assessment date, assessor, and evidence link, and SHALL compute the index as the mean current rating of in-scope capabilities.

#### Scenario: Rating without evidence
- GIVEN an assessor rating a workflow at level 3
- WHEN no evidence link is provided
- THEN the rating is not saved

#### Scenario: Index updates after reassessment
- GIVEN an index of 2.6 across 20 in-scope capabilities
- WHEN one capability moves from level 2 to level 4
- THEN the index becomes 2.7

### Requirement: Capability updates from Goal 5 work
When a registered project aligned to SP-05 is closed, the system SHALL prompt its lead to add or update the capability it delivered.

#### Scenario: Automation project closes
- GIVEN a project aligned to SP-05 that automated a workflow
- WHEN its lead moves it to Closed
- THEN the closeout asks the lead to record the workflow's new maturity level with evidence

### Requirement: Value provenance
Every KPI value SHALL record its source, as-of date, and submitter or feed, and the system SHALL reject a value without a source, and the system SHALL display the source, as-of date, and submitter or method with every KPI value shown to viewers.

#### Scenario: Manual value without source
- GIVEN a KPI owner entering a research expenditure figure
- WHEN the source field is empty
- THEN the value is not saved

#### Scenario: Provenance shown on a goal card
- GIVEN a headline KPI value entered by an owner from a named source
- WHEN a viewer sees the value on a Strategy 2035 card or KPI table
- THEN the source, as-of date, and submitter or method are visible in the card's detail

#### Scenario: Provenance on a pending value
- GIVEN a KPI displayed in a Pending source state
- WHEN its card renders
- THEN the owner's name is shown with the pending state instead of a number
- AND no source is fabricated for it
