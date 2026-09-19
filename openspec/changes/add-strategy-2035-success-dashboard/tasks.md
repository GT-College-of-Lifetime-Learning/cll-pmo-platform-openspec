# Tasks — Strategy 2035 Success Metrics Dashboard

Legend: [DEAN] needs the Dean's decision · [OIT] needs Georgia Tech OIT · (code) source-controlled · (config) click-ops
Depends on Phase 1 tasks 2.1–2.8 (lists and seed) and 4.6 (business-day calendar).

## 0. Decisions and access
- [ ] 0.1 [DEAN] Audience (Q1), Goal 1 metric definition (Q2), counting window (Q3), aligned-work counts on cards (Q8)
- [ ] 0.2 [DEAN] Goal 5 target level and rubric sign-off (Q5)
- [ ] 0.3 [OIT] Enable the Azure Maps visual in Power BI tenant settings
- [ ] 0.4 Name owners for headline and secondary KPIs (KPI-001, 003, 004, 005, 006, 007, 010, 012) — builds on Phase 1 task 0.9

## 1. Data
- [ ] 1.1 (code) Add ShortName and DisplayColor to StrategicPriorities; DashboardRole, Basis, and CountingStart to KPIs
- [ ] 1.2 (code) Create lists KpiTrajectories, StrategyActivity, Capabilities with validation (one Headline per goal; evidence required for ratings)
- [ ] 1.3 (code) Load updated seeds: priorities with short names, KPIs with roles and KPI-012, linear trajectories marked unapproved
- [ ] 1.4 (config) Activity entry form (counts and program names only, no learner fields)
- [ ] 1.5 (code) Publish maturity rubric in `docs/`; run the first capability inventory and two-person assessment
- [ ] 1.6 Collect first values: FY26 research expenditures, current hubs list, learning-systems credentials to date, credentials issued since counting start
- [ ] 1.7 (config) Phase 1 closeout: prompt SP-05 project leads to add or update a capability entry

## 2. Semantic model
- [ ] 2.1 (code) Timeline measures: elapsed %, remaining %, calendar and business days remaining, as-of date
- [ ] 2.2 (code) Expected-today by basis (cumulative, annual, point-in-time, index) and pace status
- [ ] 2.3 (code) Headline and secondary selection driven by DashboardRole
- [ ] 2.4 (code) Data-state measures: Live, Stale, Pending source, Pending definition
- [ ] 2.5 (code) Maturity index and heatmap measures
- [ ] 2.6 (code) Active aligned projects and contributing units per goal, behind a configuration flag (Q8)

## 3. Report page
- [ ] 3.1 (code) Header and timeline strip with SVG bar and expected-progress marker
- [ ] 3.2 (code) Five cards per the mapping table in proposal.md
- [ ] 3.3 (code) Signature visuals: ring + term trend; Azure Maps bubbles + hub timeline; credential trend; expenditure trend + gauge; maturity ladder + heatmap
- [ ] 3.4 (code) Recent lists (latest three per goal)
- [ ] 3.5 (code) Drill-through from each card to Phase 1 priority detail
- [ ] 3.6 (code) Phone layout; accessibility: text labels for goal and status, contrast, alt text, table fallback for the map, reading order
- [ ] 3.7 (config) Set as the app landing page; configure audience per Q1

## 4. Verify
- [ ] 4.1 Check timeline figures against a hand calculation (Aug 16, 2026 → 6.2% elapsed, 3,425 days remaining)
- [ ] 4.2 Walk every scenario; Dean review on real data
- [ ] 4.3 `openspec validate add-strategy-2035-success-dashboard --strict`; archive after Phase 1
