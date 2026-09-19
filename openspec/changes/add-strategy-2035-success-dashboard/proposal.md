# Proposal: Strategy 2035 Success Metrics Dashboard
### The Dean's top-level view

**Requested by:** Dean (via Bill) · **Owner:** Strategic Operations · **Audience:** Dean, TCC; possibly all CLL staff (Q1)
**Decision this enables:** on one screen, the Dean sees how far CLL is through the Strategy 2035
window and whether each of the five goals is on pace.

## Why

The Dean has shared a mockup of the view he wants at the very top: a *Strategy 2035 Success
Metrics Dashboard* covering Jan 1, 2026 – Dec 31, 2035. It has two parts:

- **A strategy timeline** — time elapsed and remaining, calendar and business days remaining,
  target year, and an "expected progress by today" marker.
- **One card per goal** — a headline metric, a secondary metric, a signature visual, and a short
  "most recent" activity list.

Phase 1 (`add-portfolio-registry-and-exec-dashboards`) builds the Dean Overview around the
status of work. This mockup sits one level above that: **outcomes, not activity**. Phase 1 already
stores priorities, objectives, KPIs, and KPI values, so this page is mostly presentation — plus
four things the mockup needs that Phase 1 does not have:

1. **Headline and secondary roles** — which KPI leads each goal card.
2. **Pace** — an expected value for "today" for every headline KPI, so a card can say on pace or behind.
3. **Recent-activity feeds** — terms graduated, hubs opened, credentials issued, grants awarded, capabilities delivered.
4. **A Digital Transformation Maturity Index** for Goal 5 (qualitative, 1–5, with a capability inventory).

The slide that framed the mockup asks, *"Where do you see yourself in this vision?"* The
registry can answer that literally: each goal card can show how many active projects and units
are aligned to it, one click from the list. **This is an addition to the mockup — confirm with the Dean (Q8).**

## What Changes

- A **Strategy 2035** landing page, first in the CLL SPM Power BI app, above the Dean Overview.
- A **timeline strip** recalculated at every refresh.
- **Five goal cards** matching the mockup:

| Card | Headline | Secondary | Signature visual | Recent list |
|---|---|---|---|---|
| 1 · Learning Systems Leaders | 5,000+ graduates (KPI-001) | Fortune 500 leaders (KPI-003) | Progress ring + term trend | Graduates by most recent term |
| 2 · Global Learning Hubs | 200 hubs (KPI-004) | Start-ups adopted (KPI-005) | Hub map + hub timeline | Most recent hub openings |
| 3 · Learner Reach | 5M touchpoints (KPI-006) | Credentials issued (KPI-007) | KPI card + credential trend | Recent credentials issued |
| 4 · Research Leadership | $20M annual (KPI-010) | — | Expenditure trend + funding gauge | Most recent grants |
| 5 · Digital Transformation | Maturity index / 5.0 (KPI-012, new) | — | Maturity ladder + capability heatmap | Recent capabilities |

- A **pace indicator** on every headline KPI, measured against an approved trajectory (a linear
  default is shown, labeled unapproved, until one is approved).
- **Data honesty rules** — no placeholder numbers in production; explicit "pending" states;
  as-of date and source on every number.
- **Drill-through** from each card to Phase 1's priority detail page (objectives, all KPIs, aligned projects).
- **Data additions** — KPI roles, basis, and counting start; trajectories; an activity list; a
  capability inventory with a published maturity rubric.

KPIs not on the top level (degree levels KPI-002, graduation rate KPI-008, content renewal
KPI-009, dashboard coverage KPI-011) appear one click down on the priority detail page.

## Capabilities

### New Capabilities
- `strategy-success-dashboard` — the landing page: timeline, goal cards, pace, recent activity, drill-through
- `strategy-kpi-data` — KPI roles and basis, trajectories, activity feed, maturity index, provenance

### Modified Capabilities
- None in `openspec/specs/` yet. Builds on Phase 1's `strategic-alignment` and
  `executive-dashboards` (not yet archived); archive Phase 1 first.

## Sequencing

**Build this page first**, alongside Phase 1 weeks 2–5. It needs only the KPI lists and a few
small manual feeds — none of the intake, status, or workspace flows — so the Dean sees real
data early. It launches with explicit "Data pending" states rather than waiting for all five goals.

## Success Criteria

| Measure | Target |
|---|---|
| Timeline + five cards live (real values or explicit pending states) | Week 6 of Phase 1 |
| Headline KPIs with real, sourced values | ≥ 3 of 5 at launch; 5 of 5 within one quarter |
| Headline KPIs with a named owner, source, and approved trajectory | 5 of 5 within 90 days of launch |
| Dean opens leadership and TCC meetings from this page | Sponsor-confirmed within one quarter |

## Impact

- **Licensing:** none new.
- **Tenant:** the hub map needs the Azure Maps visual enabled in Power BI admin settings [OIT].
- **People:** KPI owners submit values on each KPI's cadence and keep their activity list current;
  Strategic Operations runs a Goal 5 maturity assessment twice a year.
- **Data:** aggregate counts only. No learner-level records or learner names anywhere.

## Open Questions

| # | Question | Owner | Needed by |
|---|---|---|---|
| 1 | Audience: Dean and TCC only, or all CLL staff? The slide's framing suggests college-wide. | Dean | Week 4 |
| 2 | Goal 1: "graduates" (degrees only, as the mockup says) or the plan's "credentialed and graduated" (includes certificates and minors)? | Dean | Before KPI-001 loads |
| 3 | Counting window: do cumulative KPIs start Jan 1, 2026 (the mockup window), or include earlier results? | Dean | Week 4 |
| 4 | Pace: approve annual trajectories per headline KPI, or accept linear with a caveat? | Dean + KPI owners | 90 days after launch |
| 5 | Goal 5: target maturity (5.0? 4.0?), rubric sign-off, and assessor | Dean + Strategic Ops | Before the Goal 5 card shows a value |
| 6 | Definition of a "learner touchpoint" (carried from Phase 1 Q11) | Dean + Institutional Research | Before the Goal 3 headline shows a value |
| 7 | Goal 4: fiscal-year basis and which sponsored-research attribution counts as CLL | Research administration | Before the Goal 4 card shows a value |
| 8 | Show aligned-project and unit counts on each card? | Dean | Week 4 |
