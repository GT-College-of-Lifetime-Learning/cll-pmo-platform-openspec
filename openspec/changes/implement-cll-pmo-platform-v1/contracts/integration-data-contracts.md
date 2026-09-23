# Integration Data Contracts

One contract per source. A contract is binding: ingestion validates payloads
against it and **fails closed** on breach (design decision D5). Contract changes
follow INT-011 — semantic version, 30-day deprecation notice, dual-run of the
old and new version during the notice window.

**Shared conventions for all contracts**

- Transport is authenticated with a workload identity; no shared user accounts.
- All timestamps are delivered or converted to UTC; all dates are ISO-8601.
- Every run records: `run_id`, `contract_version`, `source_system`,
  `window_start`, `window_end`, `record_count`, `reject_count`, `status`.
- Every record carries `source_system`, `source_record_id`, `extracted_at` and
  `run_id` into the landing zone.
- Absent records are marked inactive, never deleted (DR-SYNC-001.4).
- Breach handling: schema breach fails the run; row-level breach quarantines the
  row (DQA-006).

---

## C-INT-001 — Workday Financials (budget and actuals)

| Attribute | Value |
|---|---|
| Requirement | INT-001 |
| Contract version | 1.0.0 |
| Source owner | Controller's Office, Georgia Tech Finance |
| Direction | Workday → Platform (read-only) |
| Method | Scheduled RaaS report extract over SFTP, CSV |
| Cadence | Nightly 02:00 ET, plus trailing 90-day re-read (DR-SYNC-001.3) |
| Volume | ~45,000 rows/night, ~12 MB |
| SLA | Available by 03:30 ET; 99% of business days |
| Grain | account x cost center x project x period |

**Fields**

| Field | Type | Required | Notes |
|---|---|---|---|
| `ledger_account` | string(10) | yes | Natural account code |
| `cost_center` | string(12) | yes | Maps to `unit` dimension |
| `worktag_project` | string(20) | no | Maps to `project.finance_worktag`; null = unallocated |
| `fiscal_year` | int | yes | GT fiscal year |
| `fiscal_period` | int(1-12) | yes | 1 = July |
| `budget_amount` | decimal(18,2) | yes | Signed |
| `actual_amount` | decimal(18,2) | yes | Signed |
| `encumbrance_amount` | decimal(18,2) | yes | Signed |
| `currency` | string(3) | yes | Always `USD` in v1 |
| `posted_at` | timestamp | yes | UTC |

**Keys:** (`ledger_account`, `cost_center`, `worktag_project`, `fiscal_year`, `fiscal_period`)
**Quality gates:** sum(actual) reconciles to ledger total at $0 variance monthly (DQA-003).

---

## C-INT-002 — Workday HCM (position and effort)

| Attribute | Value |
|---|---|
| Requirement | INT-002 |
| Contract version | 1.0.0 |
| Source owner | GT Human Resources |
| Direction | Workday → Platform (read-only) |
| Method | RaaS extract over SFTP, CSV |
| Cadence | Weekly, Monday 03:00 ET |
| Volume | ~3,500 rows/week |
| SLA | Available by 05:00 ET Monday |
| Grain | position x period x project allocation |
| Sensitivity | **Restricted** — position-level rows visible only to `portfolio-admin` and `data-steward` (DR-SEC-001.3) |

**Fields:** `position_id` string(12) yes; `worker_id` string(12) yes;
`worker_email` string(254) yes (join key to Entra ID); `job_profile` string(60)
yes; `cost_center` string(12) yes; `fte` decimal(4,3) yes; `allocation_worktag`
string(20) no; `effective_from` date yes; `effective_to` date no;
`employment_status` enum(`active`,`leave`,`terminated`) yes.

**Keys:** (`position_id`, `effective_from`)
**Quality gates:** `fte` between 0.000 and 1.000; sum of allocations per position per period ≤ 1.000.

---

## C-INT-003 — Banner student enrollment (via IR warehouse)

| Attribute | Value |
|---|---|
| Requirement | INT-003 (path per INT-008) |
| Contract version | 1.0.0 |
| Source owner | Office of the Registrar / Institutional Research |
| Direction | Warehouse → Platform (read-only) |
| Method | Warehouse view, JDBC pull |
| Cadence | Nightly 04:00 ET; full reload at term census |
| Volume | ~20,000 aggregate rows/night |
| SLA | Available by 05:00 ET |
| Grain | program x term x student level (aggregate only) |

**Fields:** `term_code` string(6) yes; `program_code` string(12) yes;
`program_name` string(120) yes; `student_level` enum(`UG`,`GR`,`NC`) yes;
`headcount` int yes; `credit_hours` decimal(10,2) yes; `new_starts` int yes;
`completions` int yes; `census_flag` boolean yes; `as_of_date` date yes.

**Keys:** (`term_code`, `program_code`, `student_level`, `as_of_date`)
**Quality gates:** no row with `headcount` < 5 is delivered (suppression at
source); headcount reconciles to IR published census within 0.5%.
**Privacy:** no student-identifiable data crosses this boundary. Ever.

---

## C-INT-004 — Salesforce CRM (partner pipeline)

| Attribute | Value |
|---|---|
| Requirement | INT-004 |
| Contract version | 1.0.0 |
| Source owner | CLL Partnerships / Advancement IT |
| Direction | Salesforce → Platform (read-only) |
| Method | Bulk API 2.0 query, incremental on `SystemModstamp` |
| Cadence | 06:00 and 18:00 ET |
| Volume | ~2,000 opportunities, ~500 changed per run |
| SLA | 30-minute completion window |
| Grain | opportunity |

**Fields:** `opportunity_id` string(18) yes; `account_name` string(255) yes;
`opportunity_name` string(255) yes; `stage` string(40) yes; `amount`
decimal(18,2) no; `probability` int(0-100) no; `close_date` date no;
`strategic_pillar__c` string(40) no; `linked_project_code__c` string(20) no;
`owner_email` string(254) yes; `system_modstamp` timestamp yes.

**Keys:** `opportunity_id`
**Quality gates:** `stage` must be in the agreed stage set; unknown stages quarantine the row.

---

## C-INT-005 — Smartsheet PPM (project plans, bi-directional subset)

| Attribute | Value |
|---|---|
| Requirement | INT-005 |
| Contract version | 1.0.0 |
| Source owner | CLL PMO |
| Direction | Smartsheet → Platform (plans); Platform → Smartsheet (4 fields, DR-SYNC-001.2) |
| Method | Smartsheet REST API v2 + webhook on change |
| Cadence | 4x daily (06:00, 10:00, 14:00, 18:00 ET); webhooks near-real-time |
| Volume | ~500 sheets, ~25,000 rows |
| SLA | 15-minute propagation for webhook events |
| Grain | sheet row (milestone/task) |

**Inbound fields:** `sheet_id` string yes; `row_id` string yes; `project_code`
string(20) yes; `milestone_name` string(255) yes; `start_date` date no;
`end_date` date no; `percent_complete` decimal(5,2) no; `assigned_to_email`
string(254) no; `status` string(40) no; `modified_at` timestamp yes.

**Outbound fields (platform-owned):** `project_name`, `lifecycle_state`,
`gate_flag`, `platform_status_summary`.

**Keys:** (`sheet_id`, `row_id`)
**Quality gates:** `end_date` ≥ `start_date`; `project_code` must resolve to a
registry project or the row quarantines.

---

## C-INT-006 — ServiceNow (demand and incidents)

| Attribute | Value |
|---|---|
| Requirement | INT-006 |
| Contract version | 1.0.0 |
| Source owner | OIT Service Management |
| Direction | ServiceNow → Platform (read-only) |
| Method | Table API, incremental on `sys_updated_on` |
| Cadence | Hourly |
| Volume | ~300 records/hour peak |
| SLA | 99% of hourly runs complete within 10 minutes |
| Grain | demand request / incident |

**Fields:** `sys_id` string(32) yes; `number` string(20) yes; `record_type`
enum(`demand`,`incident`) yes; `short_description` string(255) yes; `state`
string(40) yes; `priority` int(1-5) yes; `assignment_group` string(80) yes;
`linked_project_code` string(20) no; `opened_at` timestamp yes;
`resolved_at` timestamp no; `sys_updated_on` timestamp yes.

**Keys:** `sys_id`
**Quality gates:** `resolved_at` ≥ `opened_at` when present.

---

## C-INT-007 — Canvas LMS (course engagement)

| Attribute | Value |
|---|---|
| Requirement | INT-007 |
| Contract version | 1.0.0 |
| Source owner | CLL Learning Technology |
| Direction | Canvas → Platform (read-only) |
| Method | Canvas Data 2 file export |
| Cadence | Weekly, Sunday 01:00 ET |
| Volume | ~50,000 aggregate rows |
| SLA | Available by 06:00 ET Sunday |
| Grain | course x week (aggregate only) |

**Fields:** `course_code` string(40) yes; `course_name` string(200) yes;
`term_code` string(6) yes; `week_start` date yes; `active_learners` int yes;
`completion_rate` decimal(5,2) no; `avg_time_on_task_minutes` decimal(10,2) no;
`program_code` string(12) no.

**Keys:** (`course_code`, `week_start`)
**Quality gates:** `completion_rate` between 0 and 100; cells with
`active_learners` < 5 are suppressed.
**Privacy:** aggregate only; no learner-level records.

---

## C-INT-008 — Institutional Research warehouse (conformance)

| Attribute | Value |
|---|---|
| Requirement | INT-008 |
| Contract version | 1.0.0 |
| Source owner | Institutional Research |
| Direction | Warehouse → Platform (read-only) |
| Method | JDBC pull of conformed dimension views |
| Cadence | Nightly 03:30 ET |
| Volume | ~15,000 dimension rows |
| SLA | Available by 04:30 ET |
| Grain | dimension member |

**Fields:** `dimension_name` enum(`unit`,`program`,`term`,`funding_source`) yes;
`member_code` string(20) yes; `member_name` string(200) yes; `parent_code`
string(20) no; `effective_from` date yes; `effective_to` date no;
`is_current` boolean yes.

**Keys:** (`dimension_name`, `member_code`, `effective_from`)
**Quality gates:** every code referenced by any other feed must exist here, or
the referencing row quarantines as a referential-integrity failure.

---

## C-INT-009 — Entra ID (identity and groups)

| Attribute | Value |
|---|---|
| Requirement | INT-009, SEC-002 |
| Contract version | 1.0.0 |
| Source owner | OIT Identity Services |
| Direction | Entra ID → Platform (read-only) |
| Method | Microsoft Graph, delta query |
| Cadence | Every 60 minutes; on-demand at login |
| Volume | ~1,200 users, 6 groups |
| SLA | Group change reflected within 60 minutes (DR-SEC-001.7) |
| Grain | user; group membership |

**Fields:** `object_id` guid yes; `user_principal_name` string(254) yes; `mail`
string(254) yes; `display_name` string(200) yes; `account_enabled` boolean yes;
`group_object_id` guid yes; `group_display_name` string(200) yes;
`membership_changed_at` timestamp yes.

**Keys:** (`object_id`, `group_object_id`)
**Quality gates:** a platform role assignment with no matching current group
membership is an orphan and is revoked at next sync (DQA-003 daily
reconciliation).

---

## C-INT-010 — Board reporting SharePoint (package distribution)

| Attribute | Value |
|---|---|
| Requirement | INT-010 scheduling applies; BRD-005 distribution |
| Contract version | 1.0.0 |
| Source owner | CLL Executive Office |
| Direction | Platform → SharePoint (write, package artifacts only) |
| Method | Microsoft Graph drive upload to a permissioned library |
| Cadence | Per reporting cycle, on approval |
| Volume | ~10 artifacts/cycle, < 200 MB |
| SLA | Published within 30 minutes of approval |
| Grain | package artifact |

**Fields:** `package_id` string(20) yes; `reporting_period` string(10) yes;
`artifact_type` enum(`pdf`,`pptx`,`xlsx`,`csv`) yes; `snapshot_id` string(20)
yes; `approved_by` string(254) yes; `approved_at` timestamp yes;
`checksum_sha256` string(64) yes.

**Keys:** (`package_id`, `artifact_type`)
**Quality gates:** upload is refused unless `snapshot_id` resolves to a
certified snapshot and the approval record exists (BRD-002).

---

## C-INT-011 — Contract governance (meta-contract)

| Attribute | Value |
|---|---|
| Requirement | INT-011 |
| Contract version | 1.0.0 |
| Owner | Data Engineering Lead |

**Rules**

- Versioning is semantic: MAJOR = breaking (field removed, type narrowed, key
  changed), MINOR = additive, PATCH = documentation or tolerance change.
- A MAJOR change requires: 30 calendar days written notice to the PMO, a
  dual-run window where both versions ingest in parallel, and reconciliation
  showing equivalence before the old version is retired.
- Every ingested record is stamped with the `contract_version` that validated
  it, so any historical figure can be traced to the contract in force.
- An unannounced breaking change detected at runtime fails the run, raises a
  blocking exception (DQA-005), and freezes snapshot certification for affected
  measures until resolved.
- The contract register (this file) is the authoritative list; a source with no
  contract entry may not be ingested.
