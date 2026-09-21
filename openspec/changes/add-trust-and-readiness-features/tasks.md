# Tasks — Trust and Readiness Features

Legend: (code) source-controlled · (test) adversarial/planted-defect verification · (calib) Strategic Operations calibration

## 1. Finding tracker (finding-tracker spec)
- [ ] 1.1 (code) `Findings` table in demo DB schema: FindingId, Type, AffectedUnitId, AffectedItemId, Severity, FirstSeenOn, LastSeenOn, Occurrences, Status, ResolvedBy, ResolvedOn; append-only discipline (no edit/delete routes)
- [ ] 1.2 (code) Hygiene-writer in the F7 run: record/increment findings by (type, affected item) for stale-update, red-without-resolution, unaligned-item, triage-overdue, decision-overdue
- [ ] 1.3 (code) Resolution path: submitting the missing update (or fixing the cause) appends a resolution record and resets the counter on recurrence
- [ ] 1.4 (code) Recurring marker (2+ occurrences) on items in the unit view
- [ ] 1.5 (code) Governance view: needs-attention list of findings at 3+ occurrences with occurrence history
- [ ] 1.6 (code) Stage-gate extension: block move to Closed while any Open finding with 4+ occurrences exists on the item (reuses the existing stage gate)
- [ ] 1.7 (code) Findings respect D13 masking for Confidential affected items
- [ ] 1.8 (test) Planted defects: stale item across 3 simulated cycles increments occurrences; 4-occurrence finding blocks closeout; resolution resets; confidential finding masked for other-unit viewer

## 2. Cycle readiness (cycle-readiness spec)
- [ ] 2.1 (code) `demo/readiness.py`: gate registry (name, value fn, thresholds) per design D1 defaults; each gate returns value + state OK/WARN/BLOCKING
- [ ] 2.2 (code) `/readiness` page: gates sorted blockers-first with name, value, threshold, state in text; renders when failing (not an error state)
- [ ] 2.3 (code) Trust banner component on every dashboard page: OK silent, WARN subtle, BLOCKING degraded banner linking to /readiness
- [ ] 2.4 (code) Gates wired: status currency %, stale active count, expired call-up windows, decisions past SLA, core-route reachability
- [ ] 2.5 (test) Planted defects: stale items flip currency gate to BLOCKING with correct value; all-green build shows all-OK page; failing build renders blockers as content

## 3. Data feed (data-feed spec)
- [ ] 3.1 (code) `demo/export_feed.py`: kpis.csv, rag-counts.csv, currency.csv, intake-aging.csv, readiness.json + manifest.json (FEED_VERSION, generated-at, source build, per-file row counts)
- [ ] 3.2 (code) Empty-state discipline: every file written on every export, headers only when empty
- [ ] 3.3 (code) CSV-injection guard (prefix `'` on string cells starting with `=`, `+`, `-`, `@`; numerics untouched)
- [ ] 3.4 (code) `/api/feed` endpoint serving the exported files, role-filtered for item-level rows; college-level files by construction
- [ ] 3.5 (test) Planted defects: empty DB export produces all files with 0 rows + manifest records 0; `=SUM(A1)` title exports inert; feed values match dashboard values

## 4. Provenance display (strategy-kpi-data MODIFIED spec)
- [ ] 4.1 (code) Thread source, as-of date, submitter/method into Strategy 2035 card detail (sub-label) and KPI tables
- [ ] 4.2 (code) Pending-source states show the owner's name with the pending label; no fabricated source
- [ ] 4.3 (test) Planted defects: a value rendered without provenance fails the check; a pending KPI shows owner not a number

## 5. Integration and verification
- [ ] 5.1 (code) Wire readiness summary + findings into the feed export (readiness.json; findings counts)
- [ ] 5.2 (test) Full regression: routes (12), flows (18), visuals (12), timeline hand-check, plus all new planted-defect suites
- [ ] 5.3 (code) README/docs: demo page inventory updated (readiness, feed) with the production port map
- [ ] 5.4 (calib) Strategic Ops reviews gate thresholds and escalation ladder against seeded data; adjust D1 defaults
- [ ] 5.5 `openspec validate add-trust-and-readiness-features --strict`