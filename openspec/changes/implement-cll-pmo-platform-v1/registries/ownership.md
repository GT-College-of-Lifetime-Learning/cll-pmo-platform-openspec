# Ownership Registry

Authoritative list of the roles referenced by every task's **Owner** and
**Verifier** fields. Tasks name roles, not individuals, so the registry stays
correct through staffing changes. The named holder is recorded here only.

## Delivery roles

| Role key | Role | Accountable for | May verify |
|---|---|---|---|
| `SPONSOR` | PMO Director | Change sponsorship, gate approval, board package approval | GATE-0 – GATE-8 |
| `PORTFOLIO` | PMO Portfolio Manager | Project registry content, project inventory reconciliation, governance operations | Registry, governance, reporting tasks |
| `PLATFORM` | PMO Platform Lead | Overall technical delivery, architecture conformance, environment strategy | Any engineering task |
| `APPENG` | Application Engineering Lead | Application services, APIs, registry and governance features | Application tasks |
| `DATAENG` | Data Engineering Lead | Ingestion, conformance, portfolio model, snapshots, reconciliation | Data tasks |
| `INTENG` | Integration Engineer | Source connectors, contract validation, scheduling, backfill | Integration tasks |
| `SECARCH` | Security Architect | Identity, RBAC, scoping, encryption, audit, secrets, recertification | Security tasks |
| `DATAGOV` | Data Governance Lead | Data quality rules, KPI definitions, stewardship, exception escalation | Quality and KPI tasks |
| `BILEAD` | BI / Reporting Lead | Dashboard, visualisations, board package assembly and exports | Dashboard and reporting tasks |
| `QALEAD` | QA Lead | Test strategy, coverage, traceability matrix, UAT coordination | Any task's evidence |
| `RELMGR` | Release Manager | Pipelines, releases, gate closure mechanics, rollback, change freeze | Release tasks |
| `STRATOFF` | Strategy Office Analyst | Strategy 2035 taxonomy, pillar/objective definitions, narrative coordination | Taxonomy and narrative tasks |
| `A11Y` | Accessibility Specialist | WCAG 2.2 AA conformance of UI and exports | Accessibility tasks |

## Verification rule

A task's **Verifier** is always a different role from its **Owner**. Evidence
signed only by the owning role does not satisfy VER-002.

## Capability ownership

| Capability | Accountable role | Business owner |
|---|---|---|
| `integrations` | `DATAENG` | PMO Director |
| `security` | `SECARCH` | CLL CIO delegate |
| `executive-dashboard` | `BILEAD` | CLL Leadership Team |
| `project-registry` | `APPENG` | PMO Portfolio Manager |
| `kpi-governance` | `DATAGOV` | Strategy Office |
| `governance-workflow` | `APPENG` | PMO Director |
| `data-quality` | `DATAGOV` | PMO Director |
| `board-reporting` | `BILEAD` | CLL Executive Office |
| `nonfunctional` | `PLATFORM` | PMO Platform Lead |
| `verification` | `QALEAD` | PMO Director |
| `release-governance` | `RELMGR` | PMO Director |

## On-call and escalation

| Concern | First responder | Escalates to |
|---|---|---|
| Failed ingestion run | `INTENG` | `DATAENG` |
| Blocking data quality exception | `DATAGOV` | PMO Director |
| Access or identity incident | `SECARCH` | CLL CIO delegate |
| Dashboard availability | `PLATFORM` | `RELMGR` |
| Reporting cycle blocker | `PORTFOLIO` | PMO Director |
