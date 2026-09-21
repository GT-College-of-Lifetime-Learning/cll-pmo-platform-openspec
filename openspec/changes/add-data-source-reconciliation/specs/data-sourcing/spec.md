# Delta for Data Sourcing

## Purpose
The reconciliation instrument for external data: a catalog of what the dashboards need,
the declared state of each source, incremental integration of real data alongside
fabricated data, and an honest coverage view of what the dashboard can truthfully show.

## ADDED Requirements

### Requirement: Data-needs catalog
The system SHALL maintain a catalog with one row per external data element the dashboards consume, recording at minimum: the element name, the consumer visual or view, the required fields, the reporting cadence, and the definition state, and the catalog SHALL be data, never hard-coded in views.

#### Scenario: Headline KPI appears in the catalog
- GIVEN the Strategy 2035 page consumes five headline KPIs
- WHEN the catalog is opened
- THEN each headline KPI appears as a row naming its consumer view and required fields

#### Scenario: New need added
- GIVEN a dashboard visual gains a new external data dependency
- WHEN the catalog is updated with that element
- THEN the coverage view reflects it without any view-code change

### Requirement: Source states
The system SHALL classify each catalog row's source state as UNDEFINED, MISSING, PARTIAL, or HAVE, where UNDEFINED means the metric's definition itself awaits a decision, and SHALL route UNDEFINED rows to the sponsor before any source-building work begins.

#### Scenario: Definition-gated need routes to the Dean
- GIVEN the learner-touchpoint KPI whose definition is an open question
- WHEN its catalog row is reviewed
- THEN its state reads UNDEFINED and it appears on the needs-attention list for the sponsor
- AND no source-build plan is generated for it

#### Scenario: Declared source upgrades a state
- GIVEN a MISSING row whose steward declares an existing system export
- WHEN the declaration is recorded
- THEN the row's state becomes HAVE with the system, format, and steward recorded

### Requirement: Source declaration capture
The system SHALL accept structured source declarations — one row per candidate source with element, system, format, refresh cadence, steward, and notes — and SHALL record the declaration against the matching catalog row.

#### Scenario: Steward declares a source
- GIVEN a steward submitting a declaration that the registrar system exports term graduates monthly
- WHEN the declaration is captured
- THEN the matching catalog row records system, format, cadence, and steward
- AND the row's state updates according to the declaration

#### Scenario: Declaration without a matching need
- GIVEN a declaration naming an element not in the catalog
- WHEN the declaration is captured
- THEN it is recorded as an unmatched declaration for review
- AND no catalog row is created silently

### Requirement: Incremental integration with origin tagging
The system SHALL support importing real data for a HAVE or PARTIAL need into the working data store alongside fabricated data, and SHALL tag every imported row with its origin, and the tag SHALL be visible wherever the value's provenance is shown.

#### Scenario: Real import lands beside demo data
- GIVEN a calendar of confirmed Institute holidays
- WHEN it is imported for the business-day calendar need
- THEN the business-day computations use the confirmed calendar
- AND the import is recorded with origin and date

#### Scenario: Imported value shows its origin
- GIVEN a KPI value imported from a declared source
- WHEN it is displayed with provenance
- THEN the provenance names the import source, not the fabricated default

#### Scenario: Fabricated data never silently masquerades as real
- GIVEN a value that remains fabricated demo data
- WHEN it is displayed with provenance
- THEN the provenance states the demo origin

### Requirement: Coverage view
The system SHALL provide a coverage view answering, for each catalog row, whether real sourced data exists (sourced), exists in part (partial), or does not (unsourced), and SHALL aggregate the counts by consumer view so a reader can see what each dashboard page can truthfully show today.

#### Scenario: Coverage after one integration
- GIVEN the holiday calendar imported and all KPI values still fabricated
- WHEN the coverage view is opened
- THEN the holiday-calendar row reads sourced and the KPI rows read unsourced
- AND the Strategy 2035 view's summary reflects one sourced element

#### Scenario: Coverage reflects a state change
- GIVEN a MISSING row whose steward declares a partial export
- WHEN the coverage view is next opened
- THEN that row reads partial

### Requirement: Matrix generated from the catalog
The system SHALL generate the working data-source matrix document from the catalog, and SHALL fail generation when the matrix and catalog would disagree, so the committed matrix never drifts from catalog truth.

#### Scenario: Regenerated matrix matches catalog
- GIVEN the catalog with a new HAVE row
- WHEN the matrix is regenerated
- THEN the matrix contains the new row with its source state

#### Scenario: Hand-edited matrix is rejected
- GIVEN a matrix file edited independently of the catalog
- WHEN regeneration runs
- THEN the drift is reported and the matrix is replaced with catalog truth