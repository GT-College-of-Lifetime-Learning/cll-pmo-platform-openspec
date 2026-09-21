# CLL-SPM demo flow engine — local implementations of the Power Automate flows
# (F1-F7) so the demo stands alone with no OIT/M365 dependency.
#
# Mirrors the specs exactly:
#   F1 intake (design D14: contributing units captured at submission; multi-unit -> Tier 1)
#   F2 decision routing (D11: Tier 1 -> TCC, Tier 2 -> unit head + 10-business-day
#      call-up window; approval creates the registry item linked both ways)
#   F4 status intake (Red requires path-to-green or decision ask)
#   F7 hygiene (triage overdue, unit-head decision SLA, call-up window close)
#   Stage changes (activation gates, closeout summary requirement, append-only log)

import sqlite3
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

# Shared template environment with the app (single Jinja global registry —
# trust_state etc. are registered once in app.py and apply to every page).
from demo.app import templates

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "demo" / "cll_spm.db"

TODAY = date(2026, 9, 19)

TIER1_RULES = {
    # "any one qualifies" (design D3)
    "cross_unit": lambda f: len([u for u in (f.get("contributing") or "").split(",") if u.strip()]) >= 1
                              and bool(f.get("contributing")),
    "external": lambda f: f.get("external") == "on",
    "cost": lambda f: (f.get("cost") or 0) >= 25000,
    "effort": lambda f: (f.get("effort") or 0) >= 400,
    "named_deliverable": lambda f: bool(f.get("named_deliverable")),
}
TIER2_RULES = {
    "effort": lambda f: (f.get("effort") or 0) >= 80,
    "duration": lambda f: False,  # duration captured at triage; form estimate only
    "new_launch": lambda f: f.get("new_launch") == "on",
}

STAGES = ["Proposed", "Approved", "Active", "On Hold", "Closing", "Closed", "Cancelled"]

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

# ---------- Counters-based ID generation (design D10) ----------

def next_id(con, prefix, year=26):
    """Generate the next identifier for a prefix/year, mirroring the Counters flow."""
    row = con.execute(
        "SELECT Next FROM Counters WHERE Prefix=? AND CounterYear=?", (prefix, year)).fetchone()
    if row is None:
        con.execute("INSERT INTO Counters VALUES (?,?,1)", (prefix, year))
        n = 1
    else:
        n = row["Next"]
        con.execute("UPDATE Counters SET Next=? WHERE Prefix=? AND CounterYear=?",
                    (n + 1, prefix, year))
    return f"{prefix}-{year}-{n:04d}"

def classify_tier(form):
    """D3 tier classification from submitted data. Multi-unit -> Tier 1 (D14)."""
    contributing = [u.strip() for u in (form.get("contributing") or "").split(",") if u.strip()]
    if len(contributing) >= 1:
        return "1", "cross-unit work"
    if any(rule(form) for rule in TIER1_RULES.values()):
        return "1", "Tier 1 threshold met"
    if any(rule(form) for rule in TIER2_RULES.values()):
        return "2", "Tier 2 threshold met"
    return None, "below Tier 2 thresholds - operational, not registered"

def add_business_days(con, from_date, n):
    """Add n business days using the BusinessDays table (F5/F7 window math)."""
    d = from_date
    added = 0
    while added < n:
        d += timedelta(days=1)
        row = con.execute("SELECT IsBusinessDay FROM BusinessDays WHERE Date=?",
                          (d.isoformat(),)).fetchone()
        if row and row["IsBusinessDay"]:
            added += 1
    return d

def business_days_between(con, start, end):
    if end < start:
        return 0
    row = con.execute(
        "SELECT COUNT(*) FROM BusinessDays WHERE Date>=? AND Date<=? AND IsBusinessDay=1",
        (start.isoformat(), end.isoformat())).fetchone()
    return row[0]

def register_flow_routes(app: FastAPI):

    # ---------- F1: intake (design D14) ----------

    @app.get("/intake", response_class=HTMLResponse)
    def intake_form(request: Request):
        con = db()
        units = con.execute("SELECT * FROM Units WHERE UnitActive=1 ORDER BY UnitId").fetchall()
        con.close()
        return templates.TemplateResponse(request, "intake.html", {
            "request": request, "role": _role(request), "units": [dict(u) for u in units],
        })

    @app.post("/intake/submit")
    def intake_submit(
        request: Request,
        title: str = Form(...),
        requester: str = Form(...),
        unit: str = Form(...),
        contributing: str = Form(""),
        problem: str = Form(...),
        priority: str = Form(""),
        effort: int = Form(0),
        cost: int = Form(0),
        external: str = Form(""),
        new_launch: str = Form(""),
    ):
        con = db()
        form = {"title": title, "requester": requester, "unit": unit, "contributing": contributing,
                "problem": problem, "priority": priority, "effort": effort, "cost": cost,
                "external": external, "new_launch": new_launch}
        tier, why = classify_tier(form)
        reqid = next_id(con, "REQ")
        con.execute(
            """INSERT INTO IntakeRequests (RequestId,Title,Requester,ReqUnitId,
               ContributingUnitIds,Problem,ProposedPriorityId,EffortEst,CostEst,
               ExternalCommitment,Tier,TriageOwner,Status,SubmittedDate)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (reqid, title, requester, unit, contributing or None, problem, priority or None,
             effort or None, cost or None, 1 if external else 0, tier,
             None, "Submitted", TODAY.isoformat()))
        con.commit()
        con.close()
        return RedirectResponse(f"/requests/{reqid}?as={request.query_params.get('as','executive')}",
                                status_code=303)

    # ---------- Requester status view (spec 3.6) ----------

    @app.get("/requests/{reqid}", response_class=HTMLResponse)
    def request_status(request: Request, reqid: str):
        con = db()
        req = con.execute("SELECT * FROM IntakeRequests WHERE RequestId=?", (reqid,)).fetchone()
        decisions = con.execute(
            "SELECT * FROM Decisions WHERE SubjectId=? ORDER BY DecisionDate DESC", (reqid,)).fetchall()
        con.close()
        if req is None:
            return HTMLResponse("<h3>Request not found</h3>", status_code=404)
        return templates.TemplateResponse(request, "request.html", {
            "request": request, "role": _role(request),
            "req": dict(req), "decisions": [dict(d) for d in decisions],
            "today": TODAY.isoformat(),
        })

    # ---------- Triage (F2 data check, not merit review) ----------

    @app.post("/requests/{reqid}/triage")
    def triage_action(request: Request, reqid: str,
                      action: str = Form(...),
                      tier: str = Form(""),
                      triage_owner: str = Form("Strategic Operations"),
                      missing: str = Form(""),
                      priority: str = Form("")):
        con = db()
        req = con.execute("SELECT * FROM IntakeRequests WHERE RequestId=?", (reqid,)).fetchone()
        if req is None:
            con.close()
            return HTMLResponse("not found", status_code=404)
        if action == "needs_info":
            con.execute("UPDATE IntakeRequests SET Status='Needs Information', TriageOwner=? WHERE RequestId=?",
                        (triage_owner, reqid))
        elif action == "complete":
            new_tier = tier or req["Tier"]
            # reclassification to Tier 1 routes to TCC (spec scenario)
            con.execute("UPDATE IntakeRequests SET Status='Ready for Review', Tier=?, TriageOwner=?, ProposedPriorityId=? WHERE RequestId=?",
                        (new_tier, triage_owner, priority or req["ProposedPriorityId"], reqid))
        con.commit()
        con.close()
        return RedirectResponse(f"/requests/{reqid}?as={request.query_params.get('as','executive')}",
                                status_code=303)

    # ---------- F2: decision routing + approval -> WorkItem ----------

    @app.post("/requests/{reqid}/decide")
    def decide_action(request: Request, reqid: str,
                      decision: str = Form(...),
                      rationale: str = Form(""),
                      conditions: str = Form(""),
                      revisit_date: str = Form(""),
                      decides_as: str = Form("TCC")):
        con = db()
        req = con.execute("SELECT * FROM IntakeRequests WHERE RequestId=?", (reqid,)).fetchone()
        if req is None:
            con.close()
            return HTMLResponse("not found", status_code=404)

        dec_id = next_id(con, "DEC")
        decision_map = {"approve": "Approved", "approve_cond": "Approved with Conditions",
                        "defer": "Deferred", "decline": "Declined"}
        dec_text = decision_map[decision]

        # Tier 2 approvals open the 10-business-day TCC call-up window (D11)
        callup_until = None
        if req["Tier"] == "2" and decision in ("approve", "approve_cond"):
            callup_until = add_business_days(con, TODAY, 10).isoformat()

        con.execute(
            "INSERT INTO Decisions VALUES (?,?,?,?,?,?,?,?,?)",
            (dec_id, TODAY.isoformat(), decides_as, reqid, dec_text, rationale, conditions or None,
             None, "Strategic Operations"))

        new_status = {"Approved": "Approved", "Approved with Conditions": "Approved",
                      "Deferred": "Deferred", "Declined": "Declined"}[dec_text]
        linked_item = req["LinkedItemId"]
        if new_status == "Approved" and not linked_item:
            # approval creates the registry item, linked both ways (spec)
            item_id = next_id(con, "CLL")
            con.execute(
                """INSERT INTO WorkItems (ItemId,Level,Title,PrimaryPriorityId,PrimaryObjectiveId,
                   AlignmentCategory,Tier,LeadUnitId,ContributingUnitIds,Sponsor,Lead,Stage,
                   StartDate,TargetEndDate,StageChangedOn,StageChangedBy,EffortEstimateHrs,
                   CostEstimate,Confidential,Backfilled,RequestId)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (item_id, "Project", req["Title"], req["ProposedPriorityId"], None,
                 "Strategic" if req["ProposedPriorityId"] else "Operational",
                 req["Tier"], req["ReqUnitId"], req["ContributingUnitIds"],
                 None, req["Requester"], "Approved", TODAY.isoformat(), None,
                 TODAY.isoformat(), "Strategic Operations",
                 req["EffortEst"], req["CostEst"], 0, 0, reqid))
            con.execute("UPDATE IntakeRequests SET LinkedItemId=? WHERE RequestId=?", (item_id, reqid))
            linked_item = item_id

        con.execute("UPDATE IntakeRequests SET Status=?, DecisionId=?, RevisitDate=? WHERE RequestId=?",
                    (new_status, dec_id, revisit_date or None, reqid))

        # call-up window state lives on the decision note (demo: separate table would be
        # the production design; the window close is handled by F7 below)
        if callup_until:
            con.execute("UPDATE Decisions SET Conditions=COALESCE(Conditions,'') || ? WHERE DecisionId=?",
                        (f" | Tier 2 call-up window open until {callup_until}", dec_id))
        con.commit()
        con.close()
        return RedirectResponse(f"/requests/{reqid}?as={request.query_params.get('as','executive')}",
                                status_code=303)

    # ---------- D11: TCC call-up ----------

    @app.post("/requests/{reqid}/callup")
    def callup_action(request: Request, reqid: str, member: str = Form("TCC member")):
        con = db()
        req = con.execute("SELECT * FROM IntakeRequests WHERE RequestId=?", (reqid,)).fetchone()
        if req is None or req["Status"] != "Approved" or req["Tier"] != "2":
            con.close()
            return HTMLResponse("Only approved Tier 2 requests can be called up", status_code=400)
        # Called-up item stays Approved but cannot become Active until the TCC decides
        con.execute("UPDATE IntakeRequests SET Status='Awaiting Decision' WHERE RequestId=?", (reqid,))
        dec_id = next_id(con, "DEC")
        con.execute("INSERT INTO Decisions VALUES (?,?,?,?,?,?,?,?,?)",
                    (dec_id, TODAY.isoformat(), "TCC", reqid, "Called Up",
                     f"Called up by {member}; item cannot become Active until TCC records a decision",
                     None, None, member))
        con.commit()
        con.close()
        return RedirectResponse(f"/requests/{reqid}?as={request.query_params.get('as','executive')}",
                                status_code=303)

    # ---------- F4: status update form (Red requires path/ask) ----------

    @app.get("/update/{item_id}", response_class=HTMLResponse)
    def status_form(request: Request, item_id: str):
        con = db()
        item = con.execute("SELECT * FROM WorkItems WHERE ItemId=?", (item_id,)).fetchone()
        prefill = None
        if item is not None and item["SyncEnabled"]:
            import demo.sync_engine as sync_engine
            plan = sync_engine.load_plan(item_id)
            if plan:
                prefill = {"percent_complete": plan.get("percent_complete"),
                           "source": "plan sync (one-way)"}
        con.close()
        if item is None:
            return HTMLResponse("<h3>Item not found</h3>", status_code=404)
        return templates.TemplateResponse(request, "status_form.html", {
            "request": request, "role": _role(request), "item": dict(item),
            "prefill": prefill,
        })

    @app.post("/update/{item_id}/submit")
    def status_submit(request: Request, item_id: str,
                      overall: str = Form(...),
                      schedule: str = Form("Green"),
                      scope: str = Form("Green"),
                      resources: str = Form("Green"),
                      summary: str = Form(""),
                      path_to_green: str = Form(""),
                      next_milestone: str = Form(""),
                      next_milestone_date: str = Form(""),
                      pct: int = Form(0),
                      decision_needed: str = Form(""),
                      decision_ask: str = Form("")):
        con = db()
        # F4 validation: Red requires path-to-green or a decision ask (spec)
        if overall == "Red" and not path_to_green.strip() and not decision_ask.strip():
            con.close()
            item = {"ItemId": item_id, "Title": ""}
            return templates.TemplateResponse(request, "status_form.html", {
                "request": request, "role": _role(request), "item": dict(item),
                "error": "Red status requires a path to green or a decision ask — the update was not saved.",
            }, status_code=422)
        if decision_needed and not decision_ask.strip():
            con.close()
            return HTMLResponse("Decision Needed selected: describe the ask", status_code=422)
        con.execute(
            """INSERT INTO StatusUpdates VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (item_id, TODAY.isoformat(), overall, schedule, scope, resources, summary,
             path_to_green or None, next_milestone or None, next_milestone_date or None,
             pct, 1 if decision_needed else 0, decision_ask or None,
             "demo-user", TODAY.isoformat()))
        con.commit()
        con.close()
        return RedirectResponse(f"/item/{item_id}?as={request.query_params.get('as','executive')}",
                                status_code=303)

    # ---------- Stage changes (activation gates, closeout) ----------

    @app.post("/items/{item_id}/stage")
    def stage_change(request: Request, item_id: str, stage: str = Form(...),
                     closeout: str = Form("")):
        con = db()
        item = con.execute("SELECT * FROM WorkItems WHERE ItemId=?", (item_id,)).fetchone()
        if item is None:
            con.close()
            return HTMLResponse("not found", status_code=404)

        errors = []
        # Registry spec: required data before activation
        if stage == "Active":
            for field, label in (("Title", "title"), ("LeadUnitId", "lead unit"),
                                 ("Lead", "lead"), ("Sponsor", "sponsor"),
                                 ("StartDate", "start date"), ("TargetEndDate", "target end date")):
                if not item[field]:
                    errors.append(label)
            if item["Tier"] == "1" and not item["CharterUrl"]:
                errors.append("charter link (Tier 1)")
            # Tier 2 call-up block (D11)
            req = con.execute("SELECT Status FROM IntakeRequests WHERE RequestId=?",
                              (item["RequestId"] or "",)).fetchone()
            if req and req["Status"] == "Awaiting Decision":
                errors.append("TCC call-up pending — cannot become Active until the TCC decides")
        if stage == "Closed" and item["Tier"] == "1" and not closeout.strip():
            errors.append("closeout summary")
        # finding-tracker spec: Open finding with 4+ occurrences blocks closeout
        from demo.findings import closeout_blocked
        if stage == "Closed" and closeout_blocked(con, item_id):
            blocked = con.execute(
                "SELECT Type, Occurrences FROM Findings WHERE AffectedItemId=?"
                " AND Status='Open' AND Occurrences>=4 ORDER BY Occurrences DESC LIMIT 1",
                (item_id,)).fetchone()
            errors.append(
                f"unresolved finding ({blocked['Type']}, {blocked['Occurrences']} occurrences) — "
                "resolve it before closing")

        if errors:
            con.close()
            return HTMLResponse(
                f"<h3>Stage change rejected</h3><p>Missing: {', '.join(errors)}. "
                f"<a href='/item/{item_id}'>Back to item</a></p>", status_code=422)

        con.execute("UPDATE WorkItems SET Stage=?, StageChangedOn=?, StageChangedBy=? WHERE ItemId=?",
                    (stage, TODAY.isoformat(), "demo-user", item_id))
        con.commit()
        con.close()
        return RedirectResponse(f"/item/{item_id}?as={request.query_params.get('as','executive')}",
                                status_code=303)

    # ---------- F7 hygiene: findings + close expired call-up windows ----------

    @app.post("/admin/hygiene")
    def hygiene_run(request: Request):
        con = db()
        from demo.findings import run_hygiene_findings, open_findings
        touched = run_hygiene_findings(con)
        closed = 0
        rows = con.execute(
            "SELECT DecisionId, Conditions FROM Decisions WHERE Decision LIKE '%call-up window open until%'").fetchall()
        for row in rows:
            until = row["Conditions"].split("until ")[-1].strip()
            try:
                until_date = date.fromisoformat(until)
            except ValueError:
                continue
            if until_date < TODAY:
                closed += 1
                con.execute("UPDATE Decisions SET Conditions=REPLACE(?, 'open until', 'closed since') WHERE DecisionId=?",
                            (row["Conditions"], row["DecisionId"]))
        triage_late = con.execute(
            "SELECT COUNT(*) FROM IntakeRequests WHERE Status='Submitted' AND JULIANDAY('2026-09-19')-JULIANDAY(SubmittedDate)>5").fetchone()[0]
        escalated = open_findings(con, min_occurrences=2)
        con.commit()
        con.close()
        return templates.TemplateResponse(request, "hygiene.html", {
            "request": request, "role": _role(request),
            "findings_touched": touched,
            "callup_closed": closed,
            "triage_late": triage_late,
            "escalated": [dict(f) for f in escalated],
        })

def _role(request: Request):
    as_param = request.query_params.get("as", "executive")
    if as_param.startswith("unit:"):
        return {"kind": "Unit", "unit": as_param.split(":", 1)[1]}
    return {"kind": "Executive", "unit": None}