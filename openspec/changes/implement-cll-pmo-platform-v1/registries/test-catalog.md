# Test Catalog

One registered test per requirement, identified `TEST-<REQ-ID>`. Each test is a
suite of cases covering every acceptance criterion of its requirement
(VER-001). Case ids follow the criterion: case for AC-INT-001-2 is
`TEST-INT-001/AC-INT-001-2`.

**Coverage:** 72 tests · 223 acceptance criteria cases.

**Types:** `unit`, `integration`, `contract`, `e2e`, `access`, `load`, `a11y`,
`audit` (manual review with artifact), `recon` (data reconciliation).

## Integrations

| Test | Requirement | Cases | Type | Gate |
|---|---|---|---|---|
| TEST-INT-001 | INT-001 | 4 | contract, integration, recon | GATE-1 |
| TEST-INT-002 | INT-002 | 4 | contract, access, integration | GATE-1 |
| TEST-INT-003 | INT-003 | 3 | contract, integration, audit | GATE-1 |
| TEST-INT-004 | INT-004 | 3 | contract, integration | GATE-1 |
| TEST-INT-005 | INT-005 | 3 | integration, e2e | GATE-6 |
| TEST-INT-006 | INT-006 | 3 | integration | GATE-6 |
| TEST-INT-007 | INT-007 | 3 | contract, integration | GATE-6 |
| TEST-INT-008 | INT-008 | 3 | integration, recon | GATE-1 |
| TEST-INT-009 | INT-009 | 3 | integration, access | GATE-6 |
| TEST-INT-010 | INT-010 | 3 | integration, e2e | GATE-1 |
| TEST-INT-011 | INT-011 | 3 | contract, audit | GATE-6 |

## Security

| Test | Requirement | Cases | Type | Gate |
|---|---|---|---|---|
| TEST-SEC-001 | SEC-001 | 4 | e2e, access | GATE-3 |
| TEST-SEC-002 | SEC-002 | 3 | access | GATE-3 |
| TEST-SEC-003 | SEC-003 | 3 | access, integration | GATE-3 / GATE-6 |
| TEST-SEC-004 | SEC-004 | 3 | audit, integration | GATE-3 |
| TEST-SEC-005 | SEC-005 | 3 | integration, audit | GATE-3 |
| TEST-SEC-006 | SEC-006 | 3 | unit, audit | GATE-3 |
| TEST-SEC-007 | SEC-007 | 3 | e2e, audit | GATE-3 |

## Executive dashboard

| Test | Requirement | Cases | Type | Gate |
|---|---|---|---|---|
| TEST-EXD-001 | EXD-001 | 4 | e2e, access | GATE-4 |
| TEST-EXD-002 | EXD-002 | 3 | unit, e2e | GATE-4 |
| TEST-EXD-003 | EXD-003 | 3 | e2e, access | GATE-4 |
| TEST-EXD-004 | EXD-004 | 3 | e2e | GATE-4 |
| TEST-EXD-005 | EXD-005 | 3 | e2e, recon | GATE-4 |
| TEST-EXD-006 | EXD-006 | 3 | unit, e2e | GATE-4 |
| TEST-EXD-007 | EXD-007 | 3 | integration, e2e | GATE-4 |
| TEST-EXD-008 | EXD-008 | 3 | a11y, audit | GATE-4 |

## Project registry

| Test | Requirement | Cases | Type | Gate |
|---|---|---|---|---|
| TEST-PRJ-001 | PRJ-001 | 4 | unit, e2e | GATE-2 |
| TEST-PRJ-002 | PRJ-002 | 3 | unit, e2e | GATE-2 |
| TEST-PRJ-003 | PRJ-003 | 3 | unit, integration | GATE-2 |
| TEST-PRJ-004 | PRJ-004 | 3 | integration, e2e | GATE-2 |
| TEST-PRJ-005 | PRJ-005 | 3 | integration, unit | GATE-2 |
| TEST-PRJ-006 | PRJ-006 | 3 | unit, e2e | GATE-2 |
| TEST-PRJ-007 | PRJ-007 | 3 | recon, unit | GATE-2 |
| TEST-PRJ-008 | PRJ-008 | 3 | integration, audit | GATE-2 |

## KPI governance

| Test | Requirement | Cases | Type | Gate |
|---|---|---|---|---|
| TEST-KPI-001 | KPI-001 | 4 | unit, e2e | GATE-2 |
| TEST-KPI-002 | KPI-002 | 3 | unit, recon | GATE-2 |
| TEST-KPI-003 | KPI-003 | 3 | unit | GATE-2 |
| TEST-KPI-004 | KPI-004 | 3 | unit, integration | GATE-5 |
| TEST-KPI-005 | KPI-005 | 3 | integration, e2e | GATE-5 |
| TEST-KPI-006 | KPI-006 | 3 | e2e, audit | GATE-5 |
| TEST-KPI-007 | KPI-007 | 3 | e2e | GATE-5 |

## Governance workflow

| Test | Requirement | Cases | Type | Gate |
|---|---|---|---|---|
| TEST-GOV-001 | GOV-001 | 4 | e2e, unit | GATE-5 |
| TEST-GOV-002 | GOV-002 | 3 | access, e2e | GATE-5 |
| TEST-GOV-003 | GOV-003 | 3 | unit, e2e | GATE-5 |
| TEST-GOV-004 | GOV-004 | 3 | integration, e2e | GATE-5 |
| TEST-GOV-005 | GOV-005 | 3 | e2e | GATE-5 |
| TEST-GOV-006 | GOV-006 | 3 | audit, integration | GATE-5 |

## Data quality

| Test | Requirement | Cases | Type | Gate |
|---|---|---|---|---|
| TEST-DQA-001 | DQA-001 | 3 | unit, audit | GATE-1 |
| TEST-DQA-002 | DQA-002 | 3 | integration, unit | GATE-3 |
| TEST-DQA-003 | DQA-003 | 3 | recon | GATE-3 / GATE-6 |
| TEST-DQA-004 | DQA-004 | 3 | integration, e2e | GATE-3 |
| TEST-DQA-005 | DQA-005 | 3 | e2e | GATE-3 |
| TEST-DQA-006 | DQA-006 | 3 | integration | GATE-3 |

## Board reporting

| Test | Requirement | Cases | Type | Gate |
|---|---|---|---|---|
| TEST-BRD-001 | BRD-001 | 3 | e2e, recon | GATE-7 |
| TEST-BRD-002 | BRD-002 | 3 | e2e | GATE-7 |
| TEST-BRD-003 | BRD-003 | 3 | integration, recon | GATE-7 |
| TEST-BRD-004 | BRD-004 | 3 | e2e, a11y | GATE-7 |
| TEST-BRD-005 | BRD-005 | 3 | integration, access | GATE-7 |
| TEST-BRD-006 | BRD-006 | 3 | e2e, unit | GATE-7 |
| TEST-BRD-007 | BRD-007 | 3 | e2e | GATE-7 |

## Nonfunctional

| Test | Requirement | Cases | Type | Gate |
|---|---|---|---|---|
| TEST-NFR-001 | NFR-001 | 3 | load | GATE-4 / GATE-8 |
| TEST-NFR-002 | NFR-002 | 3 | e2e, audit | GATE-7 / GATE-8 |
| TEST-NFR-003 | NFR-003 | 3 | load | GATE-2 |
| TEST-NFR-004 | NFR-004 | 3 | integration | GATE-0 |
| TEST-NFR-005 | NFR-005 | 3 | a11y, audit | GATE-4 |
| TEST-NFR-006 | NFR-006 | 3 | integration, audit | GATE-7 |
| TEST-NFR-007 | NFR-007 | 3 | audit, integration | GATE-0 |

## Verification and release governance

| Test | Requirement | Cases | Type | Gate |
|---|---|---|---|---|
| TEST-VER-001 | VER-001 | 3 | audit | GATE-8 |
| TEST-VER-002 | VER-002 | 3 | audit, integration | GATE-8 |
| TEST-VER-003 | VER-003 | 3 | e2e, audit | GATE-8 |
| TEST-REL-001 | REL-001 | 3 | audit | GATE-8 |
| TEST-REL-002 | REL-002 | 3 | e2e, audit | GATE-0 / GATE-8 |

## Case count reconciliation

| Capability | Tests | Cases |
|---|---|---|
| integrations | 11 | 35 |
| security | 7 | 22 |
| executive-dashboard | 8 | 25 |
| project-registry | 8 | 25 |
| kpi-governance | 7 | 22 |
| governance-workflow | 6 | 19 |
| data-quality | 6 | 18 |
| board-reporting | 7 | 21 |
| nonfunctional | 7 | 21 |
| verification | 3 | 9 |
| release-governance | 2 | 6 |
| **Total** | **72** | **223** |
