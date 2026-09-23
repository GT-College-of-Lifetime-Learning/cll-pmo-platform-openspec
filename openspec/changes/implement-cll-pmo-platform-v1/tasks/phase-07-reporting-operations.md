# Phase 07 — Reporting & Operations

**Tasks:** T-081 – T-091 (11) · **Gate:** GATE-7 · **Business milestone:** M8 Board package from the platform
**Depends on:** Phases 04, 05, 06 · **Blocks:** Phase 08

## T-081 — Build the reporting calendar aligned to Finance close and Board meeting dates

- [ ] Complete
- **Owner:** `PORTFOLIO`
- **Verifier:** `SPONSOR`
- **Dependencies:** T-064, DEP-EXT-13
- **Requirements:** BRD-007
- **Acceptance Criteria:** AC-BRD-007-1
- **Tests:** TEST-BRD-007
- **Evidence:** EV-BRD-007
- **Release Gates:** GATE-7

## T-082 — Implement the readiness checklist with blockers and a 10-business-day lead

- [ ] Complete
- **Owner:** `PORTFOLIO`
- **Verifier:** `SPONSOR`
- **Dependencies:** T-043, T-081
- **Requirements:** BRD-007
- **Acceptance Criteria:** AC-BRD-007-2, AC-BRD-007-3
- **Tests:** TEST-BRD-007
- **Evidence:** EV-BRD-007
- **Release Gates:** GATE-7

## T-083 — Implement snapshot creation, certification and immutability

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-064, T-077
- **Requirements:** BRD-003
- **Acceptance Criteria:** AC-BRD-003-1, AC-BRD-003-2, AC-BRD-003-3
- **Tests:** TEST-BRD-003
- **Evidence:** EV-BRD-003
- **Release Gates:** GATE-7

## T-084 — Implement package assembly from a single certified snapshot

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-083
- **Requirements:** BRD-001
- **Acceptance Criteria:** AC-BRD-001-1, AC-BRD-001-2, AC-BRD-001-3
- **Tests:** TEST-BRD-001
- **Evidence:** EV-BRD-001
- **Release Gates:** GATE-7

## T-085 — Implement narrative capture, approval routing and publication blocking

- [ ] Complete
- **Owner:** `PORTFOLIO`
- **Verifier:** `SPONSOR`
- **Dependencies:** T-066, T-084
- **Requirements:** BRD-002
- **Acceptance Criteria:** AC-BRD-002-1, AC-BRD-002-2, AC-BRD-002-3
- **Tests:** TEST-BRD-002
- **Evidence:** EV-BRD-002
- **Release Gates:** GATE-7

## T-086 — Implement PDF, PPTX and XLSX exports with stamping and checksums

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `QALEAD`
- **Dependencies:** T-055, T-084
- **Requirements:** BRD-004
- **Acceptance Criteria:** AC-BRD-004-1, AC-BRD-004-2, AC-BRD-004-3
- **Tests:** TEST-BRD-004
- **Evidence:** EV-BRD-004
- **Release Gates:** GATE-7

## T-087 — Implement SharePoint distribution with approval gating and access logging

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `SECARCH`
- **Dependencies:** T-086, DEP-EXT-10
- **Requirements:** BRD-005
- **Acceptance Criteria:** AC-BRD-005-1, AC-BRD-005-2, AC-BRD-005-3
- **Tests:** TEST-BRD-005
- **Evidence:** EV-BRD-005
- **Release Gates:** GATE-7

## T-088 — Implement comparatives from published snapshots with restatement disclosure

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-066, T-083
- **Requirements:** BRD-006
- **Acceptance Criteria:** AC-BRD-006-1, AC-BRD-006-2, AC-BRD-006-3
- **Tests:** TEST-BRD-006
- **Evidence:** EV-BRD-006
- **Release Gates:** GATE-7

## T-089 — Implement retention enforcement and purge logging per data class

- [ ] Complete
- **Owner:** `PLATFORM`
- **Verifier:** `SECARCH`
- **Dependencies:** T-038, T-083
- **Requirements:** NFR-006
- **Acceptance Criteria:** AC-NFR-006-1, AC-NFR-006-2, AC-NFR-006-3
- **Tests:** TEST-NFR-006
- **Evidence:** EV-NFR-006
- **Release Gates:** GATE-7

## T-090 — Implement availability monitoring and the quarterly restore test

- [ ] Complete
- **Owner:** `PLATFORM`
- **Verifier:** `RELMGR`
- **Dependencies:** T-005
- **Requirements:** NFR-002
- **Acceptance Criteria:** AC-NFR-002-1, AC-NFR-002-2
- **Tests:** TEST-NFR-002
- **Evidence:** EV-NFR-002
- **Release Gates:** GATE-7

## T-091 — Produce the shadow board package and reconcile it to the manual package

- [ ] Complete
- **Owner:** `BILEAD`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-084, T-085, T-086, T-087, T-088
- **Requirements:** BRD-001, DQA-003
- **Acceptance Criteria:** AC-BRD-001-2, AC-DQA-003-3
- **Tests:** TEST-BRD-001, TEST-DQA-003
- **Evidence:** EV-BRD-001, EV-DQA-003
- **Release Gates:** GATE-7
