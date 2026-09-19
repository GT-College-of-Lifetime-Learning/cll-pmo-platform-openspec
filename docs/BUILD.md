# CLL Strategic Portfolio Management (SPM) — Phase 1 build

Georgia Tech College of Lifetime Learning. Registry, intake, status rhythm, and
executive dashboards on Microsoft 365. Source of truth for requirements:
`openspec/changes/add-portfolio-registry-and-exec-dashboards/`.

## Layout

| Path | Contents |
|---|---|
| `openspec/` | Change proposals, specs, designs, tasks (OpenSpec) |
| `sharepoint/` | PnP provisioning template / list schemas / seed CSVs |
| `flows/` | Unpacked Power Platform solution (`CLL-SPM`) |
| `powerbi/` | Power BI Project (PBIP) — semantic model + report (TMDL) |
| `docs/` | RAG definitions, scoring rubric, tier criteria, lead playbook, templates |

## Conventions

- Every buildable artifact is source-controlled (PnP/CLI provisioning, Power Platform
  solution unpacked with `pac solution unpack`, Power BI PBIP/TMDL).
- Flows never run under a personal account — service account + two co-owners (design D9).
- Priorities and KPIs are seed data (`sharepoint/seed/`), never hard-coded.
- No student-level records anywhere (FERPA). Dashboards meet WCAG 2.1 AA.
- All flows, forms, and connection references are prefixed `CLL-SPM` (design D12).