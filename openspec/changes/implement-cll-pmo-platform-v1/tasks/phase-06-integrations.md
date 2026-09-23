# Phase 06 — Integrations

**Tasks:** T-067 – T-080 (14) · **Gate:** GATE-6 · **Business milestone:** M7 Self-refreshing portfolio
**Depends on:** Phase 03 · **Blocks:** Phase 07

## T-067 — Build Smartsheet plan ingestion, four times daily plus webhooks

- [ ] Complete
- **Owner:** `INTENG`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-014, DEP-EXT-07
- **Requirements:** INT-005
- **Acceptance Criteria:** AC-INT-005-1, AC-INT-005-2
- **Tests:** TEST-INT-005
- **Evidence:** EV-INT-005
- **Release Gates:** GATE-6

## T-068 — Implement Smartsheet write-back limited to the four platform-owned fields

- [ ] Complete
- **Owner:** `INTENG`
- **Verifier:** `DATAENG`
- **Dependencies:** T-067
- **Requirements:** INT-005
- **Acceptance Criteria:** AC-INT-005-3
- **Tests:** TEST-INT-005
- **Evidence:** EV-INT-005
- **Release Gates:** GATE-6

## T-069 — Wire Smartsheet milestones into registry baseline and slip computation

- [ ] Complete
- **Owner:** `APPENG`
- **Verifier:** `PORTFOLIO`
- **Dependencies:** T-025, T-067
- **Requirements:** PRJ-005, INT-005
- **Acceptance Criteria:** AC-PRJ-005-1, AC-INT-005-1
- **Tests:** TEST-PRJ-005, TEST-INT-005
- **Evidence:** EV-PRJ-005
- **Release Gates:** GATE-6

## T-070 — Build ServiceNow hourly ingestion with concurrent-run prevention

- [ ] Complete
- **Owner:** `INTENG`
- **Verifier:** `DATAENG`
- **Dependencies:** T-014, DEP-EXT-08
- **Requirements:** INT-006
- **Acceptance Criteria:** AC-INT-006-1, AC-INT-006-2, AC-INT-006-3
- **Tests:** TEST-INT-006
- **Evidence:** EV-INT-006
- **Release Gates:** GATE-6

## T-071 — Implement Salesforce stage-domain quarantine and unlinked opportunity reporting

- [ ] Complete
- **Owner:** `INTENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-013, T-041
- **Requirements:** INT-004
- **Acceptance Criteria:** AC-INT-004-2, AC-INT-004-3
- **Tests:** TEST-INT-004
- **Evidence:** EV-INT-004
- **Release Gates:** GATE-6

## T-072 — Build Canvas weekly engagement ingestion with small-cell suppression

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-014, DEP-EXT-09
- **Requirements:** INT-007
- **Acceptance Criteria:** AC-INT-007-1, AC-INT-007-2, AC-INT-007-3
- **Tests:** TEST-INT-007
- **Evidence:** EV-INT-007
- **Release Gates:** GATE-6

## T-073 — Build the Entra ID delta sync of users and role group memberships

- [ ] Complete
- **Owner:** `INTENG`
- **Verifier:** `SECARCH`
- **Dependencies:** T-034
- **Requirements:** INT-009
- **Acceptance Criteria:** AC-INT-009-1
- **Tests:** TEST-INT-009
- **Evidence:** EV-INT-009
- **Release Gates:** GATE-6

## T-074 — Implement orphan role revocation and session termination on account disable

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `QALEAD`
- **Dependencies:** T-073
- **Requirements:** INT-009
- **Acceptance Criteria:** AC-INT-009-2, AC-INT-009-3
- **Tests:** TEST-INT-009
- **Evidence:** EV-INT-009
- **Release Gates:** GATE-6

## T-075 — Implement the contract dual-run and deprecation workflow

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-016
- **Requirements:** INT-011
- **Acceptance Criteria:** AC-INT-011-3
- **Tests:** TEST-INT-011
- **Evidence:** EV-INT-011
- **Release Gates:** GATE-6

## T-076 — Implement monthly financial reconciliation against the Workday ledger

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-027
- **Requirements:** DQA-003, INT-001
- **Acceptance Criteria:** AC-DQA-003-1, AC-INT-001-3
- **Tests:** TEST-DQA-003, TEST-INT-001
- **Evidence:** EV-DQA-003, EV-INT-001
- **Release Gates:** GATE-6

## T-077 — Implement the remaining registered reconciliations with tolerance-based blocking

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `DATAGOV`
- **Dependencies:** T-076
- **Requirements:** DQA-003, INT-003
- **Acceptance Criteria:** AC-DQA-003-2, AC-DQA-003-3, AC-INT-003-3
- **Tests:** TEST-DQA-003, TEST-INT-003
- **Evidence:** EV-DQA-003, EV-INT-003
- **Release Gates:** GATE-6

## T-078 — Implement ownership-violation rejection and logging for source-owned fields

- [ ] Complete
- **Owner:** `DATAENG`
- **Verifier:** `SECARCH`
- **Dependencies:** T-020, T-068
- **Requirements:** INT-001, PRJ-001
- **Acceptance Criteria:** AC-INT-001-4, AC-PRJ-001-4
- **Tests:** TEST-INT-001, TEST-PRJ-001
- **Evidence:** EV-INT-001
- **Release Gates:** GATE-6

## T-079 — Operate 14 consecutive successful scheduled run days and evidence stability

- [ ] Complete
- **Owner:** `INTENG`
- **Verifier:** `DATAENG`
- **Dependencies:** T-067, T-070, T-072, T-073, T-075
- **Requirements:** INT-006, INT-010
- **Acceptance Criteria:** AC-INT-006-1, AC-INT-010-1
- **Tests:** TEST-INT-006, TEST-INT-010
- **Evidence:** EV-INT-006, EV-INT-010
- **Release Gates:** GATE-6

## T-080 — Re-verify row-level scoping against live integrated data

- [ ] Complete
- **Owner:** `SECARCH`
- **Verifier:** `QALEAD`
- **Dependencies:** T-036, T-079
- **Requirements:** SEC-003
- **Acceptance Criteria:** AC-SEC-003-1, AC-SEC-003-2, AC-SEC-003-3
- **Tests:** TEST-SEC-003
- **Evidence:** EV-SEC-003
- **Release Gates:** GATE-6
