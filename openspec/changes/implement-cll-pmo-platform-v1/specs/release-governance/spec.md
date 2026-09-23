# Capability: release-governance — delta spec

Change: `implement-cll-pmo-platform-v1`
Requirements: REL-001 – REL-002 (2) · Acceptance criteria: 6
Gate registry: `registries/release-gates.md`

## ADDED Requirements

### Requirement: REL-001 — Release gate criteria and approval

The platform's delivery SHALL be governed by the nine release gates GATE-0
through GATE-8, each with registered entry criteria, required evidence and named
approvers, and a gate MUST NOT close while any task or acceptance criterion in
its scope is incomplete, uncovered or failing.

Acceptance criteria:
- AC-REL-001-1: Each gate registers its entry criteria, required evidence, approvers and the task range and requirements in its scope.
- AC-REL-001-2: Gate closure is refused while any in-scope task is incomplete or any in-scope acceptance criterion is uncovered, unevidenced or failing.
- AC-REL-001-3: Closing a gate with a known deficiency requires a recorded waiver naming the deficiency, the compensating control, the approver and an expiry date.

#### Scenario: Schedule pressure at a gate
- **GIVEN** GATE-6 has 2 incomplete tasks and the Board date is approaching
- **WHEN** the Release Manager attempts closure
- **THEN** closure is refused unless a waiver is recorded with compensating control, approver and expiry; no silent closure is possible

### Requirement: REL-002 — Deployment, rollback and change freeze

The platform SHALL deploy to production only through the automated pipeline from
a tagged commit, SHALL provide a tested rollback for every release, and SHALL
observe a change freeze from snapshot certification until board package
publication.

Acceptance criteria:
- AC-REL-002-1: Every production release is traceable to a tagged commit, a release record and an approving Release Manager.
- AC-REL-002-2: Every release has a rehearsed rollback path that restores the prior version within 60 minutes without data loss for committed transactions.
- AC-REL-002-3: Deployments affecting reporting are blocked during the change freeze window unless an emergency approval is recorded.

#### Scenario: Deployment attempt during freeze
- **GIVEN** the FY2027-Q3 snapshot is certified and the package is not yet published
- **WHEN** a routine deployment affecting KPI computation is triggered
- **THEN** the pipeline blocks the deployment, citing the freeze window, until the package is published or an emergency approval is recorded
