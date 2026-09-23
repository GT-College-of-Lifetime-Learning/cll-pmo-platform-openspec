# Tasks: implement-cll-pmo-platform-v1

The canonical implementation checklist — 101 tasks across 9 phases.

Each line carries its stable task id (`T-NNN`), owner and verifier role keys from
`registries/ownership.md`, and its release gate. The full field set for every
task — Owner, Verifier, Dependencies, Requirements, Acceptance Criteria, Tests,
Evidence, Release Gates — lives in the per-phase file linked at the head of each
section. Check a task off here **and** in its phase file, in the same commit as
the finished work.

**Totals:** 101 tasks · 9 phases · 9 release gates · 72 requirements · 223 acceptance criteria

## 1. Phase 00 — Foundation

Detail: [`tasks/phase-00-foundation.md`](tasks/phase-00-foundation.md) · Gate: GATE-0 · 8 tasks

- [ ] 1.1 T-001 Provision development, test and production environments with documented parity (`PLATFORM`/`RELMGR`)
- [ ] 1.2 T-002 Register the platform in Entra ID and create the six role security groups (`SECARCH`/`PLATFORM`)
- [ ] 1.3 T-003 Stand up the CI/CD pipeline with build, test, secret scanning and accessibility checks (`RELMGR`/`PLATFORM`)
- [ ] 1.4 T-004 Implement the structured run-record and telemetry framework (`PLATFORM`/`DATAENG`)
- [ ] 1.5 T-005 Implement watchdog alerting for failed and missing runs to the on-call owner (`PLATFORM`/`RELMGR`)
- [ ] 1.6 T-006 Establish release records, commit tagging and the rollback procedure (`RELMGR`/`PLATFORM`)
- [ ] 1.7 T-007 Submit and clear the institutional security intake review (`SECARCH`/`SPONSOR`)
- [ ] 1.8 T-008 Author the test strategy and register the 72-test catalog skeleton (`QALEAD`/`PLATFORM`)

## 2. Phase 01 — Source Alignment

Detail: [`tasks/phase-01-source-alignment.md`](tasks/phase-01-source-alignment.md) · Gate: GATE-1 · 9 tasks

- [ ] 2.1 T-009 Ingest IR conformed dimensions and enforce referential integrity (`DATAENG`/`DATAGOV`)
- [ ] 2.2 T-010 Build Workday Financials ingestion with the 90-day trailing re-read (`INTENG`/`DATAENG`)
- [ ] 2.3 T-011 Build Workday HCM ingestion with restricted-data handling (`INTENG`/`SECARCH`)
- [ ] 2.4 T-012 Build Banner enrollment ingestion with a fail-closed identifiable-data guard (`DATAENG`/`DATAGOV`)
- [ ] 2.5 T-013 Build Salesforce pipeline ingestion with incremental high-water mark extraction (`INTENG`/`DATAENG`)
- [ ] 2.6 T-014 Implement the scheduler with fixed dependency order and hold-on-failure (`INTENG`/`PLATFORM`)
- [ ] 2.7 T-015 Implement bounded retry with backoff and landing-zone backfill replay (`INTENG`/`DATAENG`)
- [ ] 2.8 T-016 Implement contract validation, version stamping and fail-closed breach handling (`DATAENG`/`DATAGOV`)
- [ ] 2.9 T-017 Establish the data quality rule catalog with blocking rules for all contracted keys (`DATAGOV`/`DATAENG`)

## 3. Phase 02 — Core Platform

Detail: [`tasks/phase-02-core-platform.md`](tasks/phase-02-core-platform.md) · Gate: GATE-2 · 14 tasks

- [ ] 3.1 T-018 Load the Strategy 2035 pillar and objective taxonomy with effective dating (`APPENG`/`STRATOFF`)
- [ ] 3.2 T-019 Implement the project record and immutable `project_id` issuance (`APPENG`/`PORTFOLIO`)
- [ ] 3.3 T-020 Implement duplicate detection and downstream rename reversion (`APPENG`/`PORTFOLIO`)
- [ ] 3.4 T-021 Implement the lifecycle state machine with gate preconditions (`APPENG`/`QALEAD`)
- [ ] 3.5 T-022 Implement transition history with actor, timestamp and reason capture (`APPENG`/`SECARCH`)
- [ ] 3.6 T-023 Implement objective retirement flagging and the realignment queue (`APPENG`/`STRATOFF`)
- [ ] 3.7 T-024 Implement ownership and RACI with HCM person validation and gap exceptions (`APPENG`/`PORTFOLIO`)
- [ ] 3.8 T-025 Implement the milestone mirror, baseline capture and slip computation (`APPENG`/`PORTFOLIO`)
- [ ] 3.9 T-026 Implement the RAID log with ratings, review dates and closure retention (`APPENG`/`PORTFOLIO`)
- [ ] 3.10 T-027 Implement funding linkage, worktag attribution and unallocated spend reporting (`DATAENG`/`DATAGOV`)
- [ ] 3.11 T-028 Implement immutable field-level history and as-of reconstruction (`APPENG`/`SECARCH`)
- [ ] 3.12 T-029 Implement the KPI definition registry with stewardship and publication rules (`DATAGOV`/`STRATOFF`)
- [ ] 3.13 T-030 Implement KPI lineage capture and reproducible recomputation (`DATAENG`/`DATAGOV`)
- [ ] 3.14 T-031 Implement effective-dated targets and thresholds, and run the scale test at ceilings (`DATAGOV`/`PLATFORM`)

## 4. Phase 03 — Security & Quality

Detail: [`tasks/phase-03-security-quality.md`](tasks/phase-03-security-quality.md) · Gate: GATE-3 · 12 tasks

- [ ] 4.1 T-032 Implement OIDC single sign-on with PKCE and the session policy (`SECARCH`/`APPENG`)
- [ ] 4.2 T-033 Implement workload identities and break-glass account alerting (`SECARCH`/`PLATFORM`)
- [ ] 4.3 T-034 Implement the six roles derived from Entra ID groups with authorisation checks (`SECARCH`/`DATAGOV`)
- [ ] 4.4 T-035 Implement row-level scoping predicates at the data layer (`SECARCH`/`APPENG`)
- [ ] 4.5 T-036 Verify scoping parity across dashboard, API and export paths (`QALEAD`/`SECARCH`)
- [ ] 4.6 T-037 Enforce TLS and at-rest encryption including restricted-source key separation (`SECARCH`/`PLATFORM`)
- [ ] 4.7 T-038 Implement the append-only audit log with required fields and 7-year retention (`SECARCH`/`DATAGOV`)
- [ ] 4.8 T-039 Implement secret storage, 90-day rotation with 75-day alerting, and annual key re-wrap (`SECARCH`/`RELMGR`)
- [ ] 4.9 T-040 Implement quarterly recertification campaigns with automatic removal (`SECARCH`/`SPONSOR`)
- [ ] 4.10 T-041 Implement ingestion-time rule evaluation, quarantine and per-run reporting (`DATAENG`/`DATAGOV`)
- [ ] 4.11 T-042 Implement the data quality scorecard, degraded-source marking and 24-month history (`DATAGOV`/`PLATFORM`)
- [ ] 4.12 T-043 Implement the exception queue, escalation, quarantine replay and replay idempotency (`DATAGOV`/`QALEAD`)

## 5. Phase 04 — Dashboard

Detail: [`tasks/phase-04-dashboard.md`](tasks/phase-04-dashboard.md) · Gate: GATE-4 · 12 tasks

- [ ] 5.1 T-044 Implement portfolio health computation rules and the pillar overview (`BILEAD`/`QALEAD`)
- [ ] 5.2 T-045 Implement indicator explainability and no-data-in-scope rendering (`BILEAD`/`PORTFOLIO`)
- [ ] 5.3 T-046 Implement KPI trend charts with target and threshold bands and version marks (`BILEAD`/`DATAGOV`)
- [ ] 5.4 T-047 Implement pillar to objective to project drill-down with context preservation (`BILEAD`/`QALEAD`)
- [ ] 5.5 T-048 Implement URL-addressable dashboard state (`BILEAD`/`APPENG`)
- [ ] 5.6 T-049 Implement the risk and issue heat map with cell drill-in and closed-items view (`BILEAD`/`PORTFOLIO`)
- [ ] 5.7 T-050 Implement the financial burn and variance view with closed-period immutability (`BILEAD`/`DATAENG`)
- [ ] 5.8 T-051 Implement explicit suppression rendering for effort figures (`BILEAD`/`SECARCH`)
- [ ] 5.9 T-052 Implement the milestone timeline with baseline versus current dates and overdue flags (`BILEAD`/`PORTFOLIO`)
- [ ] 5.10 T-053 Implement the freshness and completeness indicator wired to run and data quality state (`BILEAD`/`DATAGOV`)
- [ ] 5.11 T-054 Execute performance validation at 150 concurrent users (`PLATFORM`/`QALEAD`)
- [ ] 5.12 T-055 Remediate WCAG 2.2 AA findings and verify keyboard and non-colour status conveyance (`A11Y`/`BILEAD`)

## 6. Phase 05 — Governance

Detail: [`tasks/phase-05-governance.md`](tasks/phase-05-governance.md) · Gate: GATE-5 · 11 tasks

- [ ] 6.1 T-056 Configure stage gates G0 to G5 with their required evidence sets (`APPENG`/`PORTFOLIO`)
- [ ] 6.2 T-057 Implement immutable gate decision records and lifecycle transition blocking (`APPENG`/`SECARCH`)
- [ ] 6.3 T-058 Implement ordered approval sequences per gate and decision type (`APPENG`/`PORTFOLIO`)
- [ ] 6.4 T-059 Implement time-bounded delegation and self-approval prevention (`APPENG`/`SECARCH`)
- [ ] 6.5 T-060 Implement change request intake and materiality-based routing (`APPENG`/`PORTFOLIO`)
- [ ] 6.6 T-061 Implement service level tracking, automatic escalation and the escalation trail (`APPENG`/`QALEAD`)
- [ ] 6.7 T-062 Implement agenda generation and action item tracking (`PORTFOLIO`/`SPONSOR`)
- [ ] 6.8 T-063 Implement decision retention, the exportable register and deletion prevention (`APPENG`/`SECARCH`)
- [ ] 6.9 T-064 Implement KPI measurement cadence with closed-period immutability and missing-measure records (`DATAENG`/`DATAGOV`)
- [ ] 6.10 T-065 Implement stewardship enforcement and stewardship-gap blocking (`DATAGOV`/`PORTFOLIO`)
- [ ] 6.11 T-066 Implement restatement records, disclosure and the variance narrative workflow (`DATAGOV`/`SPONSOR`)

## 7. Phase 06 — Integrations

Detail: [`tasks/phase-06-integrations.md`](tasks/phase-06-integrations.md) · Gate: GATE-6 · 14 tasks

- [ ] 7.1 T-067 Build Smartsheet plan ingestion, four times daily plus webhooks (`INTENG`/`PORTFOLIO`)
- [ ] 7.2 T-068 Implement Smartsheet write-back limited to the four platform-owned fields (`INTENG`/`DATAENG`)
- [ ] 7.3 T-069 Wire Smartsheet milestones into registry baseline and slip computation (`APPENG`/`PORTFOLIO`)
- [ ] 7.4 T-070 Build ServiceNow hourly ingestion with concurrent-run prevention (`INTENG`/`DATAENG`)
- [ ] 7.5 T-071 Implement Salesforce stage-domain quarantine and unlinked opportunity reporting (`INTENG`/`DATAGOV`)
- [ ] 7.6 T-072 Build Canvas weekly engagement ingestion with small-cell suppression (`DATAENG`/`DATAGOV`)
- [ ] 7.7 T-073 Build the Entra ID delta sync of users and role group memberships (`INTENG`/`SECARCH`)
- [ ] 7.8 T-074 Implement orphan role revocation and session termination on account disable (`SECARCH`/`QALEAD`)
- [ ] 7.9 T-075 Implement the contract dual-run and deprecation workflow (`DATAENG`/`DATAGOV`)
- [ ] 7.10 T-076 Implement monthly financial reconciliation against the Workday ledger (`DATAENG`/`DATAGOV`)
- [ ] 7.11 T-077 Implement the remaining registered reconciliations with tolerance-based blocking (`DATAENG`/`DATAGOV`)
- [ ] 7.12 T-078 Implement ownership-violation rejection and logging for source-owned fields (`DATAENG`/`SECARCH`)
- [ ] 7.13 T-079 Operate 14 consecutive successful scheduled run days and evidence stability (`INTENG`/`DATAENG`)
- [ ] 7.14 T-080 Re-verify row-level scoping against live integrated data (`SECARCH`/`QALEAD`)

## 8. Phase 07 — Reporting & Operations

Detail: [`tasks/phase-07-reporting-operations.md`](tasks/phase-07-reporting-operations.md) · Gate: GATE-7 · 11 tasks

- [ ] 8.1 T-081 Build the reporting calendar aligned to Finance close and Board meeting dates (`PORTFOLIO`/`SPONSOR`)
- [ ] 8.2 T-082 Implement the readiness checklist with blockers and a 10-business-day lead (`PORTFOLIO`/`SPONSOR`)
- [ ] 8.3 T-083 Implement snapshot creation, certification and immutability (`DATAENG`/`DATAGOV`)
- [ ] 8.4 T-084 Implement package assembly from a single certified snapshot (`BILEAD`/`PORTFOLIO`)
- [ ] 8.5 T-085 Implement narrative capture, approval routing and publication blocking (`PORTFOLIO`/`SPONSOR`)
- [ ] 8.6 T-086 Implement PDF, PPTX and XLSX exports with stamping and checksums (`BILEAD`/`QALEAD`)
- [ ] 8.7 T-087 Implement SharePoint distribution with approval gating and access logging (`BILEAD`/`SECARCH`)
- [ ] 8.8 T-088 Implement comparatives from published snapshots with restatement disclosure (`BILEAD`/`DATAGOV`)
- [ ] 8.9 T-089 Implement retention enforcement and purge logging per data class (`PLATFORM`/`SECARCH`)
- [ ] 8.10 T-090 Implement availability monitoring and the quarterly restore test (`PLATFORM`/`RELMGR`)
- [ ] 8.11 T-091 Produce the shadow board package and reconcile it to the manual package (`BILEAD`/`PORTFOLIO`)

## 9. Phase 08 — Verification & Release

Detail: [`tasks/phase-08-verification-release.md`](tasks/phase-08-verification-release.md) · Gate: GATE-8 · 10 tasks

- [ ] 9.1 T-092 Complete test coverage for all 72 requirements and 223 acceptance criteria (`QALEAD`/`SPONSOR`)
- [ ] 9.2 T-093 Implement gate blocking on uncovered, unevidenced or failing criteria (`RELMGR`/`QALEAD`)
- [ ] 9.3 T-094 Generate the traceability matrix and close every chain gap (`QALEAD`/`RELMGR`)
- [ ] 9.4 T-095 Lock evidence on gate closure and enforce 7-year evidence retention (`QALEAD`/`SECARCH`)
- [ ] 9.5 T-096 Re-run performance validation on the release build (`PLATFORM`/`QALEAD`)
- [ ] 9.6 T-097 Re-run the accessibility audit on the release build including exported artifacts (`A11Y`/`QALEAD`)
- [ ] 9.7 T-098 Execute user acceptance testing across the six roles and triage defects (`QALEAD`/`SPONSOR`)
- [ ] 9.8 T-099 Record UAT sign-off with signatory, role, date and build tested (`QALEAD`/`SPONSOR`)
- [ ] 9.9 T-100 Rehearse rollback, enforce the reporting change freeze and reconcile environment drift (`RELMGR`/`PLATFORM`)
- [ ] 9.10 T-101 Close GATE-0 through GATE-8 with the waiver register and execute go-live (`RELMGR`/`SPONSOR`)
