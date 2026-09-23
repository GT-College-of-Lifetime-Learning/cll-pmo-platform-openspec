# Phase 01 — Source Alignment

**Tasks:** T-009 – T-017 (9) · **Gate:** GATE-1 · **Business milestone:** M2 Source agreement
**Depends on:** Phase 00 · **Blocks:** Phase 02

## T-009 — Ingest IR conformed dimensions and enforce referential integrity

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-004, DEP-EXT-04
- **Requirements:** INT-008
- **Acceptance Criteria:** AC-INT-008-1, AC-INT-008-2
- **Tests:** TEST-INT-008
- **Evidence:** EV-INT-008
- **Release Gates:** GATE-1

## T-010 — Build Workday Financials ingestion with the 90-day trailing re-read

- [ ] Complete
- **Owner:** `INTENG`
- **Verifier:** `DATAENG`
- **Dependencies:** T-009, DEP-EXT-02
- **Requirements:** INT-001
- **Acceptance Criteria:** AC-INT-001-1, AC-INT-001-2
- **Tests:** TEST-INT-001
- **Evidence:** EV-INT-001
- **Release Gates:** GATE-1

## T-011 — Build Workday HCM ingestion with restricted-data handling

- [ ] Complete
- **Owner:** `INTENG`
- **Verifier:** `SECARCH`
- **Dependencies:** T-009, DEP-EXT-03
- **Requirements:** INT-002
- **Acceptance Criteria:** AC-INT-002-1
- **Tests:** TEST-INT-002
- **Evidence:** EV-INT-002
- **Release Gates:** GATE-1

## T-012 — Build Banner enrollment ingestion with a fail-closed identifiable-data guard

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-009, DEP-EXT-05
- **Requirements:** INT-003
- **Acceptance Criteria:** AC-INT-003-1, AC-INT-003-2
- **Tests:** TEST-INT-003
- **Evidence:** EV-INT-003
- **Release Gates:** GATE-1

## T-013 — Build Salesforce pipeline ingestion with incremental high-water mark extraction

- [ ] Complete
- **Owner:** `INTENG`
- **Verifier:** `DATAENG`
- **Dependencies:** T-009, DEP-EXT-06
- **Requirements:** INT-004
- **Acceptance Criteria:** AC-INT-004-1
- **Tests:** TEST-INT-004
- **Evidence:** EV-INT-004
- **Release Gates:** GATE-1

## T-014 — Implement the scheduler with fixed dependency order and hold-on-failure

- [ ] Complete
- **Owner:** `INTENG`
- **Verifier:** `PLATFORM`
- **Dependencies:** T-010, T-011
- **Requirements:** INT-010, INT-008
- **Acceptance Criteria:** AC-INT-010-1, AC-INT-008-3
- **Tests:** TEST-INT-010, TEST-INT-008
- **Evidence:** EV-INT-010
- **Release Gates:** GATE-1

## T-015 — Implement bounded retry with backoff and landing-zone backfill replay

- [ ] Complete
- **Owner:** `INTENG`
- **Verifier:** `DATAENG`
- **Dependencies:** T-014
- **Requirements:** INT-010
- **Acceptance Criteria:** AC-INT-010-2, AC-INT-010-3
- **Tests:** TEST-INT-010
- **Evidence:** EV-INT-010
- **Release Gates:** GATE-1

## T-016 — Implement contract validation, version stamping and fail-closed breach handling

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-010
- **Requirements:** INT-011
- **Acceptance Criteria:** AC-INT-011-1, AC-INT-011-2
- **Tests:** TEST-INT-011
- **Evidence:** EV-INT-011
- **Release Gates:** GATE-1, GATE-6

## T-017 — Establish the data quality rule catalog with blocking rules for all contracted keys

- [ ] Complete
- **Owner:** `DATAGOV`
- **Verifier:** `DATAENG`
- **Dependencies:** T-016
- **Requirements:** DQA-001
- **Acceptance Criteria:** AC-DQA-001-1, AC-DQA-001-2, AC-DQA-001-3
- **Tests:** TEST-DQA-001
- **Evidence:** EV-DQA-001
- **Release Gates:** GATE-1
