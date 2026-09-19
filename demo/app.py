# CLL-SPM demo app — FastAPI serving the executive dashboard views specced in
# add-portfolio-registry-and-exec-dashboards, over SQLite (demo/cll_spm.db).
#
# Implements the observable behavior of the specs where the demo runs:
#   - Dean overview (executive-dashboards spec): decisions needed first, health
#     by priority (G/A/R/Stale), exec milestones next 90 days, KPI progress,
#     status currency, effort split, "+N Confidential" (D13).
#   - Governance view: intake pipeline by stage and age, requests with scores,
#     recent decisions.
#   - Unit view: own items, action needed (stale/overdue/unaligned), milestones.
#   - Item detail: status history, milestones, decisions.
#   - Role-based access (D7/D13): ?as=executive | ?as=unit:<UNITID>
#     Confidential items: hidden from other units, visible to own unit and
#     executives; masked counts always visible (ConfidentialCounts).
#
# Run:  uvicorn demo.app:app --reload     (from repo root)
# Then: http://127.0.0.1:8000/?as=executive

import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

ROOT = Path(__file__).resolve().parent.parent
DB = Path(__file__).resolve().parent / "cll_spm.db"
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

app = FastAPI(title="CLL-SPM Demo")

TODAY = date(2026, 9, 19)

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def role(request: Request):
    """Demo persona from ?as=. Default: executive (the Dean demo path)."""
    as_param = request.query_params.get("as", "executive")
    if as_param.startswith("unit:"):
        return {"kind": "Unit", "unit": as_param.split(":", 1)[1]}
    return {"kind": "Executive", "unit": None}

# ---------- role-filtered item rows (D7 + D13) ----------

def visible_items(con, r, unit):
    rows = con.execute("SELECT * FROM WorkItems").fetchall()
    if r["kind"] == "Executive":
        return rows
    out = []
    for row in rows:
        if row["Confidential"]:
            if row["LeadUnitId"] == unit:
                out.append(row)
        elif row["Tier"] == "1" or row["LeadUnitId"] == unit:
            out.append(row)
    return out

def latest_status(con, item_ids):
    if not item_ids:
        return {}
    q = f"""SELECT s.* FROM StatusUpdates s
            JOIN (SELECT ItemId, MAX(PeriodEnd) AS pe FROM StatusUpdates
                  WHERE ItemId IN ({','.join('?'*len(item_ids))})
                  GROUP BY ItemId) m
            ON s.ItemId = m.ItemId AND s.PeriodEnd = m.pe"""
    return {row["ItemId"]: row for row in con.execute(q, item_ids).fetchall()}

def stale_flag(su):
    """Stale = no update within the period + 5 business days (status-reporting spec).
    Demo period end 2026-09-15 + ~1wk => current. Last update <= 2026-08-31 => stale."""
    if su is None:
        return True
    return su["PeriodEnd"] <= "2026-08-31"

# ---------- views ----------

@app.get("/", response_class=HTMLResponse)
def dean_overview(request: Request):
    r = role(request)
    con = db()
    items = visible_items(con, r, r["unit"])
    ids = [i["ItemId"] for i in items]
    su = latest_status(con, ids)

    decisions = []
    for i in items:
        s = su.get(i["ItemId"])
        if s and s["DecisionNeeded"]:
            decisions.append({"item": i, "status": s})

    def health():
        out = {}
        for i in items:
            pri = i["PrimaryPriorityId"] or "(Operational)"
            s = su.get(i["ItemId"])
            rag = (s["OverallRAG"] if s else None) or "Stale"
            if stale_flag(s):
                rag = "Stale"
            bucket = out.setdefault(pri, {"Green": 0, "Amber": 0, "Red": 0, "Stale": 0,
                                           "title": pri})
            bucket[rag] += 1
        return out

    # masked confidential counts (D13): totals include what detail rows hide
    masked = {}
    for row in con.execute("SELECT CCPriorityId, SUM(CCCount) AS n FROM ConfidentialCounts GROUP BY CCPriorityId"):
        masked[row["CCPriorityId"]] = row["n"]

    priorities = con.execute(
        "SELECT * FROM StrategicPriorities ORDER BY PriorityId").fetchall()
    for p in priorities:
        p = dict(p)
    pri_health = health()

    milestones = con.execute(
        """SELECT m.*, w.Title FROM Milestones m JOIN WorkItems w ON m.ItemId = w.ItemId
           WHERE m.IsExecutive = 1 AND m.ForecastDate IS NOT NULL
           ORDER BY m.ForecastDate""").fetchall()
    # respect role visibility on milestones
    visible_ids = set(ids)
    milestones = [m for m in milestones if m["ItemId"] in visible_ids]

    kpis = con.execute(
        """SELECT k.*, (SELECT Value FROM KpiValues v WHERE v.KpiValueId = k.KpiId
              ORDER BY v.PeriodEnd DESC LIMIT 1) AS LatestValue
           FROM KPIs k ORDER BY k.KpiId""").fetchall()

    active = [i for i in items if i["Stage"] in ("Active", "On Hold")]
    current = [i for i in active if not stale_flag(su.get(i["ItemId"]))]
    currency = (100 * len(current) // len(active)) if active else 0

    def effort(cat):
        return sum(i["EffortEstimateHrs"] or 0 for i in active
                   if (i["AlignmentCategory"] or "Operational") == cat)
    tot_eff = effort("Strategic") + effort("Operational") + effort("Compliance") or 1

    con.close()
    return templates.TemplateResponse(request, "dean.html", {
        "request": request, "role": r,
        "decisions": decisions,
        "priorities": [dict(p) for p in priorities],
        "health": pri_health, "masked": masked,
        "milestones": milestones,
        "kpis": kpis,
        "currency_pct": currency,
        "active_count": len(active),
        "stale_count": len(active) - len(current),
        "effort_strategic_pct": 100 * effort("Strategic") // tot_eff,
        "effort_operational_pct": 100 * effort("Operational") // tot_eff,
        "effort_compliance_pct": 100 * effort("Compliance") // tot_eff,
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

@app.get("/governance", response_class=HTMLResponse)
def governance(request: Request):
    con = db()
    reqs = con.execute(
        """SELECT r.*, (COALESCE(r.ScoreAlignment,0)*0.25 + COALESCE(r.ScoreValue,0)*0.25 +
               COALESCE(r.ScoreUrgency,0)*0.15 + COALESCE(r.ScoreCapacity,0)*0.15 +
               COALESCE(r.ScoreEffort,0)*0.10 + COALESCE(r.ScoreRisk,0)*0.10) AS ScoreTotal
           FROM IntakeRequests r
           WHERE r.Status NOT IN ('Approved','Declined')
           ORDER BY r.Status, r.ScoreTotal DESC""").fetchall()
    tier2 = con.execute(
        """SELECT r.* FROM IntakeRequests r WHERE r.Status='Approved' AND r.Tier='2'""").fetchall()
    decisions = con.execute(
        "SELECT * FROM Decisions ORDER BY DecisionDate DESC LIMIT 8").fetchall()
    con.close()
    return templates.TemplateResponse(request, "governance.html", {
        "request": request, "role": role(request),
        "requests": [dict(r) for r in reqs],
        "tier2": [dict(t) for t in tier2],
        "decisions": [dict(d) for d in decisions],
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

@app.get("/unit/{unit_id}", response_class=HTMLResponse)
def unit_view(request: Request, unit_id: str):
    con = db()
    r = role(request)
    # unit leaders see their own unit; executives can inspect any
    eff_unit = unit_id
    items = con.execute("SELECT * FROM WorkItems WHERE LeadUnitId = ?", (eff_unit,)).fetchall()
    su = latest_status(con, [i["ItemId"] for i in items])

    action_needed = []
    for i in items:
        s = su.get(i["ItemId"])
        why = []
        if stale_flag(s):
            why.append("Stale")
        if not (i["PrimaryPriorityId"] or i["AlignmentCategory"]):
            why.append("Unaligned")
        if why:
            action_needed.append({"item": dict(i), "why": why})

    milestones = con.execute(
        """SELECT m.*, w.Title FROM Milestones m JOIN WorkItems w ON m.ItemId = w.ItemId
           WHERE w.LeadUnitId = ? AND m.ForecastDate IS NOT NULL ORDER BY m.ForecastDate""",
        (eff_unit,)).fetchall()

    unit = con.execute("SELECT * FROM Units WHERE UnitId = ?", (eff_unit,)).fetchone()
    con.close()
    return templates.TemplateResponse(request, "unit.html", {
        "request": request, "role": r, "unit": dict(unit) if unit else {"UnitId": unit_id, "Name": unit_id},
        "items": [dict(i) for i in items],
        "statuses": {k: dict(v) for k, v in su.items()},
        "action_needed": action_needed,
        "milestones": [dict(m) for m in milestones],
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

@app.get("/item/{item_id}", response_class=HTMLResponse)
def item_detail(request: Request, item_id: str):
    r = role(request)
    con = db()
    item = con.execute("SELECT * FROM WorkItems WHERE ItemId = ?", (item_id,)).fetchone()
    if item is None:
        con.close()
        return HTMLResponse("<h3>Item not found</h3>", status_code=404)
    # D13: confidential visible to own unit + executives only
    if item["Confidential"] and r["kind"] != "Executive" and item["LeadUnitId"] != r["unit"]:
        con.close()
        return HTMLResponse(
            "<h3>Confidential item</h3><p>You do not have access to this item's details. "
            "It is counted in aggregate totals as 'Confidential'.</p>", status_code=403)
    history = con.execute(
        "SELECT * FROM StatusUpdates WHERE ItemId = ? ORDER BY PeriodEnd", (item_id,)).fetchall()
    milestones = con.execute(
        "SELECT * FROM Milestones WHERE ItemId = ? ORDER BY ForecastDate", (item_id,)).fetchall()
    decisions = con.execute(
        "SELECT * FROM Decisions WHERE SubjectId = ?", (item_id,)).fetchall()
    unit = con.execute("SELECT Name FROM Units WHERE UnitId = ?", (item["LeadUnitId"],)).fetchone()
    con.close()
    return templates.TemplateResponse(request, "item.html", {
        "request": request, "role": r,
        "item": dict(item), "unit_name": unit["Name"] if unit else item["LeadUnitId"],
        "history": [dict(h) for h in history],
        "milestones": [dict(m) for m in milestones],
        "decisions": [dict(d) for d in decisions],
    })

@app.get("/priority/{pid}", response_class=HTMLResponse)
def priority_detail(request: Request, pid: str):
    r = role(request)
    con = db()
    pri = con.execute("SELECT * FROM StrategicPriorities WHERE PriorityId = ?", (pid,)).fetchone()
    items = con.execute(
        "SELECT * FROM WorkItems WHERE PrimaryPriorityId = ?", (pid,)).fetchall()
    # D13 for unit role
    if r["kind"] == "Unit":
        items = [i for i in items if not i["Confidential"] or i["LeadUnitId"] == r["unit"]]
    masked = con.execute(
        "SELECT COALESCE(SUM(CCCount),0) AS n FROM ConfidentialCounts WHERE CCPriorityId = ?",
        (pid,)).fetchone()["n"]
    kpis = con.execute("SELECT * FROM KPIs WHERE KpiPriorityId = ?", (pid,)).fetchall()
    su = latest_status(con, [i["ItemId"] for i in items])
    con.close()
    return templates.TemplateResponse(request, "priority.html", {
        "request": request, "role": r,
        "priority": dict(pri), "kpis": [dict(k) for k in kpis],
        "items": [dict(i) for i in items],
        "statuses": {k: dict(v) for k, v in su.items()},
        "masked": masked,
    })