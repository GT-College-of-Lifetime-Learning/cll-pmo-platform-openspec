# Business-to-Engineering Phase Crosswalk

Maps Strategy 2035 business milestones to the nine engineering phases, their
release gates, task ranges and the requirements they satisfy. This is the
artifact the PMO uses to answer "what does the Board get, and when".

## Crosswalk

| Phase | Engineering outcome | Business milestone | Gate | Tasks | Primary requirements |
|---|---|---|---|---|---|
| 00 Foundation | Environments, repo, CI, data platform skeleton, contract templates | "We can build safely" — delivery capability stood up | GATE-0 | T-001 – T-008 (8) | REL-001, REL-002, NFR-004, NFR-007, VER-001 |
| 01 Source Alignment | Source contracts signed, landing zone ingesting all 11 sources | "We know what the data says" — source owners agreed | GATE-1 | T-009 – T-017 (9) | INT-001 – INT-004, INT-008, INT-010, INT-011, DQA-001 |
| 02 Core Platform | Portfolio model, project registry, KPI registry | "Every strategic project has one record" | GATE-2 | T-018 – T-031 (14) | PRJ-001 – PRJ-008, KPI-001 – KPI-003, NFR-003 |
| 03 Security & Quality | SSO, RBAC, row scoping, audit, DQ rules and scorecard | "Institutional data is safe and trusted" | GATE-3 | T-032 – T-043 (12) | SEC-001 – SEC-007, DQA-002 – DQA-006 |
| 04 Dashboard | Executive dashboard with drill-down, freshness, accessibility | "Leadership sees the portfolio without asking for a deck" | GATE-4 | T-044 – T-055 (12) | EXD-001 – EXD-008, NFR-001, NFR-005 |
| 05 Governance | Stage gates, approval sequences, change requests, escalation, decisions | "Decisions are made and retained in one place" | GATE-5 | T-056 – T-066 (11) | GOV-001 – GOV-006, KPI-005 – KPI-007 |
| 06 Integrations | Remaining source integrations live, write-back, versioning, backfill | "Numbers refresh themselves" | GATE-6 | T-067 – T-080 (14) | INT-005 – INT-007, INT-009 – INT-011, DQA-003, SEC-003 |
| 07 Reporting & Operations | Board package, snapshots, exports, distribution, run operations | "The Board package is produced from the platform" | GATE-7 | T-081 – T-091 (11) | BRD-001 – BRD-007, NFR-002, NFR-006 |
| 08 Verification & Release | Full traceability, UAT sign-off, performance and accessibility validation, go-live | "Strategy 2035 execution is demonstrably on the record" | GATE-8 | T-092 – T-101 (10) | VER-001 – VER-003, REL-001, REL-002, NFR-001, NFR-002 |

## Business milestone detail

### M1 — Delivery capability (GATE-0)
**Business owner:** PMO Director. **Question answered:** can we build this
without creating institutional risk? **Evidence:** environment inventory,
CI pipeline run, signed security intake.

### M2 — Source agreement (GATE-1)
**Business owner:** PMO Director with source system owners. **Question
answered:** do Finance, HR, Registrar, Advancement and IT agree on what the
platform may consume and how often? **Evidence:** eleven countersigned data
contracts.

### M3 — One record per project (GATE-2)
**Business owner:** PMO Portfolio Manager. **Question answered:** how many
Strategy 2035 projects are there, who owns each one, and what state is it in?
**Evidence:** registry reconciliation against the legacy Smartsheet inventory.

### M4 — Trustworthy and protected (GATE-3)
**Business owner:** Security Architect with Data Governance Lead. **Question
answered:** can a pillar owner see only their portfolio, and can we prove who
saw what? **Evidence:** access test matrix, audit log sample, DQ scorecard.

### M5 — Leadership self-service (GATE-4)
**Business owner:** CLL Leadership Team. **Question answered:** can a dean open
the dashboard and answer a question without an analyst? **Evidence:** UAT
session notes, performance run, accessibility audit.

### M6 — Decisions on the record (GATE-5)
**Business owner:** PMO Director. **Question answered:** who approved this gate,
on what date, reviewing what? **Evidence:** gate decision export.

### M7 — Self-refreshing portfolio (GATE-6)
**Business owner:** Data Engineering Lead. **Question answered:** does the
portfolio update without manual intervention, and do the numbers reconcile to
the source systems? **Evidence:** 14 consecutive successful scheduled runs,
reconciliation report.

### M8 — Board package from the platform (GATE-7)
**Business owner:** PMO Director with Strategy Office. **Question answered:**
can we produce the quarterly package from the platform and reproduce it later?
**Evidence:** shadow package reconciled to the manual package.

### M9 — Strategy 2035 on the record (GATE-8)
**Business owner:** PMO Director, Sponsor sign-off. **Question answered:** are
all 72 requirements verified with evidence? **Evidence:** traceability matrix,
UAT sign-off, gate closure record.

## Requirement coverage by phase

| Capability | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 |
|---|---|---|---|---|---|---|---|---|---|
| integrations | | ● | | | | | ● | | ○ |
| security | ○ | | | ● | | | ○ | ○ | ○ |
| executive-dashboard | | | | | ● | ○ | | ○ | ○ |
| project-registry | | | ● | ○ | ○ | ○ | ○ | | ○ |
| kpi-governance | | | ● | | ○ | ● | | ○ | ○ |
| governance-workflow | | | | | | ● | | ○ | ○ |
| data-quality | | ○ | | ● | | | ○ | ○ | ○ |
| board-reporting | | | | | | ○ | | ● | ○ |
| nonfunctional | ○ | | ○ | ○ | ○ | | ○ | ● | ● |
| verification | ○ | | | | | | | | ● |
| release-governance | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ● |

● primary delivery  ○ contributing work
