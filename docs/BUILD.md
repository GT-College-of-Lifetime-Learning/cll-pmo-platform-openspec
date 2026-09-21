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

## Demo (local, no M365 dependency)

`demo/` is a complete local implementation of the specced behavior — the flow
engine (F1/F2/F4/F7, gates, call-up), the Strategy 2035 landing page, and the
trust features — used for demos and as the reference for the M365 build.

```
python demo\build_db.py        # rebuild the deterministic demo DB
uvicorn demo.app:app --reload  # http://127.0.0.1:8000/?as=executive
```

Pages: Strategy 2035 (landing) · Dean Overview · Governance · Readiness ·
Intake · Unit · Item detail · Priority detail. Roles via `?as=executive` or
`?as=unit:<UNITID>` (rolebar switches).

Trust features (`add-trust-and-readiness-features`):

| Demo module | Ports to M365 as |
|---|---|
| `demo/readiness.py` (computed gates) | Readiness flow / Power BI measures at refresh |
| `demo/findings.py` (Findings table, 2/3/4 ladder) | SharePoint Findings list written by F7 |
| `demo/export_feed.py` (feed + manifest) | The SharePoint lists are the feed; manifest = freshness stamps |
| Provenance sub-labels on cards | Power BI tooltips on the same columns |

Feed: `python demo\export_feed.py` writes `demo/output/feed/` (8 files +
manifest); `/api/feed` serves it. Files are written even when empty (explicit
no-data states) and CSVs are injection-guarded.

Data sourcing (`add-data-source-reconciliation`): the P2/P3 instrument —
`/coverage` page + `coverage.json` feed; `docs/data-source-matrix.md` is
GENERATED from the `DataNeeds` catalog (`python demo\generate_matrix.py`;
hand edits are rejected). Steward declarations land via
`sharepoint/seed/source-declarations.csv` + `demo\load_declarations.py`
(unmatched elements go to a review queue, never silently creating rows).
Per-source integration increments are per-source loaders — first increment:
confirmed Institute holidays (`sharepoint/seed/gt-holidays.csv` +
`demo\load_holidays.py`). Real imported data is origin-tagged; fabricated
data is labeled as such on provenance lines.

Test battery: `demo\tests\` — routes (12), flows (18), visuals (12), timeline
hand-check, planted-defect suite (30). Run after any change; planted defects
must stay at 100% caught / 0 false alarms.

## Conventions

- Every buildable artifact is source-controlled (PnP/CLI provisioning, Power Platform
  solution unpacked with `pac solution unpack`, Power BI PBIP/TMDL).
- Flows never run under a personal account — service account + two co-owners (design D9).
- Priorities and KPIs are seed data (`sharepoint/seed/`), never hard-coded.
- No student-level records anywhere (FERPA). Dashboards meet WCAG 2.1 AA.
- All flows, forms, and connection references are prefixed `CLL-SPM` (design D12).