# Proposal: Data Source Reconciliation
### The data-needs catalog, source-state tracking, and incremental real-data integration

**Owner:** Strategic Operations · **Audience:** Strategic Ops (operators), Dean (UNDEFINED routing), dashboard consumers
**Decision this enables:** Strategic Ops knows, for every number the dashboard shows, whether real data exists for it, where, in what shape — and what to build next to close each gap.

## Why

Working backwards from every dashboard visual yields a precise data-needs map (captured this session in `docs/BUILD.md`'s demo section and the backwards-matrix discussion). That map splits the data into three buckets:

1. **Self-generated** (~60% of visuals): intake requests, status updates, decisions, milestones — created by using the system; no external source to find.
2. **External-source data** (concentrated in the Strategy 2035 layer): KPI values, activity entries, capability ratings, hub locations, the Institute holiday calendar.
3. **Computed** (already done): readiness gates, findings, pace, masked counts.

Bucket 2 has no reconciliation instrument today. The financial-ai sibling pipeline solved this exact problem with an intake advisor (profile what you have, assess which needs are met, recommend what to acquire next) and an input-coverage analyzer (do the files form a complete picture). Neither pattern was brought forward in the trust-and-readiness change — they were deliberately deferred as "adaptive intake profiling" and now fit exactly.

Phase framing agreed with the sponsor:

- **P1 (complete):** fabricated demo data — the schema contract.
- **P2 (this change, first half):** reconcile what data we currently have and what we need.
- **P3 (this change, ongoing pattern):** integrate what we have incrementally; list what sources must be built and how.

## What Changes

- A **data-needs catalog** as data: one row per external data element — element, consumer visual(s), required fields, cadence, definition state, owner — seeded from the backwards map (5 headline KPIs, secondary KPIs, activity entry types, capability inventory fields, hub locations, Institute holidays).
- **Source state per need**: `UNDEFINED` (definition-gated; routes to the Dean before any build work), `MISSING`, `PARTIAL`, `HAVE` — with declared system, format, refresh cadence, and steward once known.
- **A source declaration form** (structured, one row per source) for stakeholder discovery: unit data stewards declare what exists, where, in what shape.
- **Incremental integration support**: imported real data lands in the demo database **alongside** fabricated data, tagged by origin (`DataSource`: `demo-seed` | `imported:<name>` | `manual:<owner>`); existing provenance display surfaces the tag, so a card can say "demo-seed" honestly.
- **A coverage view** answering "what can this dashboard truthfully show today?" — per need: sourced, partially sourced, or unsourced.
- A **derived working artifact** `docs/data-source-matrix.md` (generated from + validated against the catalog; the catalog is the source of truth, the matrix is the checklist Strategic Ops works through).

## Capabilities

### New Capabilities
- `data-sourcing` — the catalog, source states, declaration capture, incremental integration tagging, and coverage reporting

### Modified Capabilities
- None (the catalog references consumer visuals in other capabilities but changes none of their requirements)

## Scope

**In scope:** catalog + states + declaration form + coverage view + DataSource tagging in the demo; the matrix generator; loader pattern for the first confirmed HAVE sources as they arrive.

**Out of scope:**
- Definition decisions themselves (graduates-vs-credentialed, touchpoint, research attribution) — tracked as UNDEFINED needs routed to the Dean; the change does not answer them
- Actual stakeholder data collection (humans respond to the declaration asks)
- Production SharePoint / Power Automate wiring (OIT-gated; the M365 port map already documents the target shapes)
- Automating source-system extraction (each integrated source gets a small loader; automated feeds are future increments)

## Success Criteria

| Measure | Target |
|---|---|
| Catalog covers every external data element the dashboards consume | 100% from the backwards map |
| Every catalog row carries a source state | No blank states after P2.2 discovery round |
| A real import lands tagged and the dashboard reflects it honestly | Demonstrated with one source (e.g., GT holiday calendar) |
| Coverage view matches catalog truth | Scenario-tested |
| Matrix regenerates from catalog with zero drift | Generated, validated, committed |

## Impact

- **Licensing:** none.
- **People:** Strategic Ops works the matrix; unit data stewards fill one declaration per source; the Dean's open questions gain a routing mechanism (UNDEFINED rows).
- **Data:** real imported data is clearly tagged and never silently replaces fabricated demo data.

## Open Questions (none blocking)

| # | Question | Owner | Needed by |
|---|---|---|---|
| 1 | Who are the data stewards per source domain (registrar, institutional research, research admin, GTPE academic)? | Strategic Ops | Before discovery round |
| 2 | Which need should be the first integration increment? (Recommended: Institute holiday calendar — smallest, already REVIEW-flagged) | Strategic Ops | P3 kickoff |