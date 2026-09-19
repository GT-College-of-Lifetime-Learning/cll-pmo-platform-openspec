# Design: CLL Strategic Portfolio Management — Phase 1

## Context

Bill asked to expedite a college-wide "project to manage all projects." The starting point
was a Copilot-generated map of management layers to Microsoft 365 tools. This design keeps
that toolset, adds the data spine the map was missing, reorders the build so leadership
sees value first, and insulates the core from Microsoft product churn.

**Goals**
- One source of truth for what CLL is working on, who owns it, and why
- Dean overview on real data fast (target ≈ 60 days)
- Minimal new licensing and minimal burden on unit leads
- Everything rebuildable from source control

**Non-Goals (Phase 1)**
- Task scheduling, dependencies, critical path
- Person-level capacity planning
- Financial system integration
- Replacing any unit's existing tools

## Copilot map → revised map

| Layer | Copilot suggested | Phase 1 (this change) | Phase 2+ |
|---|---|---|---|
| Strategy & KPIs | Power BI Scorecards | Priorities + KPI lists → Power BI semantic model; Scorecards optional for manual check-ins | Automated KPI feeds |
| Portfolio | Planner Premium Portfolios | Registry + Power BI portfolio pages | Planner Portfolios as a PM-level roadmap view (Plan 3/5) |
| Program | Planner Premium | Registry (Program level) | Planner Premium for Tier 1 programs |
| Project | Planner Premium / Project | Registry + the unit's existing tool (linked) | Planner Premium as Tier 1 standard |
| Executive reporting | Power BI | Power BI (PBIP) with row-level security, published as an app | + Planner premium data |
| Documentation | SharePoint | SharePoint with charter / risk log / closeout templates | Same |
| Collaboration | Teams | Teams channel per Tier 1 project | Same |
| Intake & governance | Forms + Power Automate | Forms + Power Automate + Approvals + decision log | Power Apps if Forms limits bite |
| **Resource management** | **(not assigned)** | Lead unit, contributing units, effort estimate per item | Allocation model or Planner resource features |
| **Data spine** | **(not assigned)** | **SharePoint registry lists with stable IDs** | Evaluate Dataverse |

What Copilot got right: the layer model, Power BI as the executive surface, and Forms +
Power Automate for intake. What it missed: the spine, resource management, and sequencing.

## Decisions

### D1. The registry is the system of record, on SharePoint lists
- **Why:** standard M365 capability, no premium connectors, fast to stand up, native Power BI
  source, hand-editable during the pilot.
- **Why not Planner Portfolios as the spine:** creation needs Plan 3/5, only premium plans can
  be added, and there is no priority or KPI layer.
- **Why not Dataverse now:** better relational integrity, but its Power Automate connector is
  premium, and CLL is building in the default environment (D12).
- **Fallback / revisit trigger:** move to Dataverse when Phase 2 integrates Planner premium
  data (which already lives in Dataverse) or when relational enforcement becomes painful.

### D2. Report on projects; don't manage tasks (yet)
Executive dashboards need project-level facts — status, milestones, decisions, alignment —
not task lists. Phase 1 standardizes those facts and leaves execution where it is. This
removes the biggest adoption fight from the critical path.

### D3. Tiered registration (thresholds accepted 2026-09-19)

| Tier | Criteria (any one qualifies) | Intake decision | Status cadence | Workspace |
|---|---|---|---|---|
| **1 — Strategic** | Involves ≥ 2 CLL units · external partner or client commitment · est. cost ≥ $25K · est. effort ≥ 400 staff hours · named Strategy 2035 deliverable | TCC | Monthly; biweekly if TCC sets it | Auto-provisioned |
| **2 — Unit** | Not Tier 1, and effort ≥ 80 staff hours · or duration ≥ 6 weeks · or a new program/service launch | Unit head; TCC may call up (D11) | Monthly | On request |
| **Operational** | Below Tier 2 | Not registered | — | — |

Compliance-mandated work (e.g., SEVIS/F-1 changes) is registered by tier as usual and
categorized Compliance; it bypasses scoring ("must do") but still gets a logged decision.

**Scoring rubric (Tier 1, proposed):** each 1–5 — Strategic alignment (25%), Expected value
(25%), Urgency / compliance need (15%), Capacity available (15%), Effort (10%, inverse),
Risk (10%, inverse). Scores inform; TCC decides. TCC calibrates weights on its first batch.

### D4. Priorities and KPIs live in the semantic model, not in Scorecard hierarchies
Power BI Scorecard hierarchies and heatmap view were removed on 2026-04-15, so cascading
by unit is done with model relationships and filters. Scorecards MAY still be used as a
presentation layer for manually tracked goals, but nothing depends on them.

### D5. Status is an append-only fact table
One row per item per period in `StatusUpdates`. "Current status" is the latest row, computed
in the model. This gives trend lines and an audit trail for free.

### D6. Forms for input, flows for logic, lists locked down
Leads submit through pre-filled Microsoft Forms links; flows validate and write to lists.
Only Strategic Operations and the service account edit lists directly. Everyone else reads
through dashboards — which also keeps raw lists from bypassing dashboard security.

### D7. Access control through Power BI row-level security, delivered as an app
Roles: **Executive** (all items) and **Unit** (own unit in full — including own-unit
Confidential items, see D13 — plus non-confidential Tier 1 college-wide), driven by a
`UnitAccess` list and `USERPRINCIPALNAME()`. RLS only applies to workspace Viewers, so
everyone except the build team consumes via a Power BI app.

### D8. Build as code
| Artifact | Source-controlled as |
|---|---|
| Site, lists, columns, indexes, views | PnP provisioning template or CLI for Microsoft 365 scripts |
| Flows | Power Platform solution (unpacked with `pac solution unpack`), env vars + connection references |
| Semantic model + report | Power BI Project (PBIP) with TMDL |
| Templates, rubric, RAG definitions, playbook | Markdown / Office files in `docs/` |

### D9. Service ownership
Flows run under a non-personal service account with at least two co-owners from Strategic
Operations. No flow is owned by an individual. **Fallback if OIT can't issue one before the
pilot:** build under a Strategic Operations staff account with a second co-owner, keep all
connections in connection references, and re-point them to the service account before
college-wide go-live.

### D10. Identifiers
`SP-##` priority · `PF-##` portfolio · `CLL-YY-NNNN` program/project · `KPI-###` ·
`REQ-YY-NNNN` request · `DEC-YY-NNNN` decision. Generated by a flow from a `Counters` list
with trigger concurrency set to 1 to prevent duplicates. Objectives use `SO-<goal>.<n>`.

### D11. Delegated Tier 2 approval with TCC call-up
Tier 2 decisions sit with the unit head, who owns the budget and staff. Three guardrails keep
that from becoming a blind spot:
1. **Strategic Operations triage is a data check, not a merit review** — tier, completeness,
   alignment — within 5 business days. If a request meets any Tier 1 criterion, triage
   reclassifies it and routes it to the TCC.
2. **TCC call-up.** Every Tier 2 approval appears in the TCC governance view for 10 business
   days. Any TCC member can call it up; a called-up item stays Approved but cannot become
   Active until the TCC records a decision at its next meeting. After 10 days the approval is final.
3. **Decision SLA.** Unit heads get a reminder at 5 business days; at 10, Strategic Operations
   is notified and follows up.

Why not Strategic Operations approval: it would add a second approver without adding
authority, and slow the path Bill wants shortened. Call-up gives the TCC oversight without
putting it in every decision.

### D12. Default Power Platform environment
Everything is built in the tenant's default environment, inside one unmanaged solution.
- **DLP:** confirm with OIT that the default-environment DLP policy keeps SharePoint, Microsoft
  Forms, Approvals, Teams, Office 365 Outlook, and Office 365 Users in the same data group;
  otherwise the flows cannot run.
- **Naming:** every flow, form, and connection reference is prefixed `CLL-SPM` so it is findable
  among everyone else's default-environment flows.
- **Single-environment testing:** site URLs and list IDs live in environment variables. After
  go-live, changes are made on a cloned flow pointed at a test list, verified, then applied to
  the live flow. Export and unpack the solution after every change (D8).
- **Revisit trigger:** move to a dedicated environment if Phase 2 brings in Dataverse or if
  flow count or change frequency makes single-environment testing risky.

### D13. Confidential items — own unit sees detail; others see masked counts
A Confidential item's details are visible to executive roles **and its own unit** (the unit
already knows about its own personnel/legal work; the flag exists to hide it from other units
and college-wide viewers). RLS on detail tables (WorkItems, StatusUpdates, Milestones) uses
`NOT(Confidential) OR LeadUnitId = own unit`, so rows outside a viewer's reach vanish from
detail visuals — which is correct for detail.

RLS-filtered rows also vanish from measures, so "counted in aggregate totals" (registry spec)
cannot be satisfied by the detail tables. It is satisfied by a refresh-time
**`ConfidentialCounts` snapshot**: per priority / unit / tier / stage / RAG / period — counts
only, no titles, no drillable identifiers, nothing that identifies an item. Because the
snapshot is non-identifying by construction, it can be permissive under RLS. Measures add it
to totals; visuals show "+N Confidential" where masked items exist. This is the only pattern
that counts what RLS hides — a row cannot be both filtered and counted in the same table.

- **Why a snapshot and not measure-level security:** MLS still hides rows but cannot
  selectively un-hide counts; a non-identifying conformed table is simpler and portable.
- **Fallback / revisit trigger:** if Phase 2 moves the registry to Dataverse, revisit whether
  native row-level permissions make the snapshot unnecessary.

### D14. Multi-unit requests captured at intake
Tier classification ("involves ≥ 2 CLL units → Tier 1 regardless of size") is unanswerable
unless the request records which units are involved. The request form asks "which other CLL
units are involved?" (optional multi-select); F1 stamps `ContributingUnitIds` on the request;
triage confirms it during the 5-business-day data check; F2 carries it forward to the created
WorkItem. A request that declares contributing units is stamped Tier 1 at submission and
routes to the TCC directly; triage reclassification remains the fallback for requests that
miss it.

## Data model (SharePoint lists)

| List | Purpose | Key fields |
|---|---|---|
| `Units` | Reference | UnitId, Name, Head, Active |
| `UnitAccess` | Drives RLS | UserUPN, UnitId, Role (Unit / Executive) |
| `StrategicPriorities` | Strategy 2035 goals | PriorityId, Title, Description, ExecOwner, EffectiveFrom/To, Provisional, Source |
| `StrategicObjectives` | Objectives under each goal | ObjectiveId, PriorityId, Title, Provisional |
| `KPIs` | KPI definitions | KpiId, Name, Definition, PriorityId, ObjectiveId, UnitId (opt.), Owner, UoM, Direction, Baseline, Target, TargetDate, Frequency, Source, Method |
| `KpiValues` | KPI facts | KpiId, PeriodEnd, Value, Note, SubmittedBy |
| `Portfolios` | Grouping | PortfolioId, Title, PriorityId, Owner |
| `WorkItems` | Programs + projects | ItemId, Level, Title, ParentId, PortfolioId, PrimaryPriorityId, PrimaryObjectiveId, SecondaryPriorityIds, AlignmentCategory, AlignmentJustification, Tier, LeadUnitId, ContributingUnitIds, Sponsor, Lead, Stage, StageChangedOn/By, StartDate, TargetEndDate, BaselineEndDate, EffortEstimateHrs, CostEstimate, ExecutionTool, ExecutionLink, WorkspaceUrl, CharterUrl, KpiIds, Confidential, Backfilled, RequestId |
| `StatusUpdates` | Status facts | ItemId, PeriodEnd, OverallRAG, ScheduleRAG, ScopeRAG, ResourceRAG, Summary, PathToGreen, NextMilestone, NextMilestoneDate, PercentComplete, DecisionNeeded, DecisionAsk, SubmittedBy/On |
| `Milestones` | Executive milestones | ItemId, Title, BaselineDate, ForecastDate, ActualDate, IsExecutive |
| `IntakeRequests` | Pipeline | RequestId, Title, Requester, UnitId, ContributingUnitIds, Problem, ProposedPriorityId, EffortEst, CostEst, ExternalCommitment, Tier, Scores (6), TriageOwner, Status, RevisitDate, DecisionId, ItemId |
| `Decisions` | Append-only log | DecisionId, Date, Body, SubjectId, Decision, Rationale, Conditions, CorrectsDecisionId, RecordedBy |
| `Counters` | ID generation | Prefix, Year, Next |
| `ConfidentialCounts` | Masked aggregation (D13) | PriorityId, LeadUnitId, Tier, Stage, RAG, PeriodEnd, Count — no titles or identifiers |

Index `ItemId`, `PeriodEnd`, `LeadUnitId`, `Stage`, and `Status` columns. At ~300 active items
and monthly updates, `StatusUpdates` grows ~3,600 rows/year — fine for Power BI, but indexing
keeps list views under the 5,000-item view threshold.

## Automation (Power Automate, standard connectors only)

| Flow | Trigger | Does |
|---|---|---|
| F1 Intake | Form submitted | Create `REQ-` record, notify requester + triage owner |
| F2 Decision | Request set Ready for Review | Route by tier (Approvals), write `DEC-` record, on approve create `CLL-` item → F3; Tier 2 approvals open a 10-day TCC call-up window |
| F3 Workspace | Tier 1 approved / Tier 2 on request | Create Teams channel + library folder from template, write URLs back |
| F4 Status intake | Status form submitted | Validate (Red needs path/ask), append `StatusUpdates` row, update milestone forecast |
| F5 Reminders | Daily schedule | Pre-due reminder with pre-filled link, overdue reminder, unit-head escalation at +5 business days |
| F6 KPI reminders | Daily schedule | Remind owners of manual KPIs due / late |
| F7 Hygiene | Daily schedule | Flag unaligned items, backfilled items missing data after 30 days, triage > 5 days, unit-head decision > 5 / 10 days, close expired call-up windows |

## Dashboards (one semantic model, one report, Power BI app)

- **Dean Overview** — decisions needed (top), health by priority (G/A/R/Stale counts),
  executive milestones next 90 days, KPI progress vs. target, status currency %, effort split
  Strategic / Operational / Compliance. Phone layout.
- **Governance (TCC)** — intake pipeline by stage and age, requests awaiting decision with
  scores, recent decisions, cross-unit items.
- **Unit** — own items, "Action needed" (overdue, unaligned, stale), milestones.
- **Priority detail** — KPIs + aligned items for one priority, filterable by unit.
- **Item detail** (drill-through) — status history, milestones, KPIs, decisions, workspace link.
- Every page: last refresh timestamp. Status uses text/shape as well as color.

## Licensing summary

| Component | Phase 1 |
|---|---|
| SharePoint, Teams, Forms, Power Automate (standard), Approvals | Included in M365 |
| Power BI | Already licensed for all CLL staff — no new cost |
| Planner Plan 3/5 | Not needed until Phase 2 |
| Premium connectors (Dataverse, HTTP) | Avoided |

## Repository layout

```
cll-spm/
├── openspec/
├── sharepoint/        # PnP template or m365 CLI scripts; list schemas; seed CSVs
├── flows/             # unpacked Power Platform solution
├── powerbi/           # CLL-SPM.pbip, TMDL semantic model, report
└── docs/              # RAG definitions, scoring rubric, tier criteria, lead playbook, templates
```

## Microsoft platform notes (as of Sept 2026 — re-verify before build)

- Project Online is supported only through 2026-09-30.
- Planner portfolios: creating one requires Planner and Project Plan 3 or Plan 5; Plan 1 and
  standard M365 users can view shared portfolios read-only; only premium plans can be added.
- Power BI Scorecards remain supported, but hierarchies and heatmap view were removed
  2026-04-15; Metric Sets were retired in November 2025.
- Power BI Pro list price rose to $14/user/month in April 2025 (education pricing differs).

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Dashboards are only as good as updates | ≤ 15-minute update, pre-filled links, reminders, escalation, staleness shown publicly, Dean uses the dashboard in meetings |
| Leads see this as extra work | No tool migration in Phase 1; one monthly touch; value returned via unit view |
| Registry drowns in small work | Published tier thresholds; operational work not registered |
| Microsoft feature churn | Spine and model independent of Planner/Scorecard features (D1, D4) |
| Flow breaks when an owner leaves | Service account + co-owners (D9) |
| RLS bypass | App-only distribution; lists locked down (D6, D7) |
| Confidential personnel/legal work exposed | Confidential flag, item-level permissions, executive-only visibility |
| SharePoint as "database" limits | Indexing now; Dataverse revisit trigger defined (D1) |
| Scope creep into a full PMO methodology | Phase 1 is reporting-first; Phase 2 gated on adoption |

## Seed data (`sharepoint/seed/`)

All seed rows are flagged **Provisional**, sourced from the Strategy 2035 brochure (Jan 2026),
and shown as "Provisional" on dashboards until the Dean's office confirms.
- `units.csv` — known units; complete from the org chart before loading
- `strategic-priorities.csv` — the 5 Strategy 2035 goals (SP-01 to SP-05)
- `strategic-objectives.csv` — 25 objectives, short titles (SO-1.1 to SO-5.4)
- `kpis.csv` — 11 KPIs built from the plan's numeric targets; baselines and owners blank, so
  they display "Baseline pending" until filled
- `work-items-backfill.csv` — backfill template; row 1 is this project (`CLL-26-0001`, SO-5.3)

## Pilot (recommended)

| Unit | Why it's in the pilot |
|---|---|
| **Office of the Dean / central operations** | Owns most cross-unit Tier 1 work, so it exercises the TCC path, executive-role security, and the governance view. Hosts `CLL-26-0001`. |
| **GTPE** | High-volume delivery unit. Tests the Tier 2 path, unit-head approval, and whether the 15-minute update holds at scale. |
| **GTLI** | Small and well known to Strategic Operations, so backfill is fast and friction is easy to read. Its mix of closing work and new Language and Communications initiatives exercises lifecycle stages and intake. |

Not first wave: units with large seasonal or hourly staffing (e.g., CEISMC programs) — add
them in the college-wide drive once the unit view and reminders are proven.

## Rollout (targets)

| Weeks | Milestone |
|---|---|
| 0–2 | ✓ TCC role, tiers, licensing, seeding, Tier 2 rights, pilot units, environment settled. Remaining: pilot unit-head buy-in, goal owners, OIT requests |
| 2–5 | Registry, forms, flows, semantic model built; priorities seeded; pilot units backfilled |
| 5–8 | Pilot: one full reporting cycle with 2–3 units; Dean reviews live overview |
| 8–12 | College-wide registration drive; second cycle; go-live |

## Open questions
See the table in `proposal.md`.
