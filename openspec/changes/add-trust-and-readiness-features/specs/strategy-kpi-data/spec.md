# Delta for Strategy KPI Data

## Purpose
Extends the strategy-kpi-data capability: provenance that is captured must also be
*visible* — a viewer can see where every displayed number came from.

## MODIFIED Requirements

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