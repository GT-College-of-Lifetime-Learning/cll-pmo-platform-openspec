# CLL Strategic Portfolio Management (SPM) — OpenSpec

The "project to manage all projects": a college-wide registry, intake process, status rhythm,
and executive dashboards for the Georgia Tech College of Lifetime Learning, built on Microsoft 365.

## What's here

```
openspec/
├── config.yaml                                   # Project context + per-artifact rules
├── specs/                                        # Source of truth (empty until Phase 1 is archived)
└── changes/
    ├── add-portfolio-registry-and-exec-dashboards/   # PHASE 1 — full change
    │   ├── proposal.md     # Why, what, success criteria, open questions
    │   ├── design.md       # Architecture, decisions, data model, flows, risks, rollout
    │   ├── tasks.md        # Build checklist
    │   └── specs/          # Delta specs (6 new capabilities)
    └── add-execution-and-resource-management/        # PHASE 2 — proposal stub only
        └── proposal.md
sharepoint/seed/                                  # Provisional Strategy 2035 goals, objectives, KPIs, units, backfill template
```

## Using it with an OpenSpec-compatible coding agent

```bash
npm install -g @fission-ai/openspec@latest   # if not installed
openspec validate add-portfolio-registry-and-exec-dashboards --strict
```

Then use your agent's OpenSpec workflow to work the change: `/opsx:apply` to work the Phase 1
tasks, `/opsx:archive` when done (command names vary by tool — this repo ships opencode
commands in `.opencode/commands/`). For Phase 2, open the stub and run your agent's
continue/expand workflow to generate specs, design, and tasks.

## Read first

1. `changes/add-portfolio-registry-and-exec-dashboards/proposal.md` — the case and the blocking questions for the sponsor
2. `design.md` in the same folder — especially the revised tool map and decisions D1–D4
