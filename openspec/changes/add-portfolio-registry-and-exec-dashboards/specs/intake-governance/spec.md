# Delta for Intake and Governance

## Purpose
One transparent path from idea to decision for new Tier 1 and Tier 2 work, with decision
rights matched to tier and a permanent record of every decision.

## ADDED Requirements

### Requirement: Single intake channel
The system SHALL accept new project requests through one standard request form, assign each request an identifier, and confirm receipt to the requester.

#### Scenario: Request submitted
- GIVEN a staff member with a new project idea
- WHEN they submit the request form
- THEN a request record is created with an identifier in the form `REQ-<YY>-<NNNN>`
- AND the requester and the triage owner are notified

### Requirement: Triage
The system SHALL route each request to a Strategic Operations triage owner who confirms its tier, completeness, and alignment — a data check, not a merit decision — and either advances it or returns it as Needs Information; triage SHOULD complete within 5 business days.

#### Scenario: Incomplete request
- GIVEN a request with no effort estimate
- WHEN the triage owner reviews it
- THEN its status becomes Needs Information
- AND the requester is told exactly what is missing

#### Scenario: Multi-unit request stamped Tier 1 at submission
- GIVEN a request submitted by one unit that declares two contributing units
- WHEN the request record is created
- THEN it is classified Tier 1 and routed to the TCC
- AND the contributing units are recorded on the request

#### Scenario: Request reclassified to Tier 1
- GIVEN a request submitted as Tier 2 that involves two CLL units
- WHEN the triage owner reviews it
- THEN it is reclassified as Tier 1 and routed to the TCC
- AND the requester and their unit head are notified of the change

#### Scenario: Triage overdue
- GIVEN a request untouched by triage for 5 business days
- WHEN the daily check runs
- THEN the triage owner and the portfolio analyst are notified

### Requirement: Standard scoring
The system SHALL score Tier 1 requests against a published rubric covering strategic alignment, expected value, urgency or compliance need, capacity, effort, and risk, and SHALL store component scores with the request.

#### Scenario: Side-by-side comparison
- GIVEN five Tier 1 requests awaiting decision
- WHEN the TCC reviews them
- THEN they are listed with total and component scores side by side

#### Scenario: Compliance-mandated request
- GIVEN a request categorized as Compliance with justification
- WHEN it is triaged
- THEN it is marked "Must do" without scoring
- AND a decision is still recorded

### Requirement: Tiered decision rights
The system SHALL route Tier 2 requests to the lead unit's head and Tier 1 requests to the TCC for decision, SHALL give the TCC a call-up right over each Tier 2 approval for 10 business days, and SHALL allow escalation to the Dean.

#### Scenario: Tier 2 approved by unit head
- GIVEN a triaged Tier 2 request
- WHEN the unit head approves it
- THEN it becomes Approved without waiting for TCC review
- AND it appears in the TCC's list of Tier 2 approvals open for call-up

#### Scenario: TCC calls up a Tier 2 approval
- GIVEN a Tier 2 project approved by its unit head four business days ago
- WHEN a TCC member calls it up
- THEN it remains Approved but cannot move to Active until the TCC records a decision
- AND it is added to the next TCC meeting agenda

#### Scenario: Call-up window closes
- GIVEN a Tier 2 approval that no TCC member called up
- WHEN 10 business days have passed since approval
- THEN the approval is final and leaves the call-up list

#### Scenario: Unit head decision overdue
- GIVEN a Tier 2 request awaiting its unit head's decision
- WHEN 5 business days pass without a decision
- THEN the unit head is reminded
- AND at 10 business days Strategic Operations is notified

#### Scenario: Tier 1 deferred
- GIVEN a Tier 1 request reviewed by the TCC
- WHEN the TCC defers it
- THEN its status becomes Deferred with a revisit date
- AND the requester is notified with the rationale

### Requirement: Decision log
The system SHALL record every intake and portfolio decision with date, deciding body, subject, decision, rationale, and conditions, and SHALL NOT allow recorded decisions to be edited or deleted except by appending a correction.

#### Scenario: Correction appended
- GIVEN a recorded decision with an error in its conditions
- WHEN the portfolio analyst corrects it
- THEN a correction entry referencing the original is appended
- AND the original remains visible

### Requirement: Approval creates a registry item
The system SHALL create a registry item automatically when a request is approved, carrying forward request data and linking both records.

#### Scenario: Approved request becomes a project
- GIVEN a request approved by its decision body
- WHEN the approval is recorded
- THEN a project record is created in the Approved stage with its own identifier
- AND the request and project reference each other

### Requirement: Requester visibility
The system SHALL let requesters see the current stage of their requests and the rationale for any decision.

#### Scenario: Requester checks status
- GIVEN a requester with two open requests
- WHEN they open the request status view
- THEN they see each request's stage, triage owner, and any decision rationale
