# Decision Record: Security and Identity

**ID:** DR-SEC-001
**Status:** Accepted
**Date:** 2026-09-23
**Deciders:** Security Architect (owner), CLL CIO delegate, Data Governance Lead, PMO Director
**Governs requirements:** SEC-001 – SEC-007, plus SEC-003 scoping used by EXD-003, BRD-005, INT-009
**Gate:** must be Accepted and implemented before GATE-3 closes

## Context

The platform concentrates data that is individually low-sensitivity but jointly
sensitive: project financials, position-level effort, student enrollment
aggregates, partner pipeline and leadership commentary. Concentration raises the
classification of the whole above that of any single feed. Institutional policy
requires central identity, least privilege and auditable access for any system
holding Workday HCM or Banner-derived data.

## Decisions

### DR-SEC-001.1 — Identity is federated to Entra ID only

Authentication is OIDC against Georgia Tech Entra ID. The platform stores **no**
passwords and implements **no** local credential flow. Service-to-service access
uses workload identities, not shared accounts.

- Session lifetime: 8 hours absolute, 60 minutes idle.
- MFA is enforced by the tenant conditional access policy, not by the platform.
- Break-glass: one tenant-managed emergency account, quarterly tested, alerting
  on every use. It is a tenant control, not a platform local account.

**Rejected:** local accounts for external partners — partners are sponsored as
guest identities in Entra ID instead, keeping one identity plane.

### DR-SEC-001.2 — Six roles, group-driven, no per-user grants

Role membership is derived from Entra ID security groups synchronized by
INT-009. The platform never grants a role directly to a user.

| Role | Purpose | Data reach | Group |
|---|---|---|---|
| `portfolio-admin` | Platform administration, registry configuration | All portfolios, all fields | `CLL-PMO-Platform-Admins` |
| `pmo-staff` | Day-to-day portfolio operations | All portfolios, write to registry/RAID | `CLL-PMO-Staff` |
| `pillar-owner` | Owns one or more Strategy 2035 pillars | Scoped to owned pillars, write to own projects | `CLL-Strategy-Pillar-Owners` |
| `project-manager` | Runs individual projects | Scoped to assigned projects | `CLL-PMO-Project-Managers` |
| `executive-viewer` | Leadership and Board readers | All portfolios, read-only, aggregate + drill-down | `CLL-Leadership-Viewers` |
| `data-steward` | KPI definitions, DQ rules, reconciliation | All data, write to governance metadata | `CLL-Data-Stewards` |

Administrative roles (`portfolio-admin`, `data-steward`) are mutually
recertified by a different approver than the requester (see DR-SEC-001.6).

### DR-SEC-001.3 — Row-level scoping enforced in the data layer

Every query carries a scoping predicate derived from the caller's role and
assignment set, applied at the query boundary (see design decision D4). The
dashboard, the API and export jobs all traverse the same enforcement point.

- `executive-viewer` and `pmo-staff` scope = all Strategy 2035 projects.
- `pillar-owner` scope = projects whose `pillar_id` is in their owned set.
- `project-manager` scope = projects where they are assigned owner or manager.
- Position-level HCM effort (INT-002) is visible **only** to `portfolio-admin`
  and `data-steward`; all other roles see effort aggregated to project level
  with a minimum cell size of 5 positions.
- Denied rows are excluded, never masked in place, so counts remain consistent
  with the caller's scope.

### DR-SEC-001.4 — Encryption

- In transit: TLS 1.2 minimum, TLS 1.3 preferred; HSTS enabled; no plaintext
  internal hops, including to the landing zone.
- At rest: AES-256 on all zones, snapshots and backups, using platform-managed
  keys in the institutional key vault.
- Landing-zone payloads containing HCM or Banner data are additionally encrypted
  with a separate key whose access is limited to the ingestion workload
  identity.

### DR-SEC-001.5 — Audit logging

A tamper-evident, append-only audit log records: authentication events, role
resolution, privileged actions, registry and KPI definition changes, gate
decisions, snapshot creation, export and distribution events, and every access
to position-level HCM data.

- Each entry: timestamp (UTC), actor, actor role set, action, target entity and
  id, source IP, request id, outcome.
- Retention: 7 years, matching snapshot retention (NFR-006).
- The audit log is write-only to the application identity; no application role
  can delete or amend entries.

### DR-SEC-001.6 — Secrets and key management

All credentials, tokens and connection strings live in the institutional secrets
manager. No secret is stored in the repository, in configuration files, in
environment files committed to source control, or in task/evidence artifacts.

- Integration credentials rotate every 90 days; rotation is automated and
  alerting fires at 75 days if unrotated.
- Encryption keys rotate annually with re-wrap, not re-encrypt-in-place.
- CI enforces secret scanning; a detected secret fails the build and triggers
  rotation of the exposed credential regardless of whether it reached `main`.

### DR-SEC-001.7 — Access recertification and offboarding

- Every role group is recertified quarterly by the role's accountable owner;
  uncertified members are removed at the end of the certification window.
- Offboarding is driven by Entra ID: loss of group membership removes platform
  access at next token refresh, and no later than 60 minutes.
- Emergency revocation path: disabling the Entra ID account terminates active
  sessions within 15 minutes via token revocation check.
- Recertification evidence is retained as EV-SEC-007.

## Consequences

- The platform cannot be demonstrated to users outside the tenant without
  sponsored guest identities; demo planning must account for this.
- Aggregation floors on HCM effort mean some project-level effort figures are
  suppressed; EXD-005 must render suppression explicitly rather than as zero.
- Quarterly recertification is real operational load on pillar owners; it is
  scheduled against the governance calendar in GOV-005.

## Open items

- Confirm whether Board members are sponsored guests or receive distributed
  exports only (affects SEC-002 role assignment and BRD-005 distribution).
