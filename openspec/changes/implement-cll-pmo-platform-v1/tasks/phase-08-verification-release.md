# Phase 08 — Verification & Release

**Tasks:** T-092 – T-101 (10) · **Gate:** GATE-8 · **Business milestone:** M9 Strategy 2035 on the record
**Depends on:** all phases · **Blocks:** production go-live

## T-092 — Complete test coverage for all 72 requirements and 223 acceptance criteria

- [ ] Complete
- **Owner:** `QALEAD`
- **Verifier:** `SPONSOR`
- **Dependencies:** T-008, T-080, T-091
- **Requirements:** VER-001
- **Acceptance Criteria:** AC-VER-001-1, AC-VER-001-2
- **Tests:** TEST-VER-001
- **Evidence:** EV-VER-001
- **Release Gates:** GATE-8

## T-093 — Implement gate blocking on uncovered, unevidenced or failing criteria

- [ ] Complete
- **Owner:** `RELMGR`
- **Verifier:** `QALEAD`
- **Dependencies:** T-092
- **Requirements:** VER-001, REL-001
- **Acceptance Criteria:** AC-VER-001-3, AC-REL-001-2
- **Tests:** TEST-VER-001, TEST-REL-001
- **Evidence:** EV-VER-001, EV-REL-001
- **Release Gates:** GATE-8

## T-094 — Generate the traceability matrix and close every chain gap

- [ ] Complete
- **Owner:** `QALEAD`
- **Verifier:** `RELMGR`
- **Dependencies:** T-092
- **Requirements:** VER-002
- **Acceptance Criteria:** AC-VER-002-1, AC-VER-002-2
- **Tests:** TEST-VER-002
- **Evidence:** EV-VER-002
- **Release Gates:** GATE-8

## T-095 — Lock evidence on gate closure and enforce 7-year evidence retention

- [ ] Complete
- **Owner:** `QALEAD`
- **Verifier:** `SECARCH`
- **Dependencies:** T-089, T-094
- **Requirements:** VER-002
- **Acceptance Criteria:** AC-VER-002-3
- **Tests:** TEST-VER-002
- **Evidence:** EV-VER-002
- **Release Gates:** GATE-8

## T-096 — Re-run performance validation on the release build

- [ ] Complete
- **Owner:** `PLATFORM`
- **Verifier:** `QALEAD`
- **Dependencies:** T-054, DEP-EXT-14
- **Requirements:** NFR-001
- **Acceptance Criteria:** AC-NFR-001-1, AC-NFR-001-2, AC-NFR-001-3
- **Tests:** TEST-NFR-001
- **Evidence:** EV-NFR-001
- **Release Gates:** GATE-8

## T-097 — Re-run the accessibility audit on the release build including exported artifacts

- [ ] Complete
- **Owner:** `A11Y`
- **Verifier:** `QALEAD`
- **Dependencies:** T-055, T-086, DEP-EXT-15
- **Requirements:** NFR-005
- **Acceptance Criteria:** AC-NFR-005-1, AC-NFR-005-2
- **Tests:** TEST-NFR-005
- **Evidence:** EV-NFR-005
- **Release Gates:** GATE-8

## T-098 — Execute user acceptance testing across the six roles and triage defects

- [ ] Complete
- **Owner:** `QALEAD`
- **Verifier:** `SPONSOR`
- **Dependencies:** T-080, T-091
- **Requirements:** VER-003
- **Acceptance Criteria:** AC-VER-003-1, AC-VER-003-2
- **Tests:** TEST-VER-003
- **Evidence:** EV-VER-003
- **Release Gates:** GATE-8

## T-099 — Record UAT sign-off with signatory, role, date and build tested

- [ ] Complete
- **Owner:** `QALEAD`
- **Verifier:** `SPONSOR`
- **Dependencies:** T-098
- **Requirements:** VER-003
- **Acceptance Criteria:** AC-VER-003-3
- **Tests:** TEST-VER-003
- **Evidence:** EV-VER-003
- **Release Gates:** GATE-8

## T-100 — Rehearse rollback, enforce the reporting change freeze and reconcile environment drift

- [ ] Complete
- **Owner:** `RELMGR`
- **Verifier:** `PLATFORM`
- **Dependencies:** T-006, T-083
- **Requirements:** REL-002, NFR-007
- **Acceptance Criteria:** AC-REL-002-2, AC-REL-002-3, AC-NFR-007-3
- **Tests:** TEST-REL-002, TEST-NFR-007
- **Evidence:** EV-REL-002, EV-NFR-007
- **Release Gates:** GATE-8

## T-101 — Close GATE-0 through GATE-8 with the waiver register and execute go-live

- [ ] Complete
- **Owner:** `RELMGR`
- **Verifier:** `SPONSOR`
- **Dependencies:** T-093, T-094, T-095, T-096, T-097, T-099, T-100
- **Requirements:** REL-001, REL-002, NFR-002
- **Acceptance Criteria:** AC-REL-001-1, AC-REL-001-3, AC-REL-002-1, AC-NFR-002-3
- **Tests:** TEST-REL-001, TEST-REL-002, TEST-NFR-002
- **Evidence:** EV-REL-001, EV-REL-002, EV-NFR-002
- **Release Gates:** GATE-8
