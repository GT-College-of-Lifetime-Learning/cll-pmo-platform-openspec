# Test Strategy

**Task:** T-008 (Owner `QALEAD`, Verifier `PLATFORM`)
**Requirements:** VER-001 — acceptance criteria AC-VER-001-1, AC-VER-001-2
**Tests:** TEST-VER-001 · **Evidence:** EV-VER-001 · **Gates:** GATE-0, GATE-8

## Scope

The baseline defines **72 requirements**, **223 acceptance criteria**, **72
registered tests** and **72 evidence records**. This strategy governs how those
tests are written, run and evidenced.

Traceability chain:

```
requirement -> AC-<REQ>-<n> -> TEST-<REQ> -> EV-<REQ> -> GATE-n
```

One registered test per requirement, named `TEST-<REQ-ID>`. Each registered
test is a suite whose cases map one-to-one onto that requirement's acceptance
criteria. A case is named for its criterion: the case for AC-INT-001-2 is
`TEST-INT-001/AC-INT-001-2`.

## Test types

The registry uses nine types. Each maps to a concrete technology under D8:

| Type | Meaning | Implementation |
|---|---|---|
| `unit` | Pure logic, no I/O | xunit (API), Vitest (web) |
| `integration` | Crosses a process or service boundary | xunit + Testcontainers / Azure SQL test database |
| `contract` | Payload conforms to the agreed data contract | Schema validation against `contracts/integration-data-contracts.md` |
| `e2e` | User-visible path through the deployed system | Playwright |
| `access` | Role and row-level scoping enforcement | xunit with per-role principals against SQL row-level security |
| `load` | Throughput and latency under concurrency | Azure Load Testing |
| `a11y` | WCAG 2.2 AA conformance | axe-core, automated plus manual audit |
| `audit` | Manual review producing a signed artifact | Reviewed document in the evidence store |
| `recon` | Reconciliation between the platform and a source | SQL reconciliation with a declared tolerance |

## Coverage by capability

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

The authoritative per-test mapping — requirement, case count, type and gate —
is `openspec/changes/implement-cll-pmo-platform-v1/registries/test-catalog.md`.
That registry is the catalog skeleton required by AC-VER-001-1; this document
is the strategy required by AC-VER-001-2. The two are kept in sync: adding a
requirement requires adding its test row before the requirement can be marked
complete.

## Where tests live

| Suite | Location |
|---|---|
| API unit and integration | `tests/CllPmo.Api.Tests/` |
| Web unit | `web/src/**/*.test.tsx` |
| End-to-end | `tests/e2e/` (added in Phase 04) |
| Access control | `tests/CllPmo.Access.Tests/` (added in Phase 03) |
| Load | `tests/load/` (added in Phase 02) |
| Reconciliation | `tests/recon/` (added in Phase 01) |

Directory names mirror the test type so a registry row resolves to a path
without a lookup.

## Execution

| Trigger | Suites |
|---|---|
| Every pull request | `unit`, `contract`, accessibility smoke |
| Merge to `main` | above plus `integration`, `access` |
| Nightly | above plus `e2e`, `recon` |
| Before a gate | every suite in that gate's scope, plus `load` and `a11y` where in scope |

Current CI state: `unit` runs for the API; web typecheck and build run; secret
scanning is blocking; the accessibility smoke is advisory until GATE-4. The
remaining types are wired as their phases deliver.

## Entry and exit criteria

**Entry.** A requirement may enter test when its acceptance criteria are
written, its registry row exists, and its evidence record id is allocated.

**Exit.** A requirement exits test when every acceptance criterion has a
passing case, the evidence artifact is attached, and no severity-1 or
severity-2 defect is open against it.

## Defect severity

| Severity | Definition | Gate impact |
|---|---|---|
| 1 | Wrong board-facing number, data loss, or access control failure | Blocks every gate |
| 2 | Requirement unusable with no workaround | Blocks its own gate |
| 3 | Requirement degraded with a workaround | Waiver with expiry |
| 4 | Cosmetic | Does not block |

Severity 1 and 2 defects must be closed before GATE-8 (UAT exit criterion).

## Evidence

Each registered test produces evidence `EV-<REQ-ID>`: the run output, its
commit SHA, the environment, the date, and the reviewer for `audit` and `a11y`
types. Evidence is attached before a task is marked complete, and before its
gate closes — per the apply guidance in `openspec/config.yaml`.
