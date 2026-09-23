# Phase 03 — Security & Quality

**Tasks:** T-032 – T-043 (12) · **Gate:** GATE-3 · **Business milestone:** M4 Trustworthy and protected
**Depends on:** Phase 02 · **Blocks:** Phases 04, 06, 07

## T-032 — Implement OIDC single sign-on with PKCE and the session policy

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `APPENG`
- **Dependencies:** T-002
- **Requirements:** SEC-001
- **Acceptance Criteria:** AC-SEC-001-1, AC-SEC-001-2
- **Tests:** TEST-SEC-001
- **Evidence:** EV-SEC-001
- **Release Gates:** GATE-3

## T-033 — Implement workload identities and break-glass account alerting

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `PLATFORM`
- **Dependencies:** T-032
- **Requirements:** SEC-001
- **Acceptance Criteria:** AC-SEC-001-3, AC-SEC-001-4
- **Tests:** TEST-SEC-001
- **Evidence:** EV-SEC-001
- **Release Gates:** GATE-3

## T-034 — Implement the six roles derived from Entra ID groups with authorisation checks

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-032
- **Requirements:** SEC-002
- **Acceptance Criteria:** AC-SEC-002-1, AC-SEC-002-2, AC-SEC-002-3
- **Tests:** TEST-SEC-002
- **Evidence:** EV-SEC-002
- **Release Gates:** GATE-3

## T-035 — Implement row-level scoping predicates at the data layer

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `APPENG`
- **Dependencies:** T-019, T-034
- **Requirements:** SEC-003, INT-002
- **Acceptance Criteria:** AC-SEC-003-1, AC-SEC-003-2, AC-INT-002-2
- **Tests:** TEST-SEC-003, TEST-INT-002
- **Evidence:** EV-SEC-003, EV-INT-002
- **Release Gates:** GATE-3

## T-036 — Verify scoping parity across dashboard, API and export paths

- [ ] Complete
- **Owner:** `QALEAD`
- **Verifier:** `SECARCH`
- **Dependencies:** T-035
- **Requirements:** SEC-003
- **Acceptance Criteria:** AC-SEC-003-3
- **Tests:** TEST-SEC-003
- **Evidence:** EV-SEC-003
- **Release Gates:** GATE-3, GATE-6

## T-037 — Enforce TLS and at-rest encryption including restricted-source key separation

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `PLATFORM`
- **Dependencies:** T-001, T-007
- **Requirements:** SEC-004
- **Acceptance Criteria:** AC-SEC-004-1, AC-SEC-004-2, AC-SEC-004-3
- **Tests:** TEST-SEC-004
- **Evidence:** EV-SEC-004
- **Release Gates:** GATE-3

## T-038 — Implement the append-only audit log with required fields and 7-year retention

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-034
- **Requirements:** SEC-005, INT-002
- **Acceptance Criteria:** AC-SEC-005-1, AC-SEC-005-2, AC-SEC-005-3, AC-INT-002-4
- **Tests:** TEST-SEC-005, TEST-INT-002
- **Evidence:** EV-SEC-005, EV-INT-002
- **Release Gates:** GATE-3

## T-039 — Implement secret storage, 90-day rotation with 75-day alerting, and annual key re-wrap

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `RELMGR`
- **Dependencies:** T-003
- **Requirements:** SEC-006
- **Acceptance Criteria:** AC-SEC-006-2, AC-SEC-006-3
- **Tests:** TEST-SEC-006
- **Evidence:** EV-SEC-006
- **Release Gates:** GATE-3

## T-040 — Implement quarterly recertification campaigns with automatic removal

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `SPONSOR`
- **Dependencies:** T-034
- **Requirements:** SEC-007
- **Acceptance Criteria:** AC-SEC-007-1, AC-SEC-007-2, AC-SEC-007-3
- **Tests:** TEST-SEC-007
- **Evidence:** EV-SEC-007
- **Release Gates:** GATE-3

## T-041 — Implement ingestion-time rule evaluation, quarantine and per-run reporting

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-017
- **Requirements:** DQA-002
- **Acceptance Criteria:** AC-DQA-002-1, AC-DQA-002-2, AC-DQA-002-3
- **Tests:** TEST-DQA-002
- **Evidence:** EV-DQA-002
- **Release Gates:** GATE-3

## T-042 — Implement the data quality scorecard, degraded-source marking and 24-month history

- [ ] Complete
- **Owner:** `DATAGOV`
- **Verifier:** `PLATFORM`
- **Dependencies:** T-041
- **Requirements:** DQA-004
- **Acceptance Criteria:** AC-DQA-004-1, AC-DQA-004-2, AC-DQA-004-3
- **Tests:** TEST-DQA-004
- **Evidence:** EV-DQA-004
- **Release Gates:** GATE-3

## T-043 — Implement the exception queue, escalation, quarantine replay and replay idempotency

- [ ] Complete
- **Owner:** `DATAGOV`
- **Verifier:** `QALEAD`
- **Dependencies:** T-041, DEP-EXT-11
- **Requirements:** DQA-005, DQA-006
- **Acceptance Criteria:** AC-DQA-005-1, AC-DQA-005-2, AC-DQA-005-3, AC-DQA-006-1, AC-DQA-006-2, AC-DQA-006-3
- **Tests:** TEST-DQA-005, TEST-DQA-006
- **Evidence:** EV-DQA-005, EV-DQA-006
- **Release Gates:** GATE-3
