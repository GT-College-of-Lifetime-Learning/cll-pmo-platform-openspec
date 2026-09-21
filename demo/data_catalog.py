# CLL-SPM data-needs catalog seed — the backwards map as data.
# One row per external data element the dashboards consume.
# Source states are honest starting states; steward declarations upgrade them.

# (NeedId, Element, ConsumerView, RequiredFields, Cadence, DefinitionState,
#  SourceState, SourceSystem, SourceFormat, SourceRefresh, Steward, Notes)
CATALOG = [
    # ---- Strategy 2035 headline KPIs ----
    ("DN-001", "Learning-systems graduates (KPI-001)", "Strategy 2035 / Goal 1",
     "count by period, credential type", "Annual", "UNDEFINED-Q2", "MISSING",
     None, None, None, None, "Q2: graduates (degrees only) vs credentialed+graduated"),
    ("DN-002", "Fortune 500 leaders credentialed (KPI-003)", "Strategy 2035 / Goal 1",
     "count, cumulative", "Annual", "defined", "MISSING", None, None, None, None, None),
    ("DN-003", "Connected learning hubs (KPI-004)", "Strategy 2035 / Goal 2",
     "hub count, cumulative", "Annual", "defined", "MISSING", None, None, None, None, None),
    ("DN-004", "Hub locations (lat/long per hub)", "Strategy 2035 / Goal 2 map",
     "hub name, city, lat, long", "On change", "defined", "MISSING", None, None, None, None,
     "map visual needs stored coordinates; no geocoding (design D8)"),
    ("DN-005", "Start-ups with market adoption (KPI-005)", "Strategy 2035 / Goal 2",
     "count, cumulative", "Annual", "defined", "MISSING", None, None, None, None, None),
    ("DN-006", "Learner touchpoints (KPI-006)", "Strategy 2035 / Goal 3",
     "count, cumulative, deduplicated", "Quarterly", "UNDEFINED-Q6", "MISSING",
     None, None, None, None, "Q6: what counts as a touchpoint - routed to sponsor first"),
    ("DN-007", "Unique learners credentialed (KPI-007)", "Strategy 2035 / Goal 3",
     "count, cumulative, unique", "Quarterly", "defined", "MISSING", None, None, None, None, None),
    ("DN-008", "3-year graduation rate (KPI-008)", "Priority detail / Goal 3",
     "rate percent, cohort", "Annual", "defined-partial", "MISSING", None, None, None, None,
     "baseline from Institutional Research; target = 2x baseline"),
    ("DN-009", "Annual content renewal rate (KPI-009)", "Priority detail / Goal 3",
     "rate percent", "Annual", "defined", "MISSING", None, None, None, None, None),
    ("DN-010", "Annual external research expenditures (KPI-010)", "Strategy 2035 / Goal 4",
     "USD by fiscal year, CLL-attributed", "Annual", "UNDEFINED-Q7", "MISSING",
     None, None, None, None, "Q7: fiscal-year basis + sponsored-research attribution rules"),
    ("DN-011", "Digital Transformation Maturity Index (KPI-012)", "Strategy 2035 / Goal 5",
     "capability ratings 1-5 with evidence", "Semiannual", "UNDEFINED-Q5", "MISSING",
     None, None, None, None, "Q5: target level + rubric sign-off + assessor"),
    ("DN-012", "Dashboard KPI coverage (KPI-011)", "Priority detail / Goal 5",
     "objectives with live KPI", "Quarterly", "defined", "HAVE",
     "this system", "computed", "per refresh", "Strategic Operations", "measured by the system itself"),
    # ---- Recent-activity entries ----
    ("DN-013", "Term graduates by term", "Strategy 2035 / Goal 1 recent",
     "term, count, program", "Per term", "UNDEFINED-Q2", "MISSING", None, None, None, None, None),
    ("DN-014", "Hub openings", "Strategy 2035 / Goal 2 recent",
     "hub name, city, date", "On change", "defined", "MISSING", None, None, None, None, None),
    ("DN-015", "Credentials issued", "Strategy 2035 / Goal 3 recent",
     "program, date, count", "Quarterly", "defined", "MISSING", None, None, None, None,
     "counts only; never learner identities"),
    ("DN-016", "Grants awarded", "Strategy 2035 / Goal 4 recent",
     "grant name, date, amount, sponsor type", "On award", "defined", "MISSING", None, None, None, None, None),
    ("DN-017", "Capabilities delivered", "Strategy 2035 / Goal 5 recent",
     "capability, date", "On closeout", "defined", "HAVE",
     "this system", "computed from closeouts", "per closeout", "Strategic Operations", None),
    # ---- Capability inventory (Goal 5) ----
    ("DN-018", "Capability inventory with maturity ratings", "Strategy 2035 / Goal 5",
     "capability, area, level, evidence", "Semiannual", "UNDEFINED-Q5", "MISSING",
     None, None, None, None, "two-person assessment per rubric; evidence required"),
    # ---- Calendar ----
    ("DN-019", "Institute holiday calendar", "Readiness / business-day math (all views)",
     "holiday dates", "Annual", "defined", "PARTIAL",
     "gen_business_days.py placeholder", "python set", "annual review", "Strategic Operations",
     "REVIEW-flagged placeholders; confirmed calendar is the first P3 integration increment"),
    # ---- Dean Overview facts ----
    ("DN-020", "Executive milestones (forecast dates)", "Dean Overview",
     "milestone, forecast date, item", "Monthly", "defined", "HAVE",
     "this system", "lead entry via F4/milestones", "per cycle", "Project leads", None),
    ("DN-021", "Status updates (RAG, currency)", "Dean Overview / Unit",
     "RAG set, summary, decision ask", "Monthly", "defined", "HAVE",
     "this system", "F4 status form", "per cycle", "Project leads", None),
    ("DN-022", "In-flight work backfill (pilot units)", "Dean Overview / Governance",
     "item registry rows", "Once + on intake", "defined", "MISSING",
     None, None, None, "Unit heads + Strategic Ops",
     "pilot backfill is Phase 1 task 7.1 - the data exists in unit records, not a system"),
    # ---- Governance facts ----
    ("DN-023", "Intake requests + decisions", "Governance",
     "request + decision rows", "Continuous", "defined", "HAVE",
     "this system", "F1/F2 forms", "continuous", "CLL staff / TCC", None),
    ("DN-024", "Scoring rubric calibration (weights)", "Governance",
     "component weights", "Per TCC batch", "defined", "MISSING",
     None, None, None, "TCC", "docs/tiers-and-scoring.md; TCC calibrates on first batch"),
    ("DN-025", "Unit registry (units, heads, access)", "All views (RLS, unit pages)",
     "unit rows, UPN access", "On change", "defined", "PARTIAL",
     "org chart (units.csv seed)", "csv", "on org change", "Strategic Operations",
     "units seeded; heads + full org chart pending Dean's office confirmation"),
]

def seed_catalog(con):
    con.executemany(
        "INSERT OR REPLACE INTO DataNeeds VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", CATALOG)