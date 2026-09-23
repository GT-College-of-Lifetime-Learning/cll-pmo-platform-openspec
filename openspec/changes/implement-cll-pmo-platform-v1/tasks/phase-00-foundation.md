# Phase 00 — Foundation

**Tasks:** T-001 – T-008 (8) · **Gate:** GATE-0 · **Business milestone:** M1 Delivery capability
**Depends on:** — · **Blocks:** all later phases

Owner and Verifier are role keys from `registries/ownership.md`. A task's
Verifier is never the same role as its Owner.

## T-001 — Provision development, test and production environments with documented parity

- [ ] Complete
- **Owner:** `PLATFORM`
- **Verifier:** `RELMGR`
- **Dependencies:** DEP-EXT-11
- **Requirements:** NFR-007
- **Acceptance Criteria:** AC-NFR-007-1
- **Tests:** TEST-NFR-007
- **Evidence:** EV-NFR-007
- **Release Gates:** GATE-0

## T-002 — Register the platform in Entra ID and create the six role security groups

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `PLATFORM`
- **Dependencies:** DEP-EXT-01
- **Requirements:** SEC-001, SEC-002
- **Acceptance Criteria:** AC-SEC-001-1, AC-SEC-002-1
- **Tests:** TEST-SEC-001, TEST-SEC-002
- **Evidence:** EV-SEC-001
- **Release Gates:** GATE-0, GATE-3

## T-003 — Stand up the CI/CD pipeline with build, test, secret scanning and accessibility checks

- [ ] Complete
- **Owner:** `RELMGR`
- **Verifier:** `PLATFORM`
- **Dependencies:** T-001
- **Requirements:** NFR-007, SEC-006, NFR-005
- **Acceptance Criteria:** AC-NFR-007-2, AC-SEC-006-1, AC-NFR-005-3
- **Tests:** TEST-NFR-007, TEST-SEC-006, TEST-NFR-005
- **Evidence:** EV-NFR-007, EV-SEC-006
- **Release Gates:** GATE-0

## T-004 — Implement the structured run-record and telemetry framework

- [ ] Complete
- **Owner:** `PLATFORM`
- **Verifier:** `DATAENG`
- **Dependencies:** T-001
- **Requirements:** NFR-004
- **Acceptance Criteria:** AC-NFR-004-1, AC-NFR-004-3
- **Tests:** TEST-NFR-004
- **Evidence:** EV-NFR-004
- **Release Gates:** GATE-0

## T-005 — Implement watchdog alerting for failed and missing runs to the on-call owner

- [ ] Complete
- **Owner:** `PLATFORM`
- **Verifier:** `RELMGR`
- **Dependencies:** T-004
- **Requirements:** NFR-004
- **Acceptance Criteria:** AC-NFR-004-2
- **Tests:** TEST-NFR-004
- **Evidence:** EV-NFR-004
- **Release Gates:** GATE-0

## T-006 — Establish release records, commit tagging and the rollback procedure

- [ ] Complete
- **Owner:** `RELMGR`
- **Verifier:** `PLATFORM`
- **Dependencies:** T-003
- **Requirements:** REL-002
- **Acceptance Criteria:** AC-REL-002-1, AC-REL-002-2
- **Tests:** TEST-REL-002
- **Evidence:** EV-REL-002
- **Release Gates:** GATE-0

## T-007 — Submit and clear the institutional security intake review

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `SPONSOR`
- **Dependencies:** DEP-EXT-11
- **Requirements:** SEC-004
- **Acceptance Criteria:** AC-SEC-004-1
- **Tests:** TEST-SEC-004
- **Evidence:** EV-SEC-004
- **Release Gates:** GATE-0, GATE-3

## T-008 — Author the test strategy and register the 72-test catalog skeleton

- [ ] Complete
- **Owner:** `QALEAD`
- **Verifier:** `PLATFORM`
- **Dependencies:** T-003
- **Requirements:** VER-001
- **Acceptance Criteria:** AC-VER-001-1, AC-VER-001-2
- **Tests:** TEST-VER-001
- **Evidence:** EV-VER-001
- **Release Gates:** GATE-0, GATE-8
