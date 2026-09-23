# Dependency Catalog

Three kinds of dependency are tracked: external (outside the delivery team),
phase-level (between phases) and task-level (declared per task in `tasks/`).

## Rule

A task may depend only on tasks in the same or an earlier phase. A task
depending on an external dependency cannot start until that dependency's status
is **Available**.

## External dependencies

| ID | Dependency | Provider | Needed by | Status | Impact if late |
|---|---|---|---|---|---|
| DEP-EXT-01 | Entra ID app registration, 6 security groups created | OIT Identity Services | T-002, T-032 | Requested | Blocks GATE-0 and all of phase 03 |
| DEP-EXT-02 | Workday RaaS financial extract + SFTP drop | Controller's Office | T-010 | Requested | Blocks GATE-1; financial views unavailable |
| DEP-EXT-03 | Workday HCM position extract with restricted handling approval | GT Human Resources | T-011 | Requested | Blocks effort reporting; GATE-1 waiver needed |
| DEP-EXT-04 | IR warehouse conformed dimension views | Institutional Research | T-009 | Requested | Blocks referential integrity and all dependent feeds |
| DEP-EXT-05 | Banner enrollment aggregate view (path decision pending) | Registrar / IR | T-012 | **Open question** | Blocks INT-003; see proposal open question 2 |
| DEP-EXT-06 | Salesforce integration user + Bulk API access | Advancement IT | T-013 | Requested | Blocks pipeline reporting |
| DEP-EXT-07 | Smartsheet API token + webhook registration | CLL PMO | T-067 | Available | Blocks plan sync and write-back |
| DEP-EXT-08 | ServiceNow Table API read role | OIT Service Management | T-070 | Requested | Blocks demand/incident context |
| DEP-EXT-09 | Canvas Data 2 export subscription | CLL Learning Technology | T-072 | Requested | Blocks engagement KPIs |
| DEP-EXT-10 | Board SharePoint library with permissions | CLL Executive Office | T-087 | Requested | Blocks package distribution |
| DEP-EXT-11 | Institutional security review sign-off | CLL CIO delegate | T-007, T-043 | Scheduled | Blocks GATE-0 entry and GATE-3 closure |
| DEP-EXT-12 | Strategy 2035 pillar/objective taxonomy, published | Strategy Office | T-018 | Available | Blocks registry alignment |
| DEP-EXT-13 | Finance monthly close calendar FY2027–FY2028 | Controller's Office | T-081 | Available | Blocks reporting calendar |
| DEP-EXT-14 | Load test environment at production scale | `PLATFORM` / OIT | T-054, T-096 | Requested | Blocks NFR-001 verification |
| DEP-EXT-15 | Accessibility audit vendor engagement | CLL Procurement | T-055, T-097 | Requested | Blocks GATE-4 and GATE-8 |

## Phase dependencies

```
00 Foundation
   └─► 01 Source Alignment
          └─► 02 Core Platform
                 ├─► 03 Security & Quality
                 │      ├─► 04 Dashboard ──┐
                 │      └─► 06 Integrations │
                 └─► 05 Governance ─────────┼─► 07 Reporting & Operations
                                              └─► 08 Verification & Release
```

| Phase | Depends on | Reason |
|---|---|---|
| 01 | 00 | Needs environments, pipeline and contract templates |
| 02 | 01 | Portfolio model requires agreed contracts and conformed dimensions |
| 03 | 02 | Scoping predicates require the portfolio model and registry |
| 04 | 02, 03 | No user surface before access control is enforced |
| 05 | 02 | Gate decisions attach to registry projects |
| 06 | 03 | Remaining feeds carry scoped and restricted data |
| 07 | 04, 05, 06 | Package needs dashboard measures, governance narrative and live feeds |
| 08 | all | Verification spans the full baseline |

## Cross-capability dependencies

| Consumer | Depends on | Nature |
|---|---|---|
| `executive-dashboard` | `kpi-governance`, `project-registry`, `security` | Measures, records and scoping |
| `board-reporting` | `kpi-governance`, `data-quality`, `governance-workflow` | Certified snapshots, clean exceptions, approved narrative |
| `kpi-governance` | `integrations`, `data-quality` | Inputs and validated data |
| `governance-workflow` | `project-registry` | Gate decisions attach to projects |
| `data-quality` | `integrations` | Rules execute at the landing/conformed boundary |
| `security` | `integrations` (INT-009) | Roles derive from Entra ID groups |
| `verification` | all | Coverage spans every requirement |
| `release-governance` | `verification` | Gates close on evidence |

## Critical path

DEP-EXT-01 → T-002 → T-009 → T-018 → T-032 → T-044 → T-081 → T-092 → T-101.
Any slip on Entra ID provisioning or IR dimension views moves the go-live date
one-for-one.
