# Design: Strategy 2035 Success Metrics Dashboard

## Context
The Dean's mockup (labeled "placeholder metric data for concept review") defines the top of the
reporting hierarchy. This design turns it into the landing page of the Phase 1 Power BI app,
built on the same semantic model, and adds only the data the mockup needs that Phase 1 lacks.

```
Strategy 2035 (this change)  ── outcomes: are we on pace?
   └─ Priority detail (Phase 1) ── objectives, all KPIs, aligned projects
        └─ Dean Overview / Unit / Item detail (Phase 1) ── is the work on track?
```

## Page layout (follows the mockup)

- **Header:** CLL identity, title, window "Jan 1, 2026 – Dec 31, 2035", and the data as-of date
  (replaces the mockup's "placeholder" label).
- **Timeline strip:** time elapsed %, time remaining %, calendar days remaining, target year,
  business days remaining, as-of date; a 2026–2035 bar with an "expected progress by today" marker.
- **Five goal cards**, left to right: goal number and short name in text (color band is decorative),
  headline value vs. target with progress bar and pace marker, secondary metric bar, signature
  visual, three-row recent list, optional footer "Active work: N projects · M units →" (Q8).
- **Footer:** data notes; Goal 5 uses a qualitative maturity index; count of headline KPIs live (n / 5).

## Decisions

### D1. Same app, same model as Phase 1
The Strategy 2035 page is the app's landing page and reads Phase 1's `StrategicPriorities`,
`StrategicObjectives`, `KPIs`, and `KpiValues`. One source of truth; drill-through goes to the
Phase 1 priority detail page.

### D2. Timeline math
- Window: Jan 1, 2026 through Dec 31, 2035 = 3,652 days.
- **Elapsed** = full days before the as-of date; **remaining** = as-of date through Dec 31, 2035, inclusive.
- **Business days** exclude weekends and Institute holidays from the shared `Calendar` table (Phase 1 task 4.6).
- As-of date = date of the last successful refresh.
- Check: on Aug 16, 2026 this yields 6.2% elapsed, 93.8% remaining, and 3,425 calendar days
  remaining — the same figures shown in the mockup.

### D3. Pace against a trajectory, not a straight line by default
Expected-today = the approved trajectory value interpolated to the as-of date.
- **Cumulative KPIs** (graduates, hubs, start-ups, touchpoints, credentials): trajectory runs from the counting start to target.
- **Annual KPIs** (research $): trajectory runs from the baseline fiscal year to the target year; needs a baseline.
- **Index KPIs** (maturity): trajectory runs from the first assessment to the target level.

| Pace status | Rule |
|---|---|
| On pace | Actual ≥ 95% of expected-today |
| Behind | 80–95% |
| Well behind | < 80% |
| Not yet measurable | No data, no baseline, or before the trajectory's first milestone |

**Why not linear only:** several goals are back-loaded — degrees launch by 2029, hubs open in
batches, research grows from a base — so a straight line would show them "behind" for years. A
linear default is generated so the card is never blank, but it is labeled **"Linear pace
(unapproved)"** until the KPI owner and Dean approve annual milestones.

### D4. Card roles are data
`KPIs.DashboardRole` = Headline / Secondary / Detail; exactly one Headline and at most one
Secondary per goal. Swapping what a card leads with is a data change, not a report change.

### D5. One activity list for all "most recent" panels
`StrategyActivity` holds typed entries (TermGraduates, HubOpening, StartupAdopted,
CredentialIssued, GrantAwarded, CapabilityDelivered). Each card shows its latest three. Entries
carry counts and names of programs, hubs, or grants — never learner identities. Phase 2 can
automate feeds from source systems; v1 is manual entry through a form.

### D6. Goal 5 Digital Transformation Maturity Index
A `Capabilities` inventory lists CLL workflows and services with a current maturity level,
assessment date, assessor, and evidence link. **Index = mean current level of in-scope
capabilities** (unweighted in v1). The heatmap shows capability areas × levels.

**Draft rubric (for Dean sign-off, Q5):**

| Level | Name | Meaning |
|---|---|---|
| 1 | Manual | Paper, email, or hand-passed spreadsheets |
| 2 | Digitized | Captured in a system of record; online forms |
| 3 | Automated | Rule-based workflow moves the work without manual handoffs |
| 4 | Data-driven | Instrumented, monitored on dashboards, continuously improved |
| 5 | AI-enabled | AI agents perform or assist steps with human oversight |

The mockup's "Digitized / Automated / AI-enabled" labels map to levels 2, 3, and 5. When a
Phase 1 project aligned to SP-05 closes, its closeout prompts the lead to add or update the
capability it delivered — so Goal 5 progress is fed by Goal 5 work.

### D7. Data honesty
No placeholder or sample numbers in production. Every metric is in one of four states:

| State | Shown as |
|---|---|
| Live | Value, as-of date, source (tooltip) |
| Stale | Last value, greyed, "as of <date>" |
| Pending source | "Data source pending" + owner |
| Pending definition | "Definition pending" (e.g., touchpoints until Q6 is answered) |

Priorities and objectives still carry Phase 1's Provisional label until confirmed.

### D8. Visual implementation (Power BI)

| Mockup element | Build |
|---|---|
| Timeline strip and pace marker | Cards + DAX measure returning an SVG image for the bar and marker |
| Progress ring + term trend | Donut from DAX measures + column chart by term |
| Hub map + hub timeline | Azure Maps visual, bubble layer, with stored lat/long (no geocoding) + column chart by year; table fallback for accessibility |
| KPI card + credential trend | Card + line chart by quarter |
| Expenditure trend + funding gauge | Line chart by fiscal year + gauge vs. $20M |
| Maturity ladder + capability heatmap | SVG segmented bar (L1–L5) + matrix with conditional formatting |

Azure Maps must be enabled in the Power BI tenant settings [OIT]. Goal identity and status are
always shown in text, never by color alone. A phone layout stacks the cards under the timeline.

### D9. Audience and security
The page shows only college-level aggregates, so it is safe for an all-staff audience if the Dean
wants one (Q1). Drill-through and the optional aligned-work counts respect Phase 1 row-level security.

## Data model additions

| List / field | Purpose |
|---|---|
| `StrategicPriorities` + ShortName, DisplayColor | Card labels and bands |
| `KPIs` + DashboardRole, Basis (Cumulative / Annual / PointInTime / Index), CountingStart | Card roles and pace math |
| `KpiTrajectories` — KpiId, PeriodEnd, ExpectedValue, Approved, ApprovedBy, ApprovedOn | Pace |
| `StrategyActivity` — ActivityId, Type, PriorityId, Title, Date, Value, UnitOfMeasure, Source, SubmittedBy | Recent lists |
| `Capabilities` — CapabilityId, Name, Area, OwningUnitId, Level, AssessedOn, Assessor, EvidenceUrl, InScope, LinkedItemId | Goal 5 index and heatmap |

Seed updates in `sharepoint/seed/`: short names and colors on priorities; DashboardRole, Basis,
and CountingStart on KPIs; new KPI-012 (maturity index); `kpi-trajectories.csv` with linear
defaults marked unapproved.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Linear pace misleads on back-loaded goals | Labeled unapproved; trajectories approved within 90 days (D3) |
| Dean sees mostly "pending" at launch | Name KPI owners first (Phase 1 task 0.9); launch when ≥ 3 of 5 headlines are live; footer shows n / 5 |
| Definitions drift ("graduates" vs. "credentialed") | Definition stored on each KPI and shown in the tooltip; Q2 settles Goal 1 |
| Double counting in cumulative learner KPIs | Definitions specify "unique"; source owners certify method |
| Maturity index is subjective | Published rubric, evidence link required, two-person assessment |
| Page shared beyond CLL with provisional numbers | Internal audience only unless the Dean approves otherwise |

## Rollout (targets, in parallel with Phase 1)

| Weeks | Milestone |
|---|---|
| 2–3 | Seed updates, trajectories, activity and capability lists; timeline strip live |
| 3–5 | Cards on available data; first Goal 5 inventory; Dean reviews a draft on real data |
| 6 | Published as the app landing page |
| Ongoing | Owners close "pending" states; trajectories approved |
