# Proposal: CLL SPM — Phase 2: Execution Integration and Resource Capacity
### The last unspecced layer of the founding request

**Sponsor:** Bill · **Owner:** Strategic Operations · **Audience:** Dean, TCC, unit leaders, Tier 1 PMs
**Decision this enables:** leadership can see whether CLL has the people to deliver what it has committed to, and the largest efforts stop double-entering progress.

## Why

The audit of the founding request ("the project to manage all projects," with the Copilot
Microsoft-suite map) against the twelve synced capability specs found exactly one layer
with no spec coverage: **cross-functional resource management** — the layer Copilot's map
also left without a tool. Phase 1 answers *what is underway, why, and how it is going*;
nothing answers *whether the people exist to deliver it*, and Tier 1 leads will soon be
entering status by hand while their execution tool already knows the answers.

This change completes the spec registry: after it, every layer of the founding request
is specced. Implementation remains gated on adoption (entry criteria below), so this is
planned-but-parked — the project's established pattern: spec fully now, implement when
the gate opens.

## Entry criteria (unchanged, enforced)

Do not begin implementation until Phase 1 has held **≥ 90% status currency for two
consecutive cycles**. Adding execution tooling to an unadopted reporting system
multiplies the adoption problem. Planning artifacts (this change) are complete now;
the first implementation task re-checks the gate.

## What Changes

- **Execution tool standardization for Tier 1 work** — premium planning as the standard
  execution tool for Tier 1 projects (project-manager license tier; contributors work
  with basic editing under existing licenses).
- **Portfolio roadmap views** — a roadmap view for program and portfolio leads,
  alongside (never instead of) the registry.
- **Execution sync** — milestones and percent complete flow from the execution tool
  into the registry so Tier 1 leads stop double-entering; the registry remains the
  system of record.
- **Resource capacity** — allocation per item per period with a unit capacity heatmap,
  over-allocation flags, and a college-level capacity view answering "can we staff what
  we approved?"
- **Schedule-risk indicators** for Tier 1 items on executive views (milestone slip
  against baseline, derived from synced data).

## Capabilities

### New Capabilities
- `execution-integration` — tool linkage, sync direction, sync-failure honesty, execution-tool policy
- `resource-capacity` — allocations, capacity, over-allocation, staffing answerability

### Modified Capabilities
- `portfolio-registry` — Execution tool independence gains the Tier 1 standard-tool expectation
- `executive-dashboards` — Dean overview gains capacity and schedule-risk elements
- `status-reporting` — synced items' updates become auto-populated drafts, not eliminated

## Scope

**In scope:** the five items above, specced fully; demo-implementable portions (allocation
model, capacity math, risk indicators, auto-populated drafts) implementable in the local
demo without the tenant; production sync flows specced against the platform design.

**Out of scope:**
- Task-level management *inside* the registry — tasks live in execution tools only
- Person-level named allocation if the Dean answers the privacy question with "role-level"
  (the spec supports both; the decision is Q2)
- Financial system integration (unchanged from Phase 1's out-of-scope)
- Dataverse migration of the registry — recorded as a revisit trigger in design, not a requirement

## Success Criteria

| Measure | Target | Type |
|---|---|---|
| Founding-request spec coverage | 100% of layers specced (audit-verifiable) | Milestone |
| Tier 1 leads double-entering progress | Zero after sync goes live | Lagging |
| Over-allocated units visible before approval, not after | Capacity view live with pilot data | Leading |
| Unit heads maintaining allocations | ≥ 90% of active Tier 1 items allocated per month | Leading |

## Impact

- **Licensing:** execution-tool premium licenses for Tier 1 PMs only (list ≈ $30/user/month;
  education pricing differs); contributors unchanged. Exact count is Q1 — driven by the
  number of Tier 1 leads, knowable only after Phase 1 registration.
- **People:** Tier 1 PMs standardize on the premium tool; unit heads maintain allocations
  monthly (target ≤ 10 minutes); Strategic Operations operates sync monitoring.
- **Governance:** capacity joins the Dean overview; the TCC sees staffing risk before
  approving cross-unit work.
- **Dependencies:** Phase 1 adoption (entry criteria); OIT licensing and (for production
  sync) platform decisions.

## Open Questions

| # | Question | Owner | Needed by |
|---|---|---|---|
| 1 | How many Tier 1 PMs need premium licenses? (Count after Phase 1 registration) | Strategic Ops | Gate opening |
| 2 | Allocate by named person or by role? (HR/privacy sensitivity vs. precision) | Dean + HR | Before capacity spec implements |
| 3 | Which platform environment for premium plan data? | OIT | Before production sync builds |
| 4 | Capacity baseline: what counts as a unit's available hours? | Unit heads | First capacity cycle |