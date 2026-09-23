# Release Gate Registry

Nine gates, one per phase. A gate closes only when every in-scope task is
complete and every in-scope acceptance criterion is covered, evidenced and
passing (REL-001). Deficiencies require a recorded waiver with a compensating
control and an expiry date.

| Gate | Phase | Task scope | Requirement scope | Approvers (in order) |
|---|---|---|---|---|
| GATE-0 | 00 Foundation | T-001 – T-008 | REL-002, NFR-004, NFR-007, VER-001 | `PLATFORM` → `SECARCH` → `SPONSOR` |
| GATE-1 | 01 Source Alignment | T-009 – T-017 | INT-001 – INT-004, INT-008, INT-010, INT-011, DQA-001 | `DATAENG` → `DATAGOV` → `SPONSOR` |
| GATE-2 | 02 Core Platform | T-018 – T-031 | PRJ-001 – PRJ-008, KPI-001 – KPI-003, NFR-003 | `APPENG` → `PORTFOLIO` → `SPONSOR` |
| GATE-3 | 03 Security & Quality | T-032 – T-043 | SEC-001 – SEC-007, DQA-002 – DQA-006 | `SECARCH` → `DATAGOV` → `SPONSOR` |
| GATE-4 | 04 Dashboard | T-044 – T-055 | EXD-001 – EXD-008, NFR-001, NFR-005 | `BILEAD` → `A11Y` → `SPONSOR` |
| GATE-5 | 05 Governance | T-056 – T-066 | GOV-001 – GOV-006, KPI-005 – KPI-007 | `APPENG` → `PORTFOLIO` → `SPONSOR` |
| GATE-6 | 06 Integrations | T-067 – T-080 | INT-005 – INT-007, INT-009 – INT-011, DQA-003, SEC-003 | `DATAENG` → `SECARCH` → `SPONSOR` |
| GATE-7 | 07 Reporting & Operations | T-081 – T-091 | BRD-001 – BRD-007, NFR-002, NFR-006 | `BILEAD` → `PORTFOLIO` → `SPONSOR` |
| GATE-8 | 08 Verification & Release | T-092 – T-101 | VER-001 – VER-003, REL-001, REL-002, NFR-001, NFR-002 | `QALEAD` → `RELMGR` → `SPONSOR` |

## Entry criteria and required evidence

### GATE-0 — Delivery capability established
**Entry criteria:** environments provisioned with parity; CI/CD pipeline green on a trial change; security intake submitted; repository and OpenSpec baseline merged; test strategy drafted.
**Required evidence:** EV-NFR-007, EV-NFR-004, EV-REL-002, EV-VER-001.
**Blocks:** all subsequent phases.

### GATE-1 — Source agreement
**Entry criteria:** all eleven data contracts countersigned by source owners; landing zone receiving from the first four sources; DQ rule catalog established with blocking rules for contracted keys; scheduling and dependency order implemented.
**Required evidence:** EV-INT-001 – EV-INT-004, EV-INT-008, EV-INT-010, EV-INT-011, EV-DQA-001.
**Blocks:** GATE-2 (the portfolio model cannot be trusted without agreed sources).

### GATE-2 — One record per project
**Entry criteria:** portfolio model deployed; project registry populated and reconciled to the legacy Smartsheet inventory with zero unmatched projects; KPI registry live with definitions, lineage and targets; scale test passed.
**Required evidence:** EV-PRJ-001 – EV-PRJ-008, EV-KPI-001 – EV-KPI-003, EV-NFR-003.
**Blocks:** GATE-4, GATE-5.

### GATE-3 — Trustworthy and protected
**Entry criteria:** SSO live; six roles derived from Entra ID groups; row-level scoping enforced at the data layer; audit logging operational; secrets managed and scanned; DQ validation, scorecard, exception queue and replay operational.
**Required evidence:** EV-SEC-001 – EV-SEC-007, EV-DQA-002 – EV-DQA-006.
**Blocks:** GATE-4 (no user-facing surface before access control), GATE-6, GATE-7.

### GATE-4 — Leadership self-service
**Entry criteria:** all eight dashboard requirements implemented; performance targets met under load; WCAG 2.2 AA audit clean; freshness and completeness indicators wired to real feed state.
**Required evidence:** EV-EXD-001 – EV-EXD-008, EV-NFR-001, EV-NFR-005.
**Blocks:** GATE-7.

### GATE-5 — Decisions on the record
**Entry criteria:** stage gates G0–G5 configured; approval sequences and delegation enforced; change request routing by materiality live; escalation SLAs active; KPI stewardship and narrative capture operational.
**Required evidence:** EV-GOV-001 – EV-GOV-006, EV-KPI-005 – EV-KPI-007.
**Blocks:** GATE-7.

### GATE-6 — Self-refreshing portfolio
**Entry criteria:** all eleven integrations live; Smartsheet write-back limited to four fields and verified; contract versioning and dual-run proven; backfill and replay proven; 14 consecutive successful scheduled run days; reconciliations within tolerance.
**Required evidence:** EV-INT-005 – EV-INT-007, EV-INT-009 – EV-INT-011, EV-DQA-003, EV-SEC-003.
**Blocks:** GATE-7.

### GATE-7 — Board package from the platform
**Entry criteria:** snapshot creation and certification operational; package assembly, narrative approval, exports and distribution working end to end; one shadow package reconciled to the manual package; availability and retention controls operating.
**Required evidence:** EV-BRD-001 – EV-BRD-007, EV-NFR-002, EV-NFR-006.
**Blocks:** GATE-8.

### GATE-8 — Strategy 2035 on the record
**Entry criteria:** traceability matrix complete across 72 requirements and 223 acceptance criteria; UAT complete with no open severity-1 or severity-2 defects; performance and accessibility re-validated on the release build; rollback rehearsed; change freeze process proven.
**Required evidence:** EV-VER-001 – EV-VER-003, EV-REL-001, EV-REL-002, EV-NFR-001, EV-NFR-002.
**Blocks:** production go-live.

## Waiver record format

A waiver records: gate, deficiency, affected requirements and criteria,
compensating control, approver, approval date, expiry date and the task that
will close it. An expired waiver reopens the gate.
