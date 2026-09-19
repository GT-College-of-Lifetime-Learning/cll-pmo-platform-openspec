# CLL-SPM demo database builder.
# Creates demo/cll_spm.db (SQLite) mirroring sharepoint/registry-lists.json,
# loads the real seed CSVs, then generates a realistic portfolio:
#   ~30 work items, 6 monthly status cycles, milestones, intake pipeline,
#   decisions, KPI values, 3 Confidential items (to demo D13 masking).
# Deterministic: fixed random seed, so the DB is reproducible.

import csv
import datetime as dt
import random
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "sharepoint" / "seed"
DB = Path(__file__).resolve().parent / "cll_spm.db"

TODAY = dt.date(2026, 9, 19)
random.seed(42)

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE Units (UnitId TEXT PRIMARY KEY, Name TEXT, Head TEXT, UnitActive INT, PilotWave INT, UnitNote TEXT);
CREATE TABLE UnitAccess (UserUPN TEXT, AccessUnitId TEXT, Role TEXT,
    PRIMARY KEY (UserUPN, AccessUnitId));
CREATE TABLE StrategicPriorities (PriorityId TEXT PRIMARY KEY, Title TEXT, Description TEXT,
    ExecOwner TEXT, EffectiveFrom TEXT, EffectiveTo TEXT, Provisional INT, Source TEXT);
CREATE TABLE StrategicObjectives (ObjectiveId TEXT PRIMARY KEY, ObjPriorityId TEXT,
    ObjTitle TEXT, ObjProvisional INT);
CREATE TABLE KPIs (KpiId TEXT PRIMARY KEY, KpiName TEXT, KpiDefinition TEXT, KpiPriorityId TEXT,
    KpiObjectiveId TEXT, KpiUnitId TEXT, KpiOwner TEXT, UnitOfMeasure TEXT, Direction TEXT,
    Baseline REAL, Target REAL, TargetDate TEXT, Frequency TEXT, KpiSource TEXT, Method TEXT,
    ProvisionalFlag INT, KpiNote TEXT);
CREATE TABLE KpiValues (KpiValueId TEXT, PeriodEnd TEXT, Value REAL, ValueNote TEXT, SubmittedBy TEXT);
CREATE TABLE Portfolios (PortfolioId TEXT PRIMARY KEY, PortfolioTitle TEXT, PortPriorityId TEXT, PortfolioOwner TEXT);
CREATE TABLE WorkItems (ItemId TEXT PRIMARY KEY, Level TEXT, Title TEXT, ParentId TEXT,
    WorkPortfolioId TEXT, PrimaryPriorityId TEXT, PrimaryObjectiveId TEXT,
    SecondaryPriorityIds TEXT, AlignmentCategory TEXT, AlignmentJustification TEXT,
    Tier TEXT, LeadUnitId TEXT, ContributingUnitIds TEXT, Sponsor TEXT, Lead TEXT,
    Stage TEXT, StartDate TEXT, TargetEndDate TEXT, BaselineEndDate TEXT,
    StageChangedOn TEXT, StageChangedBy TEXT, EffortEstimateHrs INT, CostEstimate INT,
    ExecutionTool TEXT, ExecutionLink TEXT, WorkspaceUrl TEXT, CharterUrl TEXT,
    KpiIds TEXT, Confidential INT, Backfilled INT, RequestId TEXT);
CREATE TABLE StatusUpdates (ItemId TEXT, PeriodEnd TEXT, OverallRAG TEXT, ScheduleRAG TEXT,
    ScopeRAG TEXT, ResourceRAG TEXT, Summary TEXT, PathToGreen TEXT, NextMilestone TEXT,
    NextMilestoneDate TEXT, PercentComplete INT, DecisionNeeded INT, DecisionAsk TEXT,
    SubmittedBy TEXT, SubmittedOn TEXT);
CREATE TABLE Milestones (ItemId TEXT, MilestoneTitle TEXT, BaselineDate TEXT,
    ForecastDate TEXT, ActualDate TEXT, IsExecutive INT);
CREATE TABLE IntakeRequests (RequestId TEXT PRIMARY KEY, Title TEXT, Requester TEXT,
    ReqUnitId TEXT, ContributingUnitIds TEXT, Problem TEXT, ProposedPriorityId TEXT,
    EffortEst INT, CostEst INT, ExternalCommitment INT, Tier TEXT,
    ScoreAlignment INT, ScoreValue INT, ScoreUrgency INT, ScoreCapacity INT,
    ScoreEffort INT, ScoreRisk INT, TriageOwner TEXT, Status TEXT, RevisitDate TEXT,
    DecisionId TEXT, LinkedItemId TEXT, SubmittedDate TEXT);
CREATE TABLE Decisions (DecisionId TEXT PRIMARY KEY, DecisionDate TEXT, Body TEXT,
    SubjectId TEXT, Decision TEXT, Rationale TEXT, Conditions TEXT,
    CorrectsDecisionId TEXT, RecordedBy TEXT);
CREATE TABLE Counters (Prefix TEXT, CounterYear INT, Next INT, PRIMARY KEY (Prefix, CounterYear));
CREATE TABLE ConfidentialCounts (CCPriorityId TEXT, CCLeadUnitId TEXT, CCTier TEXT,
    CCStage TEXT, CCRAG TEXT, CCPeriodEnd TEXT, CCCount INT);
CREATE INDEX idx_wi_stage ON WorkItems(Stage);
CREATE INDEX idx_wi_unit ON WorkItems(LeadUnitId);
CREATE INDEX idx_su_item ON StatusUpdates(ItemId, PeriodEnd);
CREATE INDEX idx_ir_status ON IntakeRequests(Status);
"""

UNITS_HEADS = {
    "DEAN": "M. Alvarez", "GTPE": "S. Whitfield", "GTLI": "R. Okafor",
    "CEISMC": "T. Nakamura", "SAV": "L. Brennan",
}

LEADS = [
    "J. Patel", "A. Kim", "D. Ross", "P. Nguyen", "C. Marshall", "E. Vasquez",
    "H. Lindqvist", "K. Osei", "M. Fontaine", "S. Dvorak", "T. Ibarra",
    "V. Kowalski", "B. Adeyemi", "F. Marchetti", "G. Hollins", "N. Petrov",
]

T1_ITEMS = [
    # (title, priority, objective, units, effort, cost, stage, rag_path)
    ("Learner Journey Analytics Platform", "SP-05", "SO-5.2", "DEAN,GTPE,GTLI", 1200, 85000, "Active", ["Green","Green","Green","Amber","Amber","Amber"]),
    ("Global Learning Hubs - Atlanta Pilot", "SP-02", "SO-2.2", "DEAN,GTPE", 800, 120000, "Active", ["Green","Green","Green","Green","Green","Green"]),
    ("Corporate Learning Partners Program", "SP-01", "SO-1.4", "GTPE,GTLI", 600, 40000, "Active", ["Green","Green","Amber","Amber","Amber","Red"]),
    ("SEVIS/F-1 Reporting System Upgrade", "SP-05", "SO-5.1", "GTLI", 350, 28000, "Active", ["Green","Amber","Amber","Green","Green","Green"]),
    ("Faculty Learning-Systems Fellows", "SP-01", "SO-1.1", "DEAN,GTLI", 900, 60000, "Active", ["Green","Green","Green","Green","Green","Green"]),
    ("Learning Tech Incubator - Cohort 3", "SP-02", "SO-2.4", "DEAN,GTPE", 750, 95000, "Active", ["Amber","Amber","Amber","Green","Green","Green"]),
    ("Savannah Campus Expansion Study", "SP-03", "SO-3.3", "SAV,DEAN", 500, 30000, "On Hold", ["Green","Green","Amber","Amber",None,None]),
    ("Credential Pathways Redesign", "SP-01", "SO-1.2", "DEAN,GTPE,GTLI", 1500, 150000, "Active", ["Green","Green","Green","Green","Green","Green"]),
    ("Alumni Lifetime Learning Portal", "SP-03", "SO-3.1", "GTPE,DEAN", 650, 45000, "Active", ["Green","Amber","Amber","Amber","Red","Red"]),
    ("Research Expenditures Growth Initiative", "SP-04", "SO-4.6", "DEAN", 480, 70000, "Active", ["Green","Green","Green","Green","Amber","Amber"]),
]

T2_ITEMS = [
    ("GTPE Course Catalog Refresh", "SP-03", "SO-3.4", "GTPE", 320, 12000, "Active", ["Green","Green","Green","Green","Green","Amber"]),
    ("GTLI Placement Testing Overhaul", "SP-03", "SO-3.2", "GTLI", 210, 8000, "Active", ["Green","Green","Green","Amber","Amber","Amber"]),
    ("CEISMC Summer Programs Registration System", None, None, "CEISMC", 400, 15000, "Active", ["Green","Green","Green","Green","Green","Green"]),
    ("GTPE Marketing Automation Rollout", None, None, "GTPE", 160, 6000, "Active", ["Amber","Amber","Green","Green","Green","Green"]),
    ("GTLI Instructor Onboarding Redesign", None, None, "GTLI", 120, 4000, "Active", ["Green","Green","Green","Green","Green","Green"]),
    ("DEAN Space Utilization Study", None, None, "DEAN", 90, 5000, "Closing", ["Green","Green","Green","Green","Green",None]),
    ("SAV Dual-Enrollment Agreement", "SP-03", "SO-3.3", "SAV", 100, 3000, "Active", ["Green","Green","Green","Green","Amber","Amber"]),
    ("CEISMC K-12 STEM Kit Modernization", None, None, "CEISMC", 95, 7000, "Approved", [None,None,None,None,None,None]),
    ("GTPE Compliance Training Refresh", None, None, "GTPE", 85, 2000, "Active", ["Green","Green","Green","Green","Green","Green"]),
    ("GTLI Evening Program Pricing Review", None, None, "GTLI", 80, 0, "Closed", ["Green","Green","Green","Green",None,None]),
    ("DEAN Records Digitization", None, None, "DEAN", 110, 9000, "Cancelled", ["Green","Green",None,None,None,None]),
]

CONFIDENTIAL_ITEMS = [
    ("Central Operations Restructure - Phase A", "SP-05", "SO-5.1", "DEAN", 300, 20000, "Active",
     ["Amber","Amber","Amber","Amber","Amber","Amber"], "HR-sensitive restructuring of central operations roles"),
    ("GTPE Vendor Contract Dispute Resolution", None, None, "GTPE", 80, 35000, "Active",
     ["Red","Red","Amber","Amber","Amber","Amber"], "Active legal dispute with course-platform vendor"),
    ("GTLI Personnel Investigation Support", None, None, "GTLI", 60, 0, "Closing",
     ["Amber","Amber","Green","Green",None,None], "Confidential personnel matter; workspace restricted"),
]

INTAKE = [
    ("Micro-credential Platform Evaluation", "A. Kim", "GTPE", "GTPE,GTLI", "SP-01", 700, 50000, "1",
     4, 5, 2, 3, 2, 3, "In Triage", None),
    ("Learning Hub - International Partner (Berlin)", "D. Ross", "GTPE", "GTPE,DEAN,GTLI", "SP-02", 900, 140000, "1",
     5, 4, 3, 2, 1, 2, "Awaiting Decision", None),
    ("CLL Brand Refresh", "P. Nguyen", "DEAN", "DEAN", None, 250, 30000, "1",
     3, 4, 2, 4, 3, 3, "Awaiting Decision", None),
    ("AI Tutoring Pilot for Language Learners", "R. Okafor", "GTLI", "GTLI,CEISMC", "SP-03", 400, 25000, "1",
     5, 5, 3, 3, 2, 3, "Ready for Review", None),
    ("Unit Intranet Migration (GTPE)", "S. Whitfield", "GTPE", "GTPE", None, 180, 12000, "2",
     None, None, None, None, None, None, "Submitted", None),
    ("Spring Intensive Program Launch", "M. Fontaine", "GTLI", "GTLI", "SP-03", 120, 5000, "2",
     None, None, None, None, None, None, "Approved", None),
    ("Accessibility Audit Remediation", "T. Nakamura", "CEISMC", "CEISMC", "SP-05", 300, 18000, "1",
     4, 3, 5, 3, 2, 2, "Awaiting Decision", None),
    ("Savannah Lab Equipment Refresh", "L. Brennan", "SAV", "SAV", None, 85, 22000, "2",
     None, None, None, None, None, None, "Needs Information", None),
    ("Lifetime Learning Podcast Series", "H. Lindqvist", "DEAN", "DEAN,GTPE", "SP-04", 260, 15000, "1",
     3, 3, 2, 4, 3, 4, "Deferred", "2027-01-15"),
    ("Legacy LMS Decommission", "V. Kowalski", "GTPE", "GTPE", "SP-05", 140, 8000, "2",
     None, None, None, None, None, None, "Declined", None),
    ("GTLI Student App Feedback System", "S. Dvorak", "GTLI", "GTLI", None, 90, 4000, "2",
     None, None, None, None, None, None, "Approved", None),
    ("College Data Dictionary Initiative", "K. Osei", "DEAN", "DEAN,GTPE,GTLI", "SP-05", 500, 35000, "1",
     5, 4, 4, 2, 3, 3, "In Triage", None),
]

PERIOD_ENDS = ["2026-04-30", "2026-05-31", "2026-06-30", "2026-07-31", "2026-08-31", "2026-09-15"]
SUBMIT_DATES = ["2026-04-28", "2026-05-29", "2026-06-29", "2026-07-30", "2026-08-28", "2026-09-14"]

GREEN_SUMMARIES = [
    "On plan this period; deliverables tracking to forecast.",
    "Steady progress; no impediments to report.",
    "Milestone work on track; team at full capacity.",
]
AMBER_SUMMARIES = [
    "At risk: schedule pressure from competing priorities; recovery plan in place and within control.",
    "Amber: vendor response slower than planned, but contractually recoverable this period.",
    "At risk: staffing gap for two weeks; internal reallocation agreed with unit head.",
]
RED_ASKS = [
    "Need TCC decision on additional $18K vendor budget by Oct 15 to hold the launch date; without it the window slips a quarter.",
    "Requesting a staffing decision: approve 0.5 FTE analyst through December, or descope the pilot to one unit.",
]

def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))

def main():
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)

    # ---- Units (skip the TODO row) ----
    for r in load_csv(SEED / "units.csv"):
        if r["Note"].strip() == "Remove this row":
            continue
        con.execute("INSERT INTO Units VALUES (?,?,?,?,?,?)",
            (r["UnitId"], r["Name"], UNITS_HEADS.get(r["UnitId"], ""),
             1 if r["Active"] == "TRUE" else 0, int(r["PilotWave"] or 0) or None, r["Note"]))

    # ---- Demo personas for role switching ----
    personas = [
        ("dean@gatech.edu", "DEAN", "Executive"),
        ("stratops@gatech.edu", "DEAN", "Executive"),
        ("gtpe-head@gatech.edu", "GTPE", "Unit"),
        ("gtli-head@gatech.edu", "GTLI", "Unit"),
    ]
    con.executemany("INSERT INTO UnitAccess VALUES (?,?,?)", personas)

    # ---- Strategy, objectives, KPIs from real seed ----
    for r in load_csv(SEED / "strategic-priorities.csv"):
        con.execute("INSERT INTO StrategicPriorities VALUES (?,?,?,?,?,?,?,?)",
            (r["PriorityId"], r["Title"], "", r["ExecOwner"], r["EffectiveFrom"],
             r["EffectiveTo"] or None, 1 if r["Provisional"] == "TRUE" else 0, r["Source"]))
    for r in load_csv(SEED / "strategic-objectives.csv"):
        con.execute("INSERT INTO StrategicObjectives VALUES (?,?,?,?)",
            (r["ObjectiveId"], r["PriorityId"], r["Title"], 1))
    for r in load_csv(SEED / "kpis.csv"):
        con.execute("INSERT INTO KPIs (KpiId,KpiName,KpiPriorityId,KpiObjectiveId,UnitOfMeasure,"
            "Direction,Baseline,Target,TargetDate,Frequency,Method,ProvisionalFlag,KpiNote) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (r["KpiId"], r["Name"], r["PriorityId"], r["ObjectiveId"] or None, r["UnitOfMeasure"],
             r["Direction"], float(r["Baseline"]) if r["Baseline"] else None,
             float(r["Target"]) if r["Target"] else None, r["TargetDate"] or None,
             r["Frequency"], r["Method"], 1 if r["Provisional"] == "TRUE" else 0, r["Note"]))

    # ---- KPI values (quarterly history) ----
    kpi_vals = {
        "KPI-001": [820, 910, 990],
        "KPI-002": [1, 1, 1],
        "KPI-003": [12, 15, 18],
        "KPI-004": [46, 52, 61],
        "KPI-005": [6, 7, 8],
        "KPI-006": [1450000, 1620000, 1810000],
        "KPI-007": [420000, 455000, 498000],
        "KPI-008": [71.2, 71.9, 72.4],   # baseline pending: target defined as 2x baseline
        "KPI-009": [28, 30, 31],
        "KPI-010": [4300000, 4450000, 4620000],
        "KPI-011": [12, 18, 22],
    }
    periods = ["2026-03-31", "2026-06-30", "2026-09-15"]
    for kid, vals in kpi_vals.items():
        for p, v in zip(periods, vals):
            con.execute("INSERT INTO KpiValues VALUES (?,?,?,?,?)",
                (kid, p, v, "", "Institutional Research"))

    # ---- Work items ----
    def insert_item(n, level, title, pri, obj, unit, contributing, tier, stage,
                    effort, cost, conf, backfilled, reqid, start, end, exec_tool):
        item_id = f"CLL-26-{n:04d}"
        con.execute("INSERT INTO WorkItems (ItemId,Level,Title,ParentId,WorkPortfolioId,"
            "PrimaryPriorityId,PrimaryObjectiveId,SecondaryPriorityIds,AlignmentCategory,"
            "AlignmentJustification,Tier,LeadUnitId,ContributingUnitIds,Sponsor,Lead,Stage,"
            "StartDate,TargetEndDate,BaselineEndDate,StageChangedOn,StageChangedBy,"
            "EffortEstimateHrs,CostEstimate,ExecutionTool,ExecutionLink,WorkspaceUrl,"
            "CharterUrl,KpiIds,Confidential,Backfilled,RequestId) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (item_id, level, title, None, None, pri, obj, None,
             "Strategic" if pri else "Operational",
             "Compliance-mandated" if "SEVIS" in title else None,
             tier, unit, contributing, "Bill" if tier == "1" else UNITS_HEADS.get(unit, ""),
             random.choice(LEADS), stage, start, end, end,
             "2026-04-01", "Strategic Operations", effort, cost, exec_tool, None,
             f"https://gatech.sharepoint.com/sites/CLL-SPM/{item_id}" if tier == "1" else None,
             f"https://gatech.sharepoint.com/sites/CLL-SPM/{item_id}/charter.docx" if tier == "1" else None,
             None,  # KpiIds
             1 if conf else 0, 1 if backfilled else 0, reqid))
        return item_id

    n = 2  # CLL-26-0001 is the standing backfill row; load it too
    for r in load_csv(SEED / "work-items-backfill.csv"):
        con.execute("INSERT INTO WorkItems (ItemId,Level,Title,PrimaryPriorityId,PrimaryObjectiveId,"
            "AlignmentCategory,Tier,LeadUnitId,ContributingUnitIds,Sponsor,Lead,Stage,StartDate,"
            "TargetEndDate,ExecutionTool,Confidential,Backfilled) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (r["ItemId"], r["Level"], r["Title"], r["PrimaryPriorityId"], r["PrimaryObjectiveId"],
             r["AlignmentCategory"], r["Tier"], r["LeadUnitId"], r["ContributingUnitIds"],
             r["Sponsor"], r["Lead"], r["Stage"], r["StartDate"], r["TargetEndDate"],
             r["ExecutionTool"], 0, 1))

    item_rows = []          # (item_id, rags, stage, conf)
    start = "2026-04-01"
    for (title, pri, obj, units, effort, cost, stage, rags) in T1_ITEMS:
        lead_unit = units.split(",")[0]
        iid = insert_item(n, "Project", title, pri, obj, lead_unit, units, "1", stage,
                           effort, cost, False, True, f"REQ-26-{n:04d}", start, "2027-03-31", "Asana")
        item_rows.append((iid, rags, stage, False))
        n += 1
    for (title, pri, obj, unit, effort, cost, stage, rags) in T2_ITEMS:
        iid = insert_item(n, "Project", title, pri, obj, unit, None, "2", stage,
                          effort, cost, False, True, f"REQ-26-{n:04d}", start, "2026-12-18", "Smartsheet")
        item_rows.append((iid, rags, stage, False))
        n += 1
    for (title, pri, obj, unit, effort, cost, stage, rags, _why) in CONFIDENTIAL_ITEMS:
        iid = insert_item(n, "Project", title, pri, obj, unit, None, "2" if effort < 400 else "1",
                          stage, effort, cost, True, True, f"REQ-26-{n:04d}", start, "2027-01-30", "Teams")
        item_rows.append((iid, rags, stage, True))
        n += 1

    # ---- Status updates (append-only history; the D5 fact table) ----
    for (iid, rags, stage, conf) in item_rows:
        for i, rag in enumerate(rags):
            if rag is None:
                continue
            if conf:
                summ = "Confidential item; details restricted. Overall trend managed with sponsor."
                path = "Managed within the unit; executive sponsor briefed monthly." if rag == "Red" else None
                ask = None
                pct = 40 + 8 * i
            elif rag == "Red":
                summ = "Off track: critical dependency slipped beyond the lead's authority to resolve."
                path = "Recover by re-sequencing the launch milestone and holding vendor to contract SLAs."
                ask = random.choice(RED_ASKS)
                pct = max(10, 35 + 5 * i)
            elif rag == "Amber":
                summ = random.choice(AMBER_SUMMARIES)
                path = None; ask = None
                pct = 30 + 10 * i
            else:
                summ = random.choice(GREEN_SUMMARIES)
                path = None; ask = None
                pct = 35 + 10 * i
            con.execute("INSERT INTO StatusUpdates VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (iid, PERIOD_ENDS[i], rag, rag, "Green", "Green", summ, path,
                 "Executive review", "2026-10-30", min(pct, 95),
                 1 if (rag == "Red" and i == len(rags) - 1) else 0, ask,
                 "lead@example.com", SUBMIT_DATES[i]))

    # ---- Milestones (executive, next 90 days + one past) ----
    ms = [
        ("CLL-26-0002", "Learner Analytics MVP live", "2026-09-30", "2026-10-15", None),
        ("CLL-26-0003", "Hub partner MOU signed", "2026-10-01", "2026-10-20", None),
        ("CLL-26-0008", "Fellows cohort announced", "2026-11-01", "2026-11-10", None),
        ("CLL-26-0010", "Portal beta to 500 alumni", "2026-10-15", "2026-11-05", None),
        ("CLL-26-0002", "Data pipeline v1 (past)", "2026-07-31", "2026-07-28", "2026-07-28"),
    ]
    for (iid, title, base, forecast, actual) in ms:
        con.execute("INSERT INTO Milestones VALUES (?,?,?,?,?,?)",
            (iid, title, base, forecast, actual, 1))

    # ---- Intake requests ----
    for (title, requester, unit, contributing, pri, effort, cost, tier,
         sa, sv, su, sc, se, sr, status, revisit) in INTAKE:
        reqid = f"REQ-26-{n:04d}"
        submitted = (TODAY - dt.timedelta(days=random.randint(3, 40))).isoformat()
        # tier classification per D14: contributing units -> Tier 1 at submission
        eff_tier = "1" if (contributing and len(contributing.split(",")) >= 2) else tier
        con.execute("INSERT INTO IntakeRequests (RequestId,Title,Requester,ReqUnitId,"
            "ContributingUnitIds,Problem,ProposedPriorityId,EffortEst,CostEst,"
            "ExternalCommitment,Tier,ScoreAlignment,ScoreValue,ScoreUrgency,ScoreCapacity,"
            "ScoreEffort,ScoreRisk,TriageOwner,Status,RevisitDate,SubmittedDate) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (reqid, title, requester, unit, contributing,
             "See attached problem statement (demo data).", pri, effort, cost,
             1 if (cost or 0) >= 25000 and "External" in title else 0, eff_tier,
             sa, sv, su, sc, se, sr,
             "K. Osei" if status not in ("Submitted",) else None,
             status, revisit, submitted))
        if status in ("Approved", "Deferred", "Declined"):
            dec_id = f"DEC-26-{n:04d}"
            body = "TCC" if eff_tier == "1" else "Unit Head"
            con.execute("INSERT INTO Decisions VALUES (?,?,?,?,?,?,?,?,?)",
                (dec_id, (TODAY - dt.timedelta(days=random.randint(5, 20))).isoformat(),
                 body, reqid, status, "Per scoring rubric and tier criteria (demo).",
                 "Report monthly from activation" if status == "Approved" else None,
                 None, "Strategic Operations"))
        n += 1

    con.execute("INSERT INTO Counters VALUES ('CLL', 26, ?)", (n,))
    con.execute("INSERT INTO Counters VALUES ('REQ', 26, ?)", (n,))
    con.execute("INSERT INTO Counters VALUES ('DEC', 26, ?)", (n,))

    # ---- ConfidentialCounts snapshot (D13: refresh-time, non-identifying) ----
    for (iid, rags, stage, conf) in item_rows:
        if not conf:
            continue
        pri, unit, tier = con.execute(
            "SELECT PrimaryPriorityId, LeadUnitId, Tier FROM WorkItems WHERE ItemId=?",
            (iid,)).fetchone()
        last_rag = next((r for r in reversed(rags) if r), "Green")
        con.execute("INSERT INTO ConfidentialCounts VALUES (?,?,?,?,?,?,?)",
            (pri, unit, tier, stage, last_rag, PERIOD_ENDS[-1], 1))

    con.commit()
    counts = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in
              ("WorkItems", "StatusUpdates", "Milestones", "IntakeRequests", "Decisions", "KpiValues")}
    con.close()
    print(f"Built {DB}")
    for t, c in counts.items():
        print(f"  {t}: {c} rows")

if __name__ == "__main__":
    main()