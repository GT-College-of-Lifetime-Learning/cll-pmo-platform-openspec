# Capability: governance-workflow — delta spec

Change: `implement-cll-pmo-platform-v1`
Requirements: GOV-001 – GOV-006 (6) · Acceptance criteria: 19
Approval sequences: `registries/approval-sequences.md`

## ADDED Requirements

### Requirement: GOV-001 — Stage-gate approval workflow

The platform SHALL implement the stage gates G0 Concept, G1 Charter, G2 Plan,
G3 Build Readiness, G4 Launch and G5 Benefits Realisation, SHALL require the
registered evidence set at each gate, and SHALL record an immutable gate
decision.

Acceptance criteria:
- AC-GOV-001-1: Each gate defines required evidence, and a gate cannot be submitted while required evidence is missing.
- AC-GOV-001-2: A gate decision records outcome (approved, approved with conditions, deferred, rejected), approver, timestamp, conditions and evidence references.
- AC-GOV-001-3: Gate decisions are immutable once recorded; a reversal is a new decision that references the prior one.
- AC-GOV-001-4: Project lifecycle transitions requiring a gate are blocked until the corresponding decision exists.

#### Scenario: Gate submitted without evidence
- **GIVEN** G2 Plan requires a baselined schedule and a funding confirmation, and the funding confirmation is absent
- **WHEN** the project manager submits the gate
- **THEN** submission is refused, naming the missing evidence, and no decision record is created

### Requirement: GOV-002 — Approval sequences and delegation

The platform SHALL enforce the ordered approval sequence registered for each
gate and decision type, SHALL support time-bounded delegation to a named
alternate, and MUST NOT allow an approver to approve their own submission.

Acceptance criteria:
- AC-GOV-002-1: Approvals are collected in the registered order; a later approver cannot act before an earlier one.
- AC-GOV-002-2: Delegation is explicit, time-bounded, recorded with the delegating approver's identity, and visible on the decision record.
- AC-GOV-002-3: Self-approval is rejected, including via delegation chains that resolve back to the submitter.

#### Scenario: Delegate approves during absence
- **GIVEN** the PMO Director delegates G3 approvals to the Portfolio Manager from 2027-05-01 to 2027-05-14
- **WHEN** the Portfolio Manager approves a G3 gate on 2027-05-07
- **THEN** the decision records the Portfolio Manager as acting delegate for the PMO Director with the delegation window attached

### Requirement: GOV-003 — Change request intake and disposition

The platform SHALL accept change requests against scope, schedule, budget or
benefits, SHALL route them by materiality thresholds, and SHALL record
disposition with rationale.

Acceptance criteria:
- AC-GOV-003-1: A change request records requester, type, description, quantified impact and requested decision date.
- AC-GOV-003-2: Requests exceeding the materiality thresholds (>10% budget, >30 days schedule, or any benefit reduction) route to the Executive Steering Committee; others route to the PMO Director.
- AC-GOV-003-3: Disposition records outcome, rationale, approver and resulting baseline changes.

#### Scenario: Material budget increase
- **GIVEN** a change request adding $180,000 to a $1,200,000 project budget (15%)
- **WHEN** the request is submitted
- **THEN** it routes to the Executive Steering Committee rather than the PMO Director, and the routing rule applied is recorded

### Requirement: GOV-004 — Escalation and SLA management

The platform SHALL apply service levels to governance items by severity, SHALL
escalate automatically when a service level is breached, and SHALL retain the
escalation trail.

Acceptance criteria:
- AC-GOV-004-1: Each governance item type and severity carries a response service level in business days.
- AC-GOV-004-2: Breach of a service level escalates to the next level in the registered sequence and notifies both parties.
- AC-GOV-004-3: The escalation trail records each step with timestamp, from-party and to-party, and is retained with the item.

#### Scenario: High-severity issue unattended
- **GIVEN** a high-severity issue with a 3 business-day response service level and no response after 4 business days
- **WHEN** the escalation check runs
- **THEN** the issue escalates to the pillar owner, both the original owner and the pillar owner are notified, and the step is recorded

### Requirement: GOV-005 — Meeting agenda and action item tracking

The platform SHALL generate governance meeting agendas from open gates,
escalations and change requests, and SHALL track action items to closure with
owner and due date.

Acceptance criteria:
- AC-GOV-005-1: An agenda for a scheduled governance meeting is generated from open gate submissions, escalated items and pending change requests.
- AC-GOV-005-2: Action items record owner, due date, source meeting and status, and remain open until explicitly closed.
- AC-GOV-005-3: Overdue action items appear on the next agenda automatically.

#### Scenario: Carried-over action
- **GIVEN** an action item due 2027-05-10 that is still open on 2027-05-20
- **WHEN** the agenda for the 2027-05-21 meeting is generated
- **THEN** the overdue action appears in a carried-over section with its age and owner

### Requirement: GOV-006 — Governance decision record retention

The platform SHALL retain every governance decision — gate decisions, change
request dispositions and escalation outcomes — for 7 years, with the evidence
reviewed attached, and SHALL make them exportable for audit.

Acceptance criteria:
- AC-GOV-006-1: Decisions are retained for 7 years with approver, date, rationale and references to the evidence reviewed.
- AC-GOV-006-2: Decisions are exportable as a dated register filtered by project, gate, period or approver.
- AC-GOV-006-3: No role can delete a decision record; superseding decisions reference the prior record.

#### Scenario: Audit request for a fiscal year
- **GIVEN** an internal audit covering FY2027 governance decisions
- **WHEN** the PMO exports the decision register for that fiscal year
- **THEN** every decision is returned with approver, date, rationale and evidence references, with no gaps in sequence
