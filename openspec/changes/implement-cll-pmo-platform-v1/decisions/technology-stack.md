# D8 — Technology stack: Microsoft/Azure with a React + TypeScript dashboard

**Status:** Accepted
**Date:** 2026-09-23
**Governs:** all implementation tasks T-001 – T-101; referenced from `design.md`
**Related:** `security-and-identity.md`, `synchronization-ownership.md`

## Context

`design.md` fixes the architecture — four zones (landing → conformed →
portfolio model → snapshot store), decisions D1 – D7, the entity grain table
and the nonfunctional posture — but names no language, framework, runtime,
database or cloud. No task in the 101-task backlog can be implemented until
that gap is closed: T-003 (CI/CD), T-004 (run records and telemetry) and
T-005 (watchdog alerting) all presuppose a runtime.

Two constraints are already approved and are not reopened here:

- Identity is Entra ID (SEC-001, SEC-002, dependency `DEP-EXT-01`), per
  `decisions/security-and-identity.md`.
- Access control is enforced in the data layer, not the presentation layer
  (D4), across three consumers: dashboard, API and export.

The institution is a Microsoft shop, and the board-facing distribution target
is SharePoint (source catalog, board package).

## Decision

The platform is built in the Microsoft/Azure ecosystem, with a React +
TypeScript single-page application for the dashboard.

| Design zone / concern | Component | Primary requirements |
|---|---|---|
| Landing zone (raw, immutable per run) | Azure Data Lake Storage Gen2 | NFR-006, DQA-006, INT-010 |
| Ingestion (batch, contract-validated, fail-closed) | Azure Data Factory | INT-001 – INT-011, D5 |
| Conformed zone and portfolio model | Azure SQL Database | PRJ-001 – PRJ-008, KPI-001 – KPI-003 |
| Snapshot store (labelled, immutable) | Azure SQL + ADLS Gen2 archive tier | BRD-003, BRD-006, KPI-006, D1 |
| Application and API | ASP.NET Core (.NET 8) Web API, C# | D2, D4 |
| Dashboard UI | React 18 + TypeScript SPA (Vite) | EXD-001 – EXD-008, NFR-001 |
| Authentication | Entra ID (OIDC); MSAL in the SPA, JWT bearer in the API | SEC-001 |
| Authorization | App roles from Entra ID groups + SQL row-level security | SEC-002, SEC-003, D4 |
| Run records, telemetry, alerting | Azure Monitor + Application Insights | NFR-004 |
| Secrets | Azure Key Vault, referenced by managed identity | SEC-005 |
| CI/CD, secret scanning, accessibility checks | GitHub Actions | NFR-007, SEC-006, NFR-005 |
| Board package distribution | SharePoint Online | BRD-005, BRD-007 |

### Why React rather than Blazor

The dashboard carries the hardest nonfunctional targets in the baseline —
first paint p95 ≤ 3.0 s and p99 ≤ 5.0 s at 150 concurrent users (NFR-001) and
WCAG 2.2 AA (NFR-005, EXD-008). React has the larger pool of audited,
accessible charting and data-grid components and the mature automated
accessibility tooling (axe) needed to make TEST-EXD-008 and TEST-NFR-005
routine rather than bespoke. Blazor Server would also put a persistent
connection in the first-paint path, which is the wrong risk to accept against
NFR-001.

### Row-level security placement

Scoping predicates (SEC-003) are implemented as SQL row-level security
policies on the portfolio model, not as query filters in the API. This is the
direct implementation of D4: all three consumers inherit scoping from one
enforcement point.

## Rejected alternatives

| Alternative | Why rejected |
|---|---|
| Power BI as the delivery surface, no custom application | Cannot capture gate decisions, RAID items or narrative — these originate in the platform (D2). Row-level institutional scoping would be duplicated in the semantic layer. Already rejected in `design.md` as "Warehouse-only". |
| Azure Synapse / Fabric warehouse as the portfolio model | The portfolio model is transactional as well as analytical — project state transitions (PRJ-002, PRJ-008), gate decisions (GOV-001) and RAID items are written by users. A warehouse engine is the wrong fit for write paths; the snapshot store already covers the analytical read pattern. |
| Blazor (Server or WebAssembly) for the dashboard | See above — accessibility tooling maturity and NFR-001 first-paint risk. |
| Non-Microsoft stack (e.g. Python/FastAPI + Postgres on AWS) | Contradicts approved identity (Entra ID, SEC-001/SEC-002) and the SharePoint board distribution target; adds a second cloud to an institution that already operates Azure. |
| Event-driven streaming ingestion | Already rejected in `design.md`: sources are batch-oriented. |
| Self-hosted runners / Azure DevOps Pipelines for CI | The repository is on GitHub; GitHub Actions keeps CI adjacent to the OpenSpec artifacts and gives native secret scanning for SEC-006. |

## Consequences

- Azure tenancy, subscription and landing-zone policy become a hard dependency
  of T-001 (`DEP-EXT-11`).
- The repository becomes polyglot: C# under `src/`, TypeScript under `web/`.
  CI must run both toolchains, and the accessibility check runs against the
  built SPA.
- Entra ID app registration (T-002) now has a concrete shape: one API app
  registration exposing scopes, one SPA registration with the six role groups
  mapped to app roles.
- Snapshot retention of 7 years and landing retention of 400 days (NFR-006)
  are implemented as ADLS Gen2 lifecycle policies, which must be captured as
  evidence `EV-NFR-006`, not as application code.

## Open items

- Azure region and subscription topology (dev/test/prod) — owner `PLATFORM`,
  resolved in T-001.
- Whether Azure SQL is provisioned as a single database or an elastic pool —
  deferred to T-018, sized against NFR-003 (500 projects, 250 KPIs, 5 years of
  monthly history).
