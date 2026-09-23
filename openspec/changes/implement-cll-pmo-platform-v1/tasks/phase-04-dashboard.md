# Phase 04 — Dashboard

**Tasks:** T-044 – T-055 (12) · **Gate:** GATE-4 · **Business milestone:** M5 Leadership self-service
**Depends on:** Phases 02, 03 · **Blocks:** Phase 07

## T-044 — Implement portfolio health computation rules and the pillar overview

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `QALEAD`
- **Dependencies:** T-031, T-035
- **Requirements:** EXD-001
- **Acceptance Criteria:** AC-EXD-001-1, AC-EXD-001-2
- **Tests:** TEST-EXD-001
- **Evidence:** EV-EXD-001
- **Release Gates:** GATE-4

## T-045 — Implement indicator explainability and no-data-in-scope rendering

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-044
- **Requirements:** EXD-001
- **Acceptance Criteria:** AC-EXD-001-3, AC-EXD-001-4
- **Tests:** TEST-EXD-001
- **Evidence:** EV-EXD-001
- **Release Gates:** GATE-4

## T-046 — Implement KPI trend charts with target and threshold bands and version marks

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-031
- **Requirements:** EXD-002
- **Acceptance Criteria:** AC-EXD-002-1, AC-EXD-002-2, AC-EXD-002-3
- **Tests:** TEST-EXD-002
- **Evidence:** EV-EXD-002
- **Release Gates:** GATE-4

## T-047 — Implement pillar to objective to project drill-down with context preservation

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `QALEAD`
- **Dependencies:** T-044
- **Requirements:** EXD-003
- **Acceptance Criteria:** AC-EXD-003-1, AC-EXD-003-2
- **Tests:** TEST-EXD-003
- **Evidence:** EV-EXD-003
- **Release Gates:** GATE-4

## T-048 — Implement URL-addressable dashboard state

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `APPENG`
- **Dependencies:** T-047
- **Requirements:** EXD-003
- **Acceptance Criteria:** AC-EXD-003-3
- **Tests:** TEST-EXD-003
- **Evidence:** EV-EXD-003
- **Release Gates:** GATE-4

## T-049 — Implement the risk and issue heat map with cell drill-in and closed-items view

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-026, T-047
- **Requirements:** EXD-004
- **Acceptance Criteria:** AC-EXD-004-1, AC-EXD-004-2, AC-EXD-004-3
- **Tests:** TEST-EXD-004
- **Evidence:** EV-EXD-004
- **Release Gates:** GATE-4

## T-050 — Implement the financial burn and variance view with closed-period immutability

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `DATAENG`
- **Dependencies:** T-027
- **Requirements:** EXD-005
- **Acceptance Criteria:** AC-EXD-005-1, AC-EXD-005-2
- **Tests:** TEST-EXD-005
- **Evidence:** EV-EXD-005
- **Release Gates:** GATE-4

## T-051 — Implement explicit suppression rendering for effort figures

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `SECARCH`
- **Dependencies:** T-011, T-035
- **Requirements:** EXD-005, INT-002
- **Acceptance Criteria:** AC-EXD-005-3, AC-INT-002-3
- **Tests:** TEST-EXD-005, TEST-INT-002
- **Evidence:** EV-EXD-005, EV-INT-002
- **Release Gates:** GATE-4

## T-052 — Implement the milestone timeline with baseline versus current dates and overdue flags

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-025
- **Requirements:** EXD-006
- **Acceptance Criteria:** AC-EXD-006-1, AC-EXD-006-2, AC-EXD-006-3
- **Tests:** TEST-EXD-006
- **Evidence:** EV-EXD-006
- **Release Gates:** GATE-4

## T-053 — Implement the freshness and completeness indicator wired to run and data quality state

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-005, T-042
- **Requirements:** EXD-007
- **Acceptance Criteria:** AC-EXD-007-1, AC-EXD-007-2, AC-EXD-007-3
- **Tests:** TEST-EXD-007
- **Evidence:** EV-EXD-007
- **Release Gates:** GATE-4

## T-054 — Execute performance validation at 150 concurrent users

- [ ] Complete
- **Owner:** `PLATFORM`
- **Verifier:** `QALEAD`
- **Dependencies:** T-046, T-049, T-050, T-052, T-053, DEP-EXT-14
- **Requirements:** NFR-001
- **Acceptance Criteria:** AC-NFR-001-1, AC-NFR-001-2, AC-NFR-001-3
- **Tests:** TEST-NFR-001
- **Evidence:** EV-NFR-001
- **Release Gates:** GATE-4

## T-055 — Remediate WCAG 2.2 AA findings and verify keyboard and non-colour status conveyance

- [ ] Complete
- **Owner:** `A11Y`
- **Verifier:** `BILEAD`
- **Dependencies:** T-046, T-052, DEP-EXT-15
- **Requirements:** EXD-008, NFR-005
- **Acceptance Criteria:** AC-EXD-008-1, AC-EXD-008-2, AC-EXD-008-3, AC-NFR-005-1
- **Tests:** TEST-EXD-008, TEST-NFR-005
- **Evidence:** EV-EXD-008, EV-NFR-005
- **Release Gates:** GATE-4
