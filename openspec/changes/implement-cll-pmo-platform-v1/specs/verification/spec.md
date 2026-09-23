# Capability: verification — delta spec

Change: `implement-cll-pmo-platform-v1`
Requirements: VER-001 – VER-003 (3) · Acceptance criteria: 9
Catalogs: `registries/test-catalog.md`, `registries/evidence-catalog.md`

## ADDED Requirements

### Requirement: VER-001 — Test strategy and coverage

The platform SHALL verify every one of the 72 approved requirements through at
least one registered test, SHALL cover each of the 223 acceptance criteria by at
least one test case, and MUST NOT close a release gate with uncovered criteria
in its scope.

Acceptance criteria:
- AC-VER-001-1: Every requirement maps to at least one test in the test catalog, and every acceptance criterion maps to at least one test case.
- AC-VER-001-2: Test types are appropriate to the criterion: unit and integration for logic, contract tests for feeds, access tests for scoping, load tests for performance, audit for accessibility.
- AC-VER-001-3: A release gate cannot close while any acceptance criterion in its scope is uncovered or failing.

#### Scenario: Uncovered criterion at gate
- **GIVEN** GATE-4 scope includes AC-EXD-007-3 and no test case references it
- **WHEN** the Release Manager evaluates gate closure
- **THEN** closure is refused, naming the uncovered criterion, until a test case is registered and passing

### Requirement: VER-002 — Evidence capture and traceability

The platform SHALL retain, for every verified acceptance criterion, dated
evidence identifying the test executed, the executor, the result and the build
or environment, and SHALL produce a traceability matrix from requirement to
criterion to test to evidence to gate.

Acceptance criteria:
- AC-VER-002-1: Each evidence record identifies criterion, test id, executor, execution date, result, and build or environment reference.
- AC-VER-002-2: The traceability matrix is generable on demand and shows any break in the requirement-to-gate chain.
- AC-VER-002-3: Evidence is retained for 7 years and cannot be amended after a gate closes.

#### Scenario: Traceability gap detected
- **GIVEN** a test passes but no evidence record is attached
- **WHEN** the traceability matrix is generated
- **THEN** the criterion is reported as unevidenced, and it does not count toward gate closure

### Requirement: VER-003 — User acceptance testing and sign-off

The platform SHALL conduct user acceptance testing with named representatives of
each affected role before go-live, and SHALL require written sign-off from the
PMO Director and the capability's business owner.

Acceptance criteria:
- AC-VER-003-1: UAT covers each of the six roles with at least one named participant per role executing role-specific scenarios.
- AC-VER-003-2: UAT defects are triaged by severity; no severity-1 or severity-2 defect remains open at sign-off.
- AC-VER-003-3: Sign-off is recorded with signatory, role, date and the build tested.

#### Scenario: Severity-1 defect at sign-off
- **GIVEN** an open severity-1 defect where a pillar owner can view out-of-scope projects
- **WHEN** sign-off is requested
- **THEN** sign-off is refused, GATE-8 remains open, and the defect is escalated to the Security Architect
