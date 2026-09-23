# Source Catalog

The eleven sources the platform is permitted to consume or publish to. A source
with no entry here may not be integrated (INT-011). Full field-level terms are
in `contracts/integration-data-contracts.md`.

| ID | Source | Contract | Requirement | Owner (institutional) | Direction | Cadence | Classification | Ingestion order |
|---|---|---|---|---|---|---|---|---|
| SRC-01 | Workday Financials | C-INT-001 | INT-001 | Controller's Office | In | Nightly 02:00 ET + 90-day trailing | Internal / financial | 3 |
| SRC-02 | Workday HCM | C-INT-002 | INT-002 | GT Human Resources | In | Weekly Mon 03:00 ET | **Restricted** | 2 |
| SRC-03 | Banner (via IR warehouse) | C-INT-003 | INT-003 | Registrar / Institutional Research | In | Nightly 04:00 ET; full reload at census | Internal / aggregate only | 5 |
| SRC-04 | Salesforce CRM | C-INT-004 | INT-004 | CLL Partnerships / Advancement IT | In | 06:00 and 18:00 ET | Internal | 7 |
| SRC-05 | Smartsheet PPM | C-INT-005 | INT-005 | CLL PMO | In + limited out | 4x daily + webhooks | Internal | 6 |
| SRC-06 | ServiceNow | C-INT-006 | INT-006 | OIT Service Management | In | Hourly | Internal | 8 |
| SRC-07 | Canvas LMS | C-INT-007 | INT-007 | CLL Learning Technology | In | Weekly Sun 01:00 ET | Internal / aggregate only | 9 |
| SRC-08 | IR warehouse (conformed dimensions) | C-INT-008 | INT-008 | Institutional Research | In | Nightly 03:30 ET | Internal | 4 |
| SRC-09 | Entra ID | C-INT-009 | INT-009 | OIT Identity Services | In | Every 60 minutes + at login | Identity | 1 |
| SRC-10 | Board SharePoint library | C-INT-010 | BRD-005 | CLL Executive Office | Out | Per reporting cycle on approval | Confidential | n/a |
| SRC-11 | Contract register (meta) | C-INT-011 | INT-011 | Data Engineering Lead | n/a | On change | Internal | n/a |

## Ingestion dependency order (DR-SYNC-001.6)

```
1 Entra ID → 2 Workday HCM → 3 Workday Financials → 4 IR dimensions
  → 5 Banner-derived → 6 Smartsheet → 7 Salesforce → 8 ServiceNow → 9 Canvas
```

A failed upstream source holds its downstream runs rather than executing them
against stale dimensions (AC-INT-010-1).

## Entity coverage by source

| Entity | Source of record | Consumed from |
|---|---|---|
| `financial_actual`, `project.budget_amount` | SRC-01 | SRC-01 |
| `effort_allocation`, `person` (employment) | SRC-02 | SRC-02 |
| `enrollment_metric` | SRC-03 | SRC-03 |
| `partner_opportunity` | SRC-04 | SRC-04 |
| `milestone` | SRC-05 | SRC-05 |
| `demand_request`, `incident` | SRC-06 | SRC-06 |
| `course_engagement` | SRC-07 | SRC-07 |
| `unit`, `program`, `term`, `funding_source` | SRC-08 | SRC-08 |
| `person` (identity), role group membership | SRC-09 | SRC-09 |
| Published package artifacts | Platform | → SRC-10 |

## Escalation contacts by source

| Source | Platform first responder | Institutional contact path |
|---|---|---|
| SRC-01, SRC-02 | `INTENG` | Workday support queue → Controller's Office / HR |
| SRC-03, SRC-08 | `DATAENG` | Institutional Research data services |
| SRC-04 | `INTENG` | Advancement IT |
| SRC-05 | `PORTFOLIO` | CLL PMO Smartsheet administrator |
| SRC-06 | `INTENG` | OIT Service Management |
| SRC-07 | `DATAENG` | CLL Learning Technology |
| SRC-09 | `SECARCH` | OIT Identity Services |
| SRC-10 | `BILEAD` | CLL Executive Office |
