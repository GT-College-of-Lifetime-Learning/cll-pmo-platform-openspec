# Data Source Matrix

GENERATED from the DataNeeds catalog — do not edit by hand; regenerate with
`python demo/generate_matrix.py` (drift is detected and replaced with catalog truth).

The P2/P3 workflow: steward declares a source → row state flips → loader increment
imports it tagged → coverage reflects it. UNDEFINED rows route to the sponsor first.

**Coverage:** 6 sourced · 1 partial · 18 unsourced · 6 definition-gated (sponsor first)

## All views (RLS, unit pages)

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-025 | Unit registry (units, heads, access) | On change | defined | **PARTIAL** | org chart (units.csv seed) | Strategic Operations | units seeded; heads + full org chart pending Dean's office confirmation |

## Dean Overview

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-020 | Executive milestones (forecast dates) | Monthly | defined | **HAVE** | this system | Project leads |  |

## Dean Overview / Governance

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-022 | In-flight work backfill (pilot units) | Once + on intake | defined | **MISSING** | — | Unit heads + Strategic Ops | pilot backfill is Phase 1 task 7.1 - the data exists in unit records, not a system |

## Dean Overview / Unit

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-021 | Status updates (RAG, currency) | Monthly | defined | **HAVE** | this system | Project leads |  |

## Governance

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-023 | Intake requests + decisions | Continuous | defined | **HAVE** | this system | CLL staff / TCC |  |
| DN-024 | Scoring rubric calibration (weights) | Per TCC batch | defined | **MISSING** | — | TCC | docs/tiers-and-scoring.md; TCC calibrates on first batch |

## Priority detail / Goal 3

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-008 | 3-year graduation rate (KPI-008) | Annual | defined-partial | **MISSING** | — | — | baseline from Institutional Research; target = 2x baseline |
| DN-009 | Annual content renewal rate (KPI-009) | Annual | defined | **MISSING** | — | — |  |

## Priority detail / Goal 5

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-012 | Dashboard KPI coverage (KPI-011) | Quarterly | defined | **HAVE** | this system | Strategic Operations | measured by the system itself |

## Readiness / business-day math (all views)

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-019 | Institute holiday calendar | Annual | defined | **HAVE** | steward-confirmed calendar | Strategic Operations | confirmed calendar imported 2026-09-19 |

## Strategy 2035 / Goal 1

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-001 | Learning-systems graduates (KPI-001) | Annual | UNDEFINED-Q2 | **MISSING** | — | — | Q2: graduates (degrees only) vs credentialed+graduated |
| DN-002 | Fortune 500 leaders credentialed (KPI-003) | Annual | defined | **MISSING** | — | — |  |

## Strategy 2035 / Goal 1 recent

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-013 | Term graduates by term | Per term | UNDEFINED-Q2 | **MISSING** | — | — |  |

## Strategy 2035 / Goal 2

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-003 | Connected learning hubs (KPI-004) | Annual | defined | **MISSING** | — | — |  |
| DN-005 | Start-ups with market adoption (KPI-005) | Annual | defined | **MISSING** | — | — |  |

## Strategy 2035 / Goal 2 map

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-004 | Hub locations (lat/long per hub) | On change | defined | **MISSING** | — | — | map visual needs stored coordinates; no geocoding (design D8) |

## Strategy 2035 / Goal 2 recent

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-014 | Hub openings | On change | defined | **MISSING** | — | — |  |

## Strategy 2035 / Goal 3

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-006 | Learner touchpoints (KPI-006) | Quarterly | UNDEFINED-Q6 | **MISSING** | — | — | Q6: what counts as a touchpoint - routed to sponsor first |
| DN-007 | Unique learners credentialed (KPI-007) | Quarterly | defined | **MISSING** | — | — |  |

## Strategy 2035 / Goal 3 recent

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-015 | Credentials issued | Quarterly | defined | **MISSING** | — | — | counts only; never learner identities |

## Strategy 2035 / Goal 4

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-010 | Annual external research expenditures (KPI-010) | Annual | UNDEFINED-Q7 | **MISSING** | — | — | Q7: fiscal-year basis + sponsored-research attribution rules |

## Strategy 2035 / Goal 4 recent

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-016 | Grants awarded | On award | defined | **MISSING** | — | — |  |

## Strategy 2035 / Goal 5

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-011 | Digital Transformation Maturity Index (KPI-012) | Semiannual | UNDEFINED-Q5 | **MISSING** | — | — | Q5: target level + rubric sign-off + assessor |
| DN-018 | Capability inventory with maturity ratings | Semiannual | UNDEFINED-Q5 | **MISSING** | — | — | two-person assessment per rubric; evidence required |

## Strategy 2035 / Goal 5 recent

| Need | Element | Cadence | Definition | State | System | Steward | Notes |
|---|---|---|---|---|---|---|---|
| DN-017 | Capabilities delivered | On closeout | defined | **HAVE** | this system | Strategic Operations |  |
