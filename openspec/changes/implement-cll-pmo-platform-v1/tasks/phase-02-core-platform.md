# Phase 02 — Core Platform

**Tasks:** T-018 – T-031 (14) · **Gate:** GATE-2 · **Business milestone:** M3 One record per project
**Depends on:** Phase 01 · **Blocks:** Phases 03, 04, 05

## T-018 — Load the Strategy 2035 pillar and objective taxonomy with effective dating

- [ ] Complete
- **Owner:** `APPENG`
- **Verifier:** `STRATOFF`
- **Dependencies:** T-009, DEP-EXT-12
- **Requirements:** PRJ-003
- **Acceptance Criteria:** AC-PRJ-003-1, AC-PRJ-003-2
- **Tests:** TEST-PRJ-003
- **Evidence:** EV-PRJ-003
- **Release Gates:** GATE-2

## T-019 — Implement the project record and immutable `project_id` issuance

- [ ] Complete
- **Owner:** `APPENG`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-018
- **Requirements:** PRJ-001
- **Acceptance Criteria:** AC-PRJ-001-1, AC-PRJ-001-2
- **Tests:** TEST-PRJ-001
- **Evidence:** EV-PRJ-001
- **Release Gates:** GATE-2

## T-020 — Implement duplicate detection and downstream rename reversion

- [ ] Complete
- **Owner:** `APPENG`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-019
- **Requirements:** PRJ-001
- **Acceptance Criteria:** AC-PRJ-001-3, AC-PRJ-001-4
- **Tests:** TEST-PRJ-001
- **Evidence:** EV-PRJ-001
- **Release Gates:** GATE-2

## T-021 — Implement the lifecycle state machine with gate preconditions

- [ ] Complete
- **Owner:** `APPENG`
- **Verifier:** `QALEAD`
- **Dependencies:** T-019
- **Requirements:** PRJ-002
- **Acceptance Criteria:** AC-PRJ-002-1, AC-PRJ-002-2
- **Tests:** TEST-PRJ-002
- **Evidence:** EV-PRJ-002
- **Release Gates:** GATE-2

## T-022 — Implement transition history with actor, timestamp and reason capture

- [ ] Complete
- **Owner:** `APPENG`
- **Verifier:** `SECARCH`
- **Dependencies:** T-021
- **Requirements:** PRJ-002, PRJ-008
- **Acceptance Criteria:** AC-PRJ-002-3, AC-PRJ-008-1
- **Tests:** TEST-PRJ-002, TEST-PRJ-008
- **Evidence:** EV-PRJ-008
- **Release Gates:** GATE-2

## T-023 — Implement objective retirement flagging and the realignment queue

- [ ] Complete
- **Owner:** `APPENG`
- **Verifier:** `STRATOFF`
- **Dependencies:** T-018
- **Requirements:** PRJ-003
- **Acceptance Criteria:** AC-PRJ-003-3
- **Tests:** TEST-PRJ-003
- **Evidence:** EV-PRJ-003
- **Release Gates:** GATE-2

## T-024 — Implement ownership and RACI with HCM person validation and gap exceptions

- [ ] Complete
- **Owner:** `APPENG`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-011, T-019
- **Requirements:** PRJ-004
- **Acceptance Criteria:** AC-PRJ-004-1, AC-PRJ-004-2, AC-PRJ-004-3
- **Tests:** TEST-PRJ-004
- **Evidence:** EV-PRJ-004
- **Release Gates:** GATE-2

## T-025 — Implement the milestone mirror, baseline capture and slip computation

- [ ] Complete
- **Owner:** `APPENG`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-019
- **Requirements:** PRJ-005
- **Acceptance Criteria:** AC-PRJ-005-1, AC-PRJ-005-2, AC-PRJ-005-3
- **Tests:** TEST-PRJ-005
- **Evidence:** EV-PRJ-005
- **Release Gates:** GATE-2

## T-026 — Implement the RAID log with ratings, review dates and closure retention

- [ ] Complete
- **Owner:** `APPENG`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-019
- **Requirements:** PRJ-006
- **Acceptance Criteria:** AC-PRJ-006-1, AC-PRJ-006-2, AC-PRJ-006-3
- **Tests:** TEST-PRJ-006
- **Evidence:** EV-PRJ-006
- **Release Gates:** GATE-2

## T-027 — Implement funding linkage, worktag attribution and unallocated spend reporting

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-010, T-019
- **Requirements:** PRJ-007
- **Acceptance Criteria:** AC-PRJ-007-1, AC-PRJ-007-2, AC-PRJ-007-3
- **Tests:** TEST-PRJ-007
- **Evidence:** EV-PRJ-007
- **Release Gates:** GATE-2

## T-028 — Implement immutable field-level history and as-of reconstruction

- [ ] Complete
- **Owner:** `APPENG`
- **Verifier:** `SECARCH`
- **Dependencies:** T-022
- **Requirements:** PRJ-008
- **Acceptance Criteria:** AC-PRJ-008-2, AC-PRJ-008-3
- **Tests:** TEST-PRJ-008
- **Evidence:** EV-PRJ-008
- **Release Gates:** GATE-2

## T-029 — Implement the KPI definition registry with stewardship and publication rules

- [ ] Complete
- **Owner:** `DATAGOV`
- **Verifier:** `STRATOFF`
- **Dependencies:** T-018
- **Requirements:** KPI-001
- **Acceptance Criteria:** AC-KPI-001-1, AC-KPI-001-2, AC-KPI-001-3, AC-KPI-001-4
- **Tests:** TEST-KPI-001
- **Evidence:** EV-KPI-001
- **Release Gates:** GATE-2

## T-030 — Implement KPI lineage capture and reproducible recomputation

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-029
- **Requirements:** KPI-002
- **Acceptance Criteria:** AC-KPI-002-1, AC-KPI-002-2, AC-KPI-002-3
- **Tests:** TEST-KPI-002
- **Evidence:** EV-KPI-002
- **Release Gates:** GATE-2

## T-031 — Implement effective-dated targets and thresholds, and run the scale test at ceilings

- [ ] Complete
- **Owner:** `DATAGOV`
- **Verifier:** `PLATFORM`
- **Dependencies:** T-029
- **Requirements:** KPI-003, NFR-003
- **Acceptance Criteria:** AC-KPI-003-1, AC-KPI-003-2, AC-KPI-003-3, AC-NFR-003-1, AC-NFR-003-2, AC-NFR-003-3
- **Tests:** TEST-KPI-003, TEST-NFR-003
- **Evidence:** EV-KPI-003, EV-NFR-003
- **Release Gates:** GATE-2
