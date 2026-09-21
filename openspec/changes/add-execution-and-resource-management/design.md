# Design: Phase 2 — Execution Integration and Resource Capacity

## Context

The founding-request audit found resource management the only unspecced layer. This
change completes the spec registry; implementation is gated on Phase 1 adoption
(≥ 90% currency × 2 cycles). Demo-implementable portions (capacity model, sync-draft
flow, risk indicators) build in the local demo against the same contracts, so the
production build ports from a working reference — the project's established pattern.

```
execution plan (Tier 1 standard tool)  ──one-way sync──▶  registry (system of record)
        plan milestones/percent                            ├── auto-populated status drafts
                                                            ├── schedule-risk indicator
unit head allocations ──▶ capacity model ──▶ heatmap (units × periods)
                                            ├── over-allocation → unit head + governance
                                            └── capacity summary → Dean overview
```

## Decisions

### D1. Registry stays the system of record; sync is one-way
Plans push milestones + percent complete INTO the registry on a schedule (target: within
one business day; production via scheduled flow). The registry never writes back except
on explicit command. When plan data and a lead's entry disagree, both surfaces show the
registry value with its as-of date AND surface the disagreement — silent resolution in
either direction is a trust failure.

**Why not bidirectional:** the registry feeds RLS-governed dashboards, the decision log,
and closeout; letting a plan tool overwrite governed data bypasses every gate Phase 1
built. The plan is a witness, not the record.

### D2. Standard tool for Tier 1; everything else stays free
Tier 1 items activate with a plan in the standard tool (workspace provisioning creates
it, F3's pattern extended). Tier 2 keeps execution-tool independence untouched — the
adoption fight stays out of Phase 2 the way it stayed out of Phase 1.

**Licensing:** premium licenses for Tier 1 PMs only. Count = Tier 1 lead count, knowable
only after Phase 1 registration (proposal Q1) — do not buy until the count exists.

### D3. Sync-failure honesty mirrors data-state honesty
Synced fields carry a sync-state (live / stale / failed) computed like the KPI data
states: expected window elapsed without a successful sync → stale, labeled everywhere
the values appear. The finding tracker records chronic sync failures (type
`sync-failed`, 2/3/4 ladder applies). This reuses the trust architecture rather than
inventing a parallel one.

### D4. Allocation granularity is a policy flag, not a schema choice
One `Allocations` store: Period, ItemId, UnitId, Granularity (person|role), Target
(person UPN or role name), Percent. The Dean's privacy answer (Q2) sets the flag;
entry forms and every view enforce it. Role-level selected ⇒ person-level is not
addressable anywhere — enforced at the query layer, not just hidden in the UI.

**Why both:** the spec keeps capability without committing HR to person-level data;
the Dean decides, and the system honestly does whichever was chosen.

### D5. Capacity math is simple and labeled
Committed = Σ allocations per unit-period. Available = the unit's stated capacity
(unit heads declare FTE available per period; Q4). Utilization states: unallocated
(<10%), allocated, at capacity (90–100%), over-allocated (>100%). Heatmap cells carry
text labels (WCAG discipline). Stale-allocation labeling mirrors D3: allocations older
than one cycle mark the computed utilization stale.

### D6. Over-allocation is visible, never prevented
Recording an allocation that exceeds capacity stores it and warns — unit heads own
staffing trade-offs; the system's job is to make the over-commitment impossible to
miss. Cross-unit over-allocations also surface in governance (they're college risk,
not just unit risk).

### D7. Schedule-risk indicator, derived not asserted
For synced Tier 1 items: next milestone's forecast vs. baseline; slip count = consecutive
periods forecast > baseline. Display: text ("milestone slipped 2 periods") + trend, not
color alone; drill to the milestone history. The lead's RAG remains their judgment; this
indicator is computed evidence next to it.

### D8. Auto-populated drafts, not eliminated updates
Synced items still get one confirmed update per period — the draft arrives with
milestone/forecast/percent pre-filled and sync-named as source; the lead edits anything
and confirms. **Why not auto-submit:** the RAG, summary, and decision ask are human
judgments; a silent pipeline would erode the append-only status history's meaning (and
the currency metric that gates Phase 2 itself).

### D9. Production port
| Demo | Production |
|---|---|
| `demo/sync_engine.py` (planted plan data → registry updates, sync states) | Scheduled flow reading premium plan data (standard connectors where possible; the premium-data connector question is OIT Q3) |
| `Allocations` table + `/capacity` heatmap | SharePoint list + Power BI matrix visual with RLS |
| Draft auto-population in the status form | F4 pre-fill step reading synced fields |
| Roadmap view from registry data | Portfolio tool as a presentation layer; registry + Power BI remain authoritative |

### D10. Dataverse revisit trigger (carried, not scheduled)
When Phase 2's production sync builds on premium plan data (which lives in Dataverse),
re-evaluate the registry's home per Phase 1 design D1. Recorded here so the trigger
survives; migration itself is out of scope.

## Data model additions

| Table / field | Purpose |
|---|---|
| `Allocations` (AllocationId, Period, ItemId, UnitId, Granularity, Target, Percent, AllocatedBy, AllocatedOn, ReviewedOn) | capacity model (D4/D5) |
| `UnitCapacity` (UnitId, Period, AvailableFte, DeclaredBy) | denominator (D5) |
| `WorkItems` + `SyncEnabled`, `LastSyncOn`, `PlanUrl` | execution link + honesty (D1/D3) |
| `Milestones` + `Source` (manual\|sync) | provenance for synced milestones |

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Sync becomes a trust leak (stale plan data shown as current) | D3 sync states + finding-tracker ladder |
| Person-level allocation raises HR concerns | D4 policy flag; default role-level until the Dean answers Q2 |
| Capacity theater: allocations gamed or stale | D5 stale labeling; unit-head accountability; over-allocation always visible |
| Premium license cost surprises | D2: count before buying; Q1 owns the number |
| Phase 2 starts before adoption | Entry criteria hard-gated; first implementation task re-checks |

## Rollout (gated)

| Gate | Milestone |
|---|---|
| Entry check | ≥ 90% currency × 2 consecutive cycles (task 0.1 re-verifies) |
| Phase A | License count (Q1), granularity decision (Q2), capacity baselines (Q4) |
| Phase B | Demo: allocations + capacity heatmap + risk indicator + sync-draft flow (implementable now, parkable without) |
| Phase C | Production: standard tool designated, provisioning extended, sync flow + monitoring live |
| Phase D | First capacity cycle; adoption measured against success criteria |