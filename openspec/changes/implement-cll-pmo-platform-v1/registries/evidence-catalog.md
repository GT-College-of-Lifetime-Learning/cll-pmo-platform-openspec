# Evidence Catalog

One evidence record per requirement, identified `EV-<REQ-ID>`. An evidence
record holds the dated artifacts proving every acceptance criterion of that
requirement was verified (VER-002). Evidence is retained 7 years and becomes
immutable when its gate closes.

**Required fields on every record:** criterion id, test id, executor, execution
date, result, build or environment reference, artifact location.

## Evidence records

| Evidence | Requirement | Artifact form | Produced by | Countersigned by | Gate |
|---|---|---|---|---|---|
| EV-INT-001 | INT-001 | Run logs + monthly reconciliation report | `INTENG` | `DATAGOV` | GATE-1 |
| EV-INT-002 | INT-002 | Run logs + access test matrix + suppression sample | `INTENG` | `SECARCH` | GATE-1 |
| EV-INT-003 | INT-003 | Contract validation log + privacy attestation | `DATAENG` | `DATAGOV` | GATE-1 |
| EV-INT-004 | INT-004 | Run logs + quarantine sample | `INTENG` | `DATAGOV` | GATE-1 |
| EV-INT-005 | INT-005 | Webhook latency report + write-back restriction test | `INTENG` | `PORTFOLIO` | GATE-6 |
| EV-INT-006 | INT-006 | Hourly run statistics over 14 days | `INTENG` | `DATAENG` | GATE-6 |
| EV-INT-007 | INT-007 | Weekly load log + suppression verification | `DATAENG` | `DATAGOV` | GATE-6 |
| EV-INT-008 | INT-008 | Dimension load log + referential integrity report | `DATAENG` | `DATAGOV` | GATE-1 |
| EV-INT-009 | INT-009 | Group sync log + revocation timing test | `INTENG` | `SECARCH` | GATE-6 |
| EV-INT-010 | INT-010 | Scheduler dependency test + backfill replay report | `INTENG` | `DATAENG` | GATE-1 |
| EV-INT-011 | INT-011 | Dual-run reconciliation + version stamp sample | `DATAENG` | `DATAGOV` | GATE-6 |
| EV-SEC-001 | SEC-001 | SSO configuration export + session expiry test | `SECARCH` | `PLATFORM` | GATE-3 |
| EV-SEC-002 | SEC-002 | Role-permission matrix + denial log sample | `SECARCH` | `DATAGOV` | GATE-3 |
| EV-SEC-003 | SEC-003 | Scoping test matrix across dashboard, API and export | `SECARCH` | `QALEAD` | GATE-3 |
| EV-SEC-004 | SEC-004 | TLS scan + encryption configuration attestation | `SECARCH` | `PLATFORM` | GATE-3 |
| EV-SEC-005 | SEC-005 | Audit log schema + 30-day completeness sample | `SECARCH` | `DATAGOV` | GATE-3 |
| EV-SEC-006 | SEC-006 | Secret scan results + rotation schedule export | `SECARCH` | `RELMGR` | GATE-3 |
| EV-SEC-007 | SEC-007 | Recertification campaign record + removal log | `SECARCH` | `SPONSOR` | GATE-3 |
| EV-EXD-001 | EXD-001 | Scoped render screenshots + indicator rule documentation | `BILEAD` | `QALEAD` | GATE-4 |
| EV-EXD-002 | EXD-002 | Version-boundary chart sample + gap handling test | `BILEAD` | `DATAGOV` | GATE-4 |
| EV-EXD-003 | EXD-003 | Drill-down session recording + URL state test | `BILEAD` | `QALEAD` | GATE-4 |
| EV-EXD-004 | EXD-004 | Heat map test results + RAID linkage sample | `BILEAD` | `PORTFOLIO` | GATE-4 |
| EV-EXD-005 | EXD-005 | Financial view reconciliation + suppression render sample | `BILEAD` | `DATAENG` | GATE-4 |
| EV-EXD-006 | EXD-006 | Timeline slip calculation test + overdue flag sample | `BILEAD` | `PORTFOLIO` | GATE-4 |
| EV-EXD-007 | EXD-007 | Degraded-state simulation results | `BILEAD` | `DATAGOV` | GATE-4 |
| EV-EXD-008 | EXD-008 | WCAG 2.2 AA audit report + keyboard walkthrough | `A11Y` | `BILEAD` | GATE-4 |
| EV-PRJ-001 | PRJ-001 | Registry reconciliation to Smartsheet inventory | `APPENG` | `PORTFOLIO` | GATE-2 |
| EV-PRJ-002 | PRJ-002 | State machine test results | `APPENG` | `QALEAD` | GATE-2 |
| EV-PRJ-003 | PRJ-003 | Taxonomy mapping report + retirement handling test | `APPENG` | `STRATOFF` | GATE-2 |
| EV-PRJ-004 | PRJ-004 | Ownership validation test + gap exception sample | `APPENG` | `PORTFOLIO` | GATE-2 |
| EV-PRJ-005 | PRJ-005 | Baseline capture record + slip calculation test | `APPENG` | `PORTFOLIO` | GATE-2 |
| EV-PRJ-006 | PRJ-006 | RAID test results + overdue review sample | `APPENG` | `PORTFOLIO` | GATE-2 |
| EV-PRJ-007 | PRJ-007 | Attribution reconciliation (attributed + unallocated = total) | `DATAENG` | `DATAGOV` | GATE-2 |
| EV-PRJ-008 | PRJ-008 | History reconstruction test + immutability attestation | `APPENG` | `SECARCH` | GATE-2 |
| EV-KPI-001 | KPI-001 | Registry export + cross-surface consistency test | `DATAGOV` | `STRATOFF` | GATE-2 |
| EV-KPI-002 | KPI-002 | Lineage record sample + recomputation proof | `DATAENG` | `DATAGOV` | GATE-2 |
| EV-KPI-003 | KPI-003 | Effective-dated target test results | `DATAGOV` | `QALEAD` | GATE-2 |
| EV-KPI-004 | KPI-004 | Cadence run log + closed-period immutability test | `DATAENG` | `DATAGOV` | GATE-5 |
| EV-KPI-005 | KPI-005 | Stewardship register + gap block test | `DATAGOV` | `PORTFOLIO` | GATE-5 |
| EV-KPI-006 | KPI-006 | Restatement record sample + disclosure render | `DATAGOV` | `SPONSOR` | GATE-5 |
| EV-KPI-007 | KPI-007 | Narrative requirement log + approval block test | `DATAGOV` | `PORTFOLIO` | GATE-5 |
| EV-GOV-001 | GOV-001 | Gate configuration export + decision immutability test | `APPENG` | `PORTFOLIO` | GATE-5 |
| EV-GOV-002 | GOV-002 | Sequence and delegation test + self-approval rejection log | `APPENG` | `SECARCH` | GATE-5 |
| EV-GOV-003 | GOV-003 | Routing test across materiality thresholds | `APPENG` | `PORTFOLIO` | GATE-5 |
| EV-GOV-004 | GOV-004 | SLA breach simulation + escalation trail sample | `APPENG` | `QALEAD` | GATE-5 |
| EV-GOV-005 | GOV-005 | Generated agenda sample + carried-over action test | `PORTFOLIO` | `SPONSOR` | GATE-5 |
| EV-GOV-006 | GOV-006 | Decision register export + deletion-prevention attestation | `APPENG` | `SECARCH` | GATE-5 |
| EV-DQA-001 | DQA-001 | Rule catalog export + coverage check per feed | `DATAGOV` | `DATAENG` | GATE-1 |
| EV-DQA-002 | DQA-002 | Validation run report (evaluated/clean/quarantined/flagged) | `DATAENG` | `DATAGOV` | GATE-3 |
| EV-DQA-003 | DQA-003 | Reconciliation results per registered cadence | `DATAENG` | `DATAGOV` | GATE-3 |
| EV-DQA-004 | DQA-004 | Scorecard export + degraded-source alert sample | `DATAGOV` | `PLATFORM` | GATE-3 |
| EV-DQA-005 | DQA-005 | Exception queue export + escalation sample | `DATAGOV` | `SPONSOR` | GATE-3 |
| EV-DQA-006 | DQA-006 | Replay run report + idempotency proof | `DATAENG` | `QALEAD` | GATE-3 |
| EV-BRD-001 | BRD-001 | Assembled package + snapshot traceability report | `BILEAD` | `PORTFOLIO` | GATE-7 |
| EV-BRD-002 | BRD-002 | Narrative approval trail + re-approval test | `PORTFOLIO` | `SPONSOR` | GATE-7 |
| EV-BRD-003 | BRD-003 | Snapshot certification record + reproduction test | `DATAENG` | `DATAGOV` | GATE-7 |
| EV-BRD-004 | BRD-004 | Exported artifacts + checksum register | `BILEAD` | `QALEAD` | GATE-7 |
| EV-BRD-005 | BRD-005 | Distribution log + unapproved-publication rejection test | `BILEAD` | `SECARCH` | GATE-7 |
| EV-BRD-006 | BRD-006 | Comparative rendering sample with restatement disclosure | `BILEAD` | `DATAGOV` | GATE-7 |
| EV-BRD-007 | BRD-007 | Reporting calendar + readiness checklist output | `PORTFOLIO` | `SPONSOR` | GATE-7 |
| EV-NFR-001 | NFR-001 | Load test report at 150 concurrent users | `PLATFORM` | `QALEAD` | GATE-4 |
| EV-NFR-002 | NFR-002 | Availability report + restore test record | `PLATFORM` | `RELMGR` | GATE-7 |
| EV-NFR-003 | NFR-003 | Scale test report at 500 projects / 250 KPIs / 5 years | `PLATFORM` | `DATAENG` | GATE-2 |
| EV-NFR-004 | NFR-004 | Telemetry sample + watchdog alert test | `PLATFORM` | `RELMGR` | GATE-0 |
| EV-NFR-005 | NFR-005 | Accessibility audit report + CI check results | `A11Y` | `QALEAD` | GATE-4 |
| EV-NFR-006 | NFR-006 | Retention configuration + purge log sample | `PLATFORM` | `SECARCH` | GATE-7 |
| EV-NFR-007 | NFR-007 | Environment parity report + drift reconciliation record | `PLATFORM` | `RELMGR` | GATE-0 |
| EV-VER-001 | VER-001 | Coverage report: 72 requirements / 223 criteria | `QALEAD` | `SPONSOR` | GATE-8 |
| EV-VER-002 | VER-002 | Traceability matrix (requirement → criterion → test → evidence → gate) | `QALEAD` | `RELMGR` | GATE-8 |
| EV-VER-003 | VER-003 | UAT results + signed sign-off records | `QALEAD` | `SPONSOR` | GATE-8 |
| EV-REL-001 | REL-001 | Gate closure records + waiver register | `RELMGR` | `SPONSOR` | GATE-8 |
| EV-REL-002 | REL-002 | Release record, rollback rehearsal, freeze enforcement log | `RELMGR` | `PLATFORM` | GATE-8 |

**Total:** 72 evidence records covering 223 acceptance criteria.

## Immutability

When a gate closes, every evidence record in its scope is locked. A later
correction is a new dated record referencing the original; the original is never
amended (AC-VER-002-3).
