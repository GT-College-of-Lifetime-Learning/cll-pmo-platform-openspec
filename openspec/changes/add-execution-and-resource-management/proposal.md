# Proposal: CLL SPM — Phase 2: Execution Integration and Resource Capacity
*(Stub. Generate specs, design, and tasks with `/opsx:continue` once Phase 1 meets its entry criteria.)*

## Why
Phase 1 shows leadership what is underway, why, and how it is going. It does not show
whether CLL has the people to deliver it, or task-level schedule risk on the largest efforts.
"Cross-functional resource management" was in the original scope and is deferred here.

## Entry criteria
Do not start until Phase 1 has held ≥ 90% status currency for two consecutive cycles.
Adding execution tooling to an unadopted reporting system multiplies the adoption problem.

## What Changes (draft)
- **Planner premium as the standard execution tool for Tier 1 work.** Plan 3 for project
  managers; Plan 5 only where portfolio leads need it. Contributors work in premium plans with
  basic editing under their existing Microsoft 365 license.
- **Planner Portfolios** as a roadmap view for program and portfolio leads, alongside (not
  instead of) the registry.
- **Execution sync.** Milestones and percent complete flow from premium plans into the registry
  so Tier 1 leads stop double-entering; evaluate moving the registry to Dataverse, where
  premium plan data already lives.
- **Resource capacity.** Role- or person-level allocation (% per item per month) with a unit
  capacity heatmap and over-allocation alerts. Compare Planner's resource features against a
  lightweight allocation list before committing.

## Capabilities
### New Capabilities
- `execution-integration` — premium-plan linkage and milestone/progress sync
- `resource-capacity` — allocation, capacity, and over-allocation reporting

### Modified Capabilities
- `portfolio-registry` — execution sync fields; possible Dataverse migration
- `executive-dashboards` — capacity views; schedule-risk indicators for Tier 1
- `status-reporting` — auto-populated fields for synced items

## Impact
- **Licensing:** Planner and Project Plan 3 (≈ $30/user/month list) for Tier 1 PMs; Plan 5
  selectively; possible premium connector or Dataverse capacity if the registry moves.
- **People:** Tier 1 PMs adopt Planner premium; unit heads maintain allocations monthly.

## Open Questions
- How many people would need Plan 3? (Drives cost; count Tier 1 leads after Phase 1.)
- Allocate by named person or by role? (Privacy and HR sensitivity vs. precision.)
- Does OIT support Dataverse for this, and in which environment?
