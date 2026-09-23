# Capability: security — delta spec

Change: `implement-cll-pmo-platform-v1`
Requirements: SEC-001 – SEC-007 (7) · Acceptance criteria: 22
Decision record: `decisions/security-and-identity.md` (DR-SEC-001)

## Purpose

Protect the institutional data the platform concentrates. Project financials,
position-level effort, enrollment aggregates and leadership commentary are each
modest on their own but jointly sensitive, so identity is federated to Entra ID,
access is role-based and row-scoped at the data layer, and every privileged read
is auditable seven years later.

## ADDED Requirements

### Requirement: SEC-001 — Federated authentication via Entra ID

The platform SHALL authenticate all human users through OIDC federation with
Georgia Tech Entra ID, MUST NOT store passwords or implement any local
credential flow, and SHALL use workload identities for service-to-service
access.

Acceptance criteria:
- AC-SEC-001-1: All interactive access is obtained through an Entra ID authorization code flow with PKCE; no local login form exists in any environment.
- AC-SEC-001-2: Sessions expire after 8 hours absolute and 60 minutes idle, whichever comes first.
- AC-SEC-001-3: No shared or service user accounts exist; integrations authenticate as workload identities.
- AC-SEC-001-4: Use of the tenant break-glass account raises an alert to the Security Architect within 5 minutes.

#### Scenario: Unauthenticated deep link
- **GIVEN** an anonymous user opens a direct link to a project detail page
- **WHEN** the request reaches the platform
- **THEN** the user is redirected to Entra ID, and after successful authentication is returned to the originally requested page with their scope applied

### Requirement: SEC-002 — Role-based access control

The platform SHALL implement exactly the six roles defined in DR-SEC-001.2,
SHALL derive role membership solely from Entra ID security groups, and MUST NOT
support direct per-user role grants.

Acceptance criteria:
- AC-SEC-002-1: The six roles `portfolio-admin`, `pmo-staff`, `pillar-owner`, `project-manager`, `executive-viewer` and `data-steward` are the only roles recognised.
- AC-SEC-002-2: A user with no mapped group membership receives an access-denied response and no portfolio data.
- AC-SEC-002-3: Every write action is authorised against the role's permitted action set, and denials are logged with actor, action and target.

#### Scenario: Viewer attempts a write
- **GIVEN** a user holding only `executive-viewer`
- **WHEN** they submit an edit to a project lifecycle state through the API
- **THEN** the request is denied with 403, no state change occurs, and the denial is recorded in the audit log

### Requirement: SEC-003 — Row-level data scoping

The platform SHALL apply a row-level scoping predicate derived from the caller's
role and assignment set at the data layer, such that the dashboard, the API and
export jobs all traverse the same enforcement point.

Acceptance criteria:
- AC-SEC-003-1: `pillar-owner` results contain only projects in their owned pillars; `project-manager` results contain only projects where they are the assigned owner or manager.
- AC-SEC-003-2: Out-of-scope rows are excluded rather than masked, so counts and aggregates are internally consistent with the caller's scope.
- AC-SEC-003-3: Identical queries issued through the dashboard, the API and an export produce identical scoped result sets for the same caller.

#### Scenario: Cross-pillar drill-down attempt
- **GIVEN** a `pillar-owner` for the Workforce pillar
- **WHEN** they request a project belonging to the Research pillar by direct id
- **THEN** the platform returns not-found rather than access-denied, avoiding disclosure of the record's existence, and logs the attempt

### Requirement: SEC-004 — Encryption in transit and at rest

The platform SHALL encrypt all data in transit with TLS 1.2 or higher and all
data at rest with AES-256, and SHALL protect landing-zone payloads containing
Workday HCM or Banner-derived data with a separate key restricted to the
ingestion workload identity.

Acceptance criteria:
- AC-SEC-004-1: All external and internal hops, including to the landing zone, negotiate TLS 1.2 minimum with HSTS enabled on public endpoints.
- AC-SEC-004-2: All zones, snapshots and backups are encrypted at rest with AES-256 using institutional key vault keys.
- AC-SEC-004-3: Restricted-source landing payloads are encrypted with a distinct key that no application role can read.

#### Scenario: Legacy client negotiation
- **GIVEN** a client offering only TLS 1.0
- **WHEN** it attempts to connect to the platform API
- **THEN** the handshake is refused and the rejection is logged with the offered protocol version

### Requirement: SEC-005 — Audit logging

The platform SHALL maintain a tamper-evident, append-only audit log of
authentication, role resolution, privileged actions, registry and KPI definition
changes, gate decisions, snapshot creation, exports and every access to
position-level HCM data, retained for 7 years.

Acceptance criteria:
- AC-SEC-005-1: Each entry records timestamp (UTC), actor, actor role set, action, target entity and id, source IP, request id and outcome.
- AC-SEC-005-2: No application role can delete or amend an audit entry; the application identity holds append-only permission.
- AC-SEC-005-3: Audit entries are retained for 7 years and are queryable by actor, target and date range.

#### Scenario: Reconstructing who saw restricted data
- **GIVEN** an inquiry about access to position-level effort in March 2027
- **WHEN** a Security Architect queries the audit log for that entity and date range
- **THEN** every read is returned with actor, role set and timestamp, with no gaps in the sequence

### Requirement: SEC-006 — Secrets and key management

The platform SHALL store all credentials, tokens and connection strings in the
institutional secrets manager, MUST NOT persist any secret in source control or
in change artifacts, and SHALL rotate integration credentials at least every 90
days.

Acceptance criteria:
- AC-SEC-006-1: No secret value appears in the repository, configuration files, task files or evidence artifacts; CI secret scanning fails the build on detection.
- AC-SEC-006-2: Integration credentials rotate automatically every 90 days, with an alert at 75 days if rotation has not occurred.
- AC-SEC-006-3: Encryption keys rotate annually by re-wrap, with the prior key retained only for decryption of existing material.

#### Scenario: Secret committed by mistake
- **GIVEN** a developer commits an API token in a configuration file
- **WHEN** the CI secret scan runs on the pull request
- **THEN** the build fails, the pull request is blocked, and the exposed credential is rotated regardless of whether it reached `main`

### Requirement: SEC-007 — Access recertification and offboarding

The platform SHALL support quarterly recertification of every role group by its
accountable owner, SHALL remove uncertified members at the close of the
certification window, and SHALL revoke access on loss of Entra ID group
membership within 60 minutes.

Acceptance criteria:
- AC-SEC-007-1: A quarterly recertification campaign lists every member of every role group with last-access date for the accountable owner's decision.
- AC-SEC-007-2: Members not certified by the window close are removed automatically and the removal is recorded.
- AC-SEC-007-3: Recertification outcomes are retained as evidence EV-SEC-007 for 7 years.

#### Scenario: Owner does not complete certification
- **GIVEN** the `CLL-Data-Stewards` group has 4 uncertified members at window close
- **WHEN** the certification window expires
- **THEN** the 4 members lose the `data-steward` role, the accountable owner is notified, and the removal is written to the audit log and the evidence record
