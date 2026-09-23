# Approval Sequences

Ordered approval chains for every decision type in the platform and in this
change. Enforced by GOV-002 (platform decisions) and REL-001 (release gates).
No approver may approve their own submission, including through delegation.

## Stage-gate approvals (GOV-001)

| Gate | Purpose | Sequence | Quorum | Service level |
|---|---|---|---|---|
| G0 Concept | Idea accepted into the pipeline | Project Sponsor → PMO Director | Both | 5 business days |
| G1 Charter | Charter and funding source confirmed | Project Manager → Pillar Owner → PMO Director | All three | 10 business days |
| G2 Plan | Baseline schedule and budget approved | Project Manager → PMO Portfolio Manager → PMO Director | All three | 10 business days |
| G3 Build Readiness | Ready to execute; risks accepted | Project Manager → Pillar Owner → Security Architect (if data in scope) → PMO Director | All applicable | 10 business days |
| G4 Launch | Ready to go live | Project Manager → Pillar Owner → PMO Director → Executive Steering Committee | All four | 15 business days |
| G5 Benefits Realisation | Benefits measured and accepted | KPI Steward → Pillar Owner → PMO Director | All three | 20 business days |

## Change request approvals (GOV-003)

| Materiality | Trigger | Sequence | Service level |
|---|---|---|---|
| Minor | ≤ 5% budget and ≤ 10 days schedule | PMO Portfolio Manager | 3 business days |
| Moderate | ≤ 10% budget and ≤ 30 days schedule | PMO Portfolio Manager → PMO Director | 5 business days |
| Material | > 10% budget, or > 30 days schedule, or any benefit reduction | PMO Director → Executive Steering Committee | 15 business days |
| Scope removal affecting a Strategy 2035 objective | Any | PMO Director → Strategy Office → Executive Steering Committee | 20 business days |

## KPI governance approvals (KPI-001, KPI-003, KPI-006)

| Decision | Sequence | Service level |
|---|---|---|
| New KPI definition | KPI Steward → Data Governance Lead → Strategy Office | 10 business days |
| Target or threshold change | KPI Steward → Pillar Owner → PMO Director | 10 business days |
| Definition version change with no published impact | KPI Steward → Data Governance Lead | 5 business days |
| Restatement of a published period | KPI Steward → Data Governance Lead → PMO Director → Executive Steering Committee | 10 business days |

## Board reporting approvals (BRD-002, BRD-005)

| Decision | Sequence | Service level |
|---|---|---|
| Snapshot certification | Data Steward → Data Governance Lead | 2 business days |
| Section narrative | Section author → PMO Director | 3 business days |
| KPI exception narrative | KPI Steward → Data Governance Lead → PMO Director | 3 business days |
| Package publication | PMO Director → CLL Executive Office | 2 business days |
| Distribution list change | PMO Portfolio Manager → CLL Executive Office | 5 business days |

## Security approvals (DR-SEC-001)

| Decision | Sequence | Service level |
|---|---|---|
| New role or permission change | Security Architect → Data Governance Lead → CLL CIO delegate | 10 business days |
| Scoping rule exception | Security Architect → CLL CIO delegate | 5 business days |
| Quarterly recertification | Role accountable owner → Security Architect | Certification window |
| Emergency access grant | Security Architect → CLL CIO delegate (retrospective within 1 business day) | Immediate |

## Release gate approvals (REL-001)

| Gate | Sequence | Quorum |
|---|---|---|
| GATE-0 | `PLATFORM` → `SECARCH` → `SPONSOR` | All three |
| GATE-1 | `DATAENG` → `DATAGOV` → `SPONSOR` | All three |
| GATE-2 | `APPENG` → `PORTFOLIO` → `SPONSOR` | All three |
| GATE-3 | `SECARCH` → `DATAGOV` → `SPONSOR` | All three |
| GATE-4 | `BILEAD` → `A11Y` → `SPONSOR` | All three |
| GATE-5 | `APPENG` → `PORTFOLIO` → `SPONSOR` | All three |
| GATE-6 | `DATAENG` → `SECARCH` → `SPONSOR` | All three |
| GATE-7 | `BILEAD` → `PORTFOLIO` → `SPONSOR` | All three |
| GATE-8 | `QALEAD` → `RELMGR` → `SPONSOR` | All three |

## Delegation rules

- Delegation is explicit, named and time-bounded, and is recorded on the
  decision (AC-GOV-002-2).
- A delegation chain that resolves back to the submitter is rejected as
  self-approval (AC-GOV-002-3).
- Sponsor approval may not be delegated for GATE-8 or for package publication.
- Emergency access approval may be retrospective by at most one business day.
