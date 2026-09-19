# Proposal: CLL Strategic Portfolio Management — Phase 1
### Registry, intake, status rhythm, and executive dashboards

**Sponsor:** Bill · **Owner:** Strategic Operations · **Audience:** Dean, TCC, unit leaders
**Decision this enables:** leadership can see, compare, and steer all significant CLL work
against Strategy 2035 without manual data calls.

## Why

CLL leadership has no single, current view of what work is underway, how it maps to
Strategy 2035, or where executive decisions are needed. Status lives in unit-specific tools,
email, and slide decks, so every leadership question triggers a manual data call. Bill has
asked to expedite a college-wide "project to manage all projects" with executive dashboards
and tracking.

Strategy 2035 already commits CLL to this. Goal 5 includes becoming data-informed, with
interactive dashboards across every strategic objective (objective SO-5.3 in the seed data).
This change is the first deliverable against that objective and is registered as the first
Tier 1 project, `CLL-26-0001`.

The starting point was a Copilot recommendation that maps each management layer to a
Microsoft tool (Power BI Scorecards, Planner Premium Portfolios, Planner Premium, Power BI,
SharePoint, Teams, Forms + Power Automate). That map is a sound toolset but not yet a system:

- **No shared data spine.** Nothing ties priority → portfolio → program → project → KPI
  together with common IDs and required fields, so dashboards cannot roll up reliably.
- **Resource management is in scope but has no tool assigned.** "Cross-functional resource
  management" is on the requirements list and missing from the tool map.
- **Execution tooling sits on the critical path to dashboards.** Moving every unit into
  Planner Premium before leadership sees anything is the slowest route. Creating Planner
  portfolios requires Plan 3 or Plan 5 licenses, and only premium plans can be added to them.
- **The Microsoft project/portfolio stack is mid-transition.** Project Online retires
  2026-09-30; Power BI Scorecard hierarchies (the cascading feature) were removed 2026-04-15.
  The design must not depend on any one SKU staying the same.

## What Changes

Phase 1 stands up the minimum system leadership needs, using capabilities already in
Georgia Tech's Microsoft 365 tenant:

- A **portfolio registry** as the system of record for priorities, portfolios, programs, and
  projects — stable IDs, tiers, lifecycle stages, required data.
- **Strategic alignment**: every registered item tied to a Strategy 2035 priority or explicitly
  categorized as Operational/Compliance; KPIs defined with owners, baselines, and targets.
- **Intake and governance**: one request form, triage, a scoring rubric, tiered decision
  rights, and a permanent decision log.
- **Status reporting**: a monthly rhythm, standard RAG definitions, pre-filled update links,
  reminders, escalation, and visible staleness.
- **Executive dashboards**: Dean, governance (TCC), and unit views with role-based access,
  drill-through, freshness stamps, and meeting-ready export.
- **Project workspaces**: provisioned on approval with charter, risk log, and closeout templates.

**Units keep their current task tools in Phase 1.** They report into the registry; they do
not migrate execution. That is what makes the timeline short.

## Capabilities

### New Capabilities
- `portfolio-registry` — hierarchy, identifiers, tiers, lifecycle, required data, backfill
- `strategic-alignment` — priorities, KPIs, alignment rules, coverage reporting
- `intake-governance` — request → triage → score → decision → registry, decision log
- `status-reporting` — cadence, content, RAG definitions, reminders, currency, history
- `executive-dashboards` — Dean / governance / unit views, access control, freshness, export
- `project-workspaces` — provisioning, templates, registry link, closeout and retention

### Modified Capabilities
- None (greenfield)

## Scope

**In scope:** everything under What Changes, a pilot with the Office of the Dean (central
operations), GTPE, and GTLI, and college-wide rollout.

**Out of scope (Phase 1):**
- Task-level scheduling, dependencies, critical path → Phase 2 (`add-execution-and-resource-management`)
- Person-level capacity and allocation → Phase 2 (Phase 1 captures lead unit, contributing units, and effort estimates only)
- Integration with financial systems → future change
- Student-level data of any kind
- Replacing unit-specific operational systems

## Success Criteria

| Measure | Target | Type |
|---|---|---|
| Dean overview live with real data | ≈ 60 days from kickoff (sponsor to confirm) | Milestone |
| Qualifying in-flight projects registered | ≥ 95% within 30 days of go-live | Leading |
| Status currency per cycle | ≥ 90% of active items Current | Leading |
| Alignment coverage | 100% aligned or explicitly Operational/Compliance | Leading |
| Median intake time, submission → decision | ≤ 30 days | Lagging |
| Manual status decks for leadership meetings | Replaced by dashboard within one quarter | Lagging |

## Impact

- **Licensing:** none new. All CLL staff already have Power BI; Phase 1 uses no Planner
  Plan 3/5 and no premium connectors.
- **People:** unit leads submit a monthly update (target ≤ 15 minutes per item); a portfolio
  analyst role in Strategic Operations maintains the registry and runs the cycle.
- **Governance:** introduces registration thresholds and a scoring rubric; the TCC decides
  Tier 1 intake and portfolio-level questions.
- **Dependencies:** Georgia Tech OIT for the SharePoint site, Team, Power BI workspace,
  service account, and a DLP-policy check on the default Power Platform environment.

## Resolved (2026-09-19)

| # | Question | Answer |
|---|---|---|
| 1 | TCC's role | TCC is the decision body for Tier 1 intake and portfolio-level decisions |
| 2 | Power BI licensing | All CLL staff have Power BI — no new licensing for dashboards |
| 3 | Tier thresholds (design D3) | Accepted as proposed |
| 4 | Seed Strategy 2035 priorities? | Yes — 5 goals, 25 objectives, 11 KPIs seeded as Provisional (`sharepoint/seed/`) |
| 5 | Tier 2 decision rights | Unit head decides; Strategic Operations does a data check at triage; TCC has a 10-business-day call-up right (design D11) |
| 6 | Pilot units | Recommended: Office of the Dean (central operations), GTPE, GTLI (design "Pilot") |
| 7 | Power Platform environment | Default environment (design D12) |

## Open Questions (none blocking)

| # | Question | Owner | Needed by |
|---|---|---|---|
| 8 | Who is the executive owner of each Strategy 2035 goal? KPIs and priorities need named owners. | Sponsor | Week 3 (seeding) |
| 9 | Pilot unit heads agree and name a contact | Strategic Ops | Week 2 |
| 10 | Non-personal service account for flows | OIT | Week 2 — fallback in design D9 |
| 11 | How is a "learner touchpoint" counted (KPI-006)? | Sponsor + Institutional Research | Before the Dean overview shows KPIs |
