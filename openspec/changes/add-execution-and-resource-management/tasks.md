# Tasks — Phase 2: Execution Integration and Resource Capacity

Legend: [GATE] blocked on Phase 1 adoption · [DEAN] needs the Dean · [OIT] needs Georgia Tech OIT ·
(code) source-controlled · (test) adversarial/planted-defect verification · (humans) real-world input

## 0. Entry gate and decisions
- [ ] 0.1 [GATE] Verify entry criteria before any implementation: ≥ 90% status currency for two consecutive Phase 1 cycles
- [ ] 0.2 [DEAN] Allocation granularity (Q2) — person-level or role-level; role-level is the default until answered
- [ ] 0.3 [GATE] Count Tier 1 leads/PMs after Phase 1 registration → premium license count (Q1)
- [ ] 0.4 [OIT] Confirm environment + connector path for premium plan data (Q3)
- [ ] 0.5 (humans) Unit heads declare available capacity per period (Q4) — capacity baselines

## 1. Demo: resource capacity (implementable now)
- [ ] 1.1 (code) `Allocations` + `UnitCapacity` tables; `WorkItems` gains SyncEnabled/LastSyncOn/PlanUrl; Milestones gains Source
- [ ] 1.2 (code) Allocation entry: unit-head form per item/period with the granularity flag enforced at entry; over-allocation warning on save (visible, not preventing)
- [ ] 1.3 (code) Capacity model: utilization per unit-period with states unallocated/allocated/at capacity/over-allocated; stale-allocation labeling after one cycle unreviewed
- [ ] 1.4 (code) `/capacity` heatmap page: units × periods, text labels, drill from a cell to driving items
- [ ] 1.5 (code) Governance: cross-unit over-allocations surface in the needs-attention list; Dean overview gains capacity summary with over-allocated units named
- [ ] 1.6 (test) Planted defects: over-allocation entry stores + warns; role-level flag blocks person-addressable queries; stale allocations label the result; heatmap cell text not color alone

## 2. Demo: execution sync contracts (implementable now)
- [ ] 2.1 (code) `demo/sync_engine.py`: planted plan (JSON fixture) → registry milestone/percent updates, one-way; sync states live/stale/failed per D3
- [ ] 2.2 (code) Status draft flow: synced items' monthly update arrives pre-populated (milestone/forecast/percent, sync named as source); confirm-or-edit; confirmation counts as the period update
- [ ] 2.3 (code) Schedule-risk indicator on Tier 1 item detail: milestone slip vs baseline over consecutive periods, text + trend, sync state shown
- [ ] 2.4 (code) Sync-failed findings feed the finding tracker (type sync-failed, 2/3/4 ladder)
- [ ] 2.5 (code) Roadmap view: programs/portfolios on a timeline from registry data, drill to detail
- [ ] 2.6 (test) Planted defects: broken plan link → stale/failed labels on every surface; disagreement between plan and lead entry surfaces (not silently resolved); draft without confirmation does NOT count toward currency; risk indicator shows slip text

## 3. Production: standard tool + sync (gated)
- [ ] 3.1 [GATE] Designate the Tier 1 standard execution tool; extend workspace provisioning (F3 pattern) to create the plan and record PlanUrl
- [ ] 3.2 [GATE] Build the scheduled sync flow per D9 port map; sync-state computation in the semantic model
- [ ] 3.3 [GATE] F4 pre-fill step reading synced fields (production draft flow)
- [ ] 3.4 [GATE] Capacity pages in Power BI with RLS; heatmap matrix; Dean overview capacity tiles
- [ ] 3.5 [GATE] Licensing: acquire per the Q1 count; verify contributors' basic-edit path
- [ ] 3.6 [OIT] Dataverse revisit evaluation (design D10 trigger) — record the decision either way

## 4. First capacity cycle and verify
- [ ] 4.1 (humans) Unit heads record first month's allocations; review cadence begins
- [ ] 4.2 [GATE] Measure: allocations current for ≥ 90% of active Tier 1 items; zero Tier 1 double-entry after sync live
- [ ] 4.3 (test) Full regression battery + all new planted-defect suites
- [ ] 4.4 `openspec validate add-execution-and-resource-management --strict`; sync specs; archive after Phase 1 archives