# Tasks — Phase 1

Legend: [SPONSOR] needs Bill/Dean decision · [OIT] needs Georgia Tech OIT · (code) source-controlled · (config) click-ops

## 0. Decisions and access (blocking)
- [x] 0.1 [SPONSOR] Confirm TCC's role — TCC decides Tier 1 intake and portfolio-level questions
- [x] 0.2 [SPONSOR] Approve tier thresholds (design D3) — accepted as proposed
- [x] 0.3 [SPONSOR] Seed Strategy 2035 priorities as Provisional — approved; CSVs in `sharepoint/seed/`
- [x] 0.4 [SPONSOR] Pilot units — recommended: Office of the Dean (central ops), GTPE, GTLI
- [ ] 0.5 Brief the three pilot unit heads; get agreement and a named contact in each
- [x] 0.6 [OIT] Confirm Power BI licensing — all CLL staff licensed
- [ ] 0.7 [OIT] Request SharePoint site + Team "CLL-SPM", Power BI workspace, and a non-personal service account
- [x] 0.8 Power Platform environment — default environment (design D12)
- [ ] 0.9 [OIT] Confirm default-environment DLP policy keeps SharePoint, Forms, Approvals, Teams, Outlook, and Office 365 Users in one data group
- [ ] 0.10 [OIT] Confirm app registration / auth approach for provisioning scripts (PnP or CLI for Microsoft 365)
- [ ] 0.11 [SPONSOR] Name an executive owner for each Strategy 2035 goal

## 1. Repository and build pipeline
- [x] 1.1 (code) Create repo with `openspec/`, `sharepoint/`, `flows/`, `powerbi/`, `docs/`
- [x] 1.2 (code) Provisioning script skeleton that can deploy lists to a test site and to production
- [ ] 1.3 (config) Create `CLL-SPM` solution in the default environment with environment variables (site URL, list IDs) and connection references
- [x] 1.4 (code) Export/unpack routine for the solution (`pac solution export` + `unpack`) committed to `flows/`
- [x] 1.5 (code) Create PBIP project in `powerbi/` and confirm TMDL diffs cleanly in git

## 2. Registry and alignment (portfolio-registry, strategic-alignment)
- [x] 2.1 (code) Define list schemas: Units, UnitAccess, StrategicPriorities, StrategicObjectives, KPIs, KpiValues, Portfolios, WorkItems, StatusUpdates, Milestones, IntakeRequests, Decisions, Counters
- [x] 2.2 (code) Add column validation for activation-required fields and stage values
- [x] 2.3 (code) Add indexes on ItemId, PeriodEnd, LeadUnitId, Stage, Status
- [ ] 2.4 (config) ID-generation flow using Counters with trigger concurrency = 1
- [ ] 2.5 (config) Stage-change logging (date + actor) and closeout-summary check
- [x] 2.6 (code) Seed Units and UnitAccess
- [x] 2.7 (code) Load `strategic-priorities.csv` (5) and `strategic-objectives.csv` (25) as Provisional; define initial portfolios (PF-##)
- [x] 2.8 (code) Load `kpis.csv` (11); assign owners once 0.9 is done; missing baselines display "pending"
- [ ] 2.9 (config) Confidential item handling: item-level permissions set by flow; lists restricted to Strategic Operations + service account
- [x] 2.10 (code) Backfill import script from a standard spreadsheet template (marks Backfilled)
- [x] 2.11 (code) Business-day calendar table for due/stale calculations (needed by intake and status flows)

## 3. Intake and governance (intake-governance)
- [ ] 3.1 (config) Request form (Microsoft Forms, group-owned) with units-involved multi-select (design D14)
- [ ] 3.2 (config) F1: create REQ record (stamping ContributingUnitIds; multi-unit → Tier 1), notify requester + triage owner
- [x] 3.3 (code) Publish scoring rubric and tier criteria in `docs/`; TCC calibrates rubric weights on its first batch
- [ ] 3.4 (config) F2: route by tier via Approvals; write DEC record; on approval create WorkItem and link both ways; open 10-day TCC call-up window for Tier 2
- [ ] 3.4a (config) Call-up action: TCC member flags a Tier 2 approval → item blocked from Active, added to next TCC agenda
- [ ] 3.5 (config) Decisions list append-only (no edit/delete for non-admins; corrections reference original)
- [ ] 3.6 (config) Requester status view (filtered to requester)
- [ ] 3.7 (config) F7 hygiene: triage > 5 business days; unit-head decision reminder at 5 and Strategic Ops notice at 10; close expired call-up windows

## 4. Status reporting (status-reporting)
- [x] 4.1 (code) Publish RAG definitions and a one-page lead playbook in `docs/`
- [ ] 4.2 (config) Status update form with pre-filled item ID link
- [ ] 4.3 (config) F4: validate Red → path/ask required; append StatusUpdates; update milestone forecast
- [ ] 4.4 (config) F5: pre-due reminder, overdue reminder, unit-head escalation at +5 business days
- [ ] 4.5 (config) F6: manual KPI reminders and Late flag
- [x] 4.6 (code) Refresh measures using the business-day calendar (task 2.11) for due/stale calculations

## 5. Project workspaces (project-workspaces)
- [x] 5.1 (code) Charter, risk/issue log, and closeout templates in `docs/templates/`
- [ ] 5.2 (config) F3: Teams channel + library folder from template; write WorkspaceUrl back
- [ ] 5.3 (config) Block Tier 1 activation without CharterUrl
- [ ] 5.4 [OIT] Confirm retention label to apply on closeout; read-only on Closed

## 6. Semantic model and dashboards (executive-dashboards)
- [x] 6.1 (code) Star schema: facts StatusUpdates, KpiValues, Milestones; dims WorkItems, Priorities, Portfolios, Units, KPIs, Date
- [x] 6.1a (code) ConfidentialCounts snapshot (refresh-time, non-identifying; design D13) + "+N Confidential" measure folded into totals
- [x] 6.2 (code) Measures: latest RAG, status currency %, decisions needed, alignment coverage, effort split, intake aging, KPI progress
- [x] 6.3 (code) RLS roles Executive and Unit driven by UnitAccess + USERPRINCIPALNAME(); detail tables use NOT(Confidential) OR LeadUnitId = own unit (D13); test with "View as"
- [ ] 6.4 (code) Pages: Dean Overview (with phone layout), Governance, Unit, Priority detail, Item drill-through
- [ ] 6.5 (code) Freshness stamp on every page; status shown with text/shape, not color alone
- [ ] 6.6 (config) Scheduled refresh ≥ daily; failure notification to portfolio analyst
- [ ] 6.7 (config) Publish Power BI app with audiences; no Viewer access to workspace for consumers
- [ ] 6.8 (config) Accessibility check against WCAG 2.1 AA (contrast, keyboard, alt text, reading order)

## 7. Pilot
- [ ] 7.1 Backfill pilot units' in-flight work — load `CLL-26-0001` (this project) first
- [ ] 7.2 Run one full monthly cycle (reminders → updates → dashboard)
- [ ] 7.3 Dean and governance walkthrough on live data; capture changes
- [ ] 7.4 Measure update time and currency; adjust forms and thresholds

## 8. College-wide rollout
- [ ] 8.1 Registration drive for all units (backfill template + office hours)
- [ ] 8.2 30-minute training for leads; playbook link in every reminder
- [ ] 8.3 [SPONSOR] Dashboard becomes the standing status item in leadership and TCC meetings; Governance view is the TCC agenda source
- [ ] 8.4 Second cycle; report success criteria to sponsor

## 9. Verify and archive
- [ ] 9.1 Walk every spec scenario against the live system; record evidence
- [ ] 9.2 `openspec validate add-portfolio-registry-and-exec-dashboards --strict`
- [ ] 9.3 `/opsx:verify`, then `/opsx:archive`
