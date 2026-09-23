# cll-pmo-platform-openspec

Georgia Tech College of Lifetime Learning **Strategy 2035 PMO Platform** OpenSpec
implementation repository.

This repository is spec-driven: the specification is the source of truth, and
implementation work is traced back to approved requirements, acceptance criteria,
tests, evidence and release gates.

## Layout

```
openspec/
  config.yaml                         # OpenSpec project configuration
  specs/                              # Main specs (populated at sync time)
    executive-dashboard/
    project-registry/
    kpi-governance/
    governance-workflow/
    integrations/
    security/
    data-quality/
    board-reporting/
    nonfunctional/
    verification/
    release-governance/
  changes/
    implement-cll-pmo-platform-v1/    # Baseline change (v1)
      proposal.md
      design.md
      phase-crosswalk.md
      manifest.json
      decisions/
      contracts/
      registries/
      specs/                          # Delta specs for this change
      tasks/                          # 9 phase files, 101 tasks
```

## Baseline at a glance

| Metric | Count |
|---|---|
| Approved requirements | 72 |
| Acceptance criteria | 223 |
| Implementation tasks | 101 |
| Phase task files | 9 |
| Capabilities (domain specs) | 11 |
| Release gates | 9 |

## Requirement identifier ranges

| Prefix | Capability | Range | Count |
|---|---|---|---|
| INT | Integrations | INT-001 – INT-011 | 11 |
| SEC | Security | SEC-001 – SEC-007 | 7 |
| EXD | Executive Dashboard | EXD-001 – EXD-008 | 8 |
| PRJ | Project Registry | PRJ-001 – PRJ-008 | 8 |
| KPI | KPI Governance | KPI-001 – KPI-007 | 7 |
| GOV | Governance Workflow | GOV-001 – GOV-006 | 6 |
| DQA | Data Quality | DQA-001 – DQA-006 | 6 |
| BRD | Board Reporting | BRD-001 – BRD-007 | 7 |
| NFR | Nonfunctional | NFR-001 – NFR-007 | 7 |
| VER | Verification | VER-001 – VER-003 | 3 |
| REL | Release Governance | REL-001 – REL-002 | 2 |

## Working the change

```bash
openspec list
openspec show implement-cll-pmo-platform-v1
openspec validate implement-cll-pmo-platform-v1 --strict
```

Workflow: explore -> propose -> apply -> verify -> sync -> archive. Changes are
developed on `openspec/<change-name>` branches and merged to `main` via pull
request.
