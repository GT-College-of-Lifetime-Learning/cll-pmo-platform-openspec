# Data Feed Specification

## Purpose
A versioned, consumable export of the dashboard's data — one feed consumed by the app
itself, testable, and a stable contract for any external consumer including the future
Power BI model.

## Requirements

### Requirement: Versioned feed
The system SHALL publish a feed of dashboard headline data — KPI values, RAG counts by priority, status currency, intake aging, readiness summary — as files under a feed directory plus an HTTP endpoint, and the feed SHALL carry a version number.

#### Scenario: Feed reflects current build
- GIVEN a freshly built database
- WHEN the feed is exported
- THEN feed values match the dashboard pages' values for the same data

### Requirement: Manifest
The system SHALL write a manifest with each feed export containing at least: generated-at timestamp, source identifier and build reference, per-file row counts, and the feed version.

#### Scenario: Manifest row counts
- GIVEN a feed export with 5 RAG-count rows
- WHEN the manifest is read
- THEN it lists that file with row count 5

### Requirement: Empty-state discipline
The system SHALL write every feed file on every export, even when a file has no data rows (headers only), so consumers can render an explicit no-data state instead of guessing or failing.

#### Scenario: Empty RAG counts
- GIVEN a database with no work items
- WHEN the feed is exported
- THEN the RAG-counts file exists with its header row and zero data rows
- AND the manifest records row count 0

### Requirement: Injection-safe strings
The system SHALL guard string cells in any CSV export against spreadsheet formula injection by prefixing cells that begin with a formula character.

#### Scenario: Title beginning with an equals sign
- GIVEN an item titled "=SUM(A1)"
- WHEN feeds are exported as CSV
- THEN the exported cell renders as text, not a formula, when opened in a spreadsheet

### Requirement: Feed endpoint honors access rules
The HTTP feed endpoint SHALL apply the same role-based filtering as the dashboards; the file export intended for the Power BI spine carries only college-level aggregates by construction.

#### Scenario: Unit role requests the feed
- GIVEN a unit leader requesting the feed endpoint
- WHEN it returns
- THEN item-level rows respect the same visibility rules as the dashboard for that role
