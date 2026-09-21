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

from demo.flows import register_flow_routes  # noqa: E402
register_flow_routes(app)

from demo.phase2_routes import register_phase2_routes  # noqa: E402
register_phase2_routes(app)

from demo.admin_routes import register_admin_routes  # noqa: E402
register_admin_routes(app)

# Trust banner (cycle-readiness spec): every page shows the readiness summary.
# Computed per render via a Jinja global so no route has to thread it through.
import demo.readiness as _readiness  # noqa: E402

def _trust_summary():
    try:
        _, has_blocking, has_warn = _readiness.evaluate()
        if has_blocking:
            return "degraded"
        if has_warn:
            return "warn"
        return "ok"
    except Exception:
        return "unknown"

templates.env.globals["trust_state"] = _trust_summary

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

# ---------- Strategy 2035 (add-strategy-2035-success-dashboard) ----------

WINDOW_START = date(2026, 1, 1)
WINDOW_END = date(2035, 12, 31)

def _business_days_between(con, start, end):
    row = con.execute(
        "SELECT COUNT(*) FROM BusinessDays WHERE IsBusinessDay=1 AND Date >= ? AND Date <= ?",
        (start.isoformat(), end.isoformat())).fetchone()
    return row[0] if row else None

@app.get("/strategy", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
def strategy_2035(request: Request):
    r = role(request)
    con = db()
    as_of = TODAY  # demo as-of date; in production = last successful refresh

    # --- Timeline (design D2; hand-check scenario: 2026-08-16 -> 6.2% / 3,425) ---
    elapsed_days = (as_of - WINDOW_START).days
    total_days = (WINDOW_END - WINDOW_START).days + 1  # 3,652
    days_remaining = (WINDOW_END - as_of).days + 1
    elapsed_pct = round(100 * elapsed_days / total_days, 1)
    bd_remaining = _business_days_between(con, as_of, WINDOW_END)

    # --- Goals, cards, pace (D3/D4), data states (D7) ---
    priorities = con.execute(
        "SELECT * FROM StrategicPriorities ORDER BY PriorityId").fetchall()
    goals = []
    live_count = 0
    for p in priorities:
        pid = p["PriorityId"]
        headline = con.execute(
            "SELECT * FROM KPIs WHERE KpiPriorityId=? AND DashboardRole='Headline'", (pid,)).fetchone()
        secondary = con.execute(
            "SELECT * FROM KPIs WHERE KpiPriorityId=? AND DashboardRole='Secondary'", (pid,)).fetchone()

        g = {
            "no": pid[-1], "pid": pid, "short_name": p["ShortName"] or p["Title"],
            "color": p["DisplayColor"] or "#B3A369", "state": "Pending source",
            "headline_value": None, "headline_target": None, "uom": "", "pct": 0,
            "pct_f": 0, "pace": "Not yet measurable",
            "pace_label": "Linear pace (unapproved)", "owner": None,
            "secondary": None, "recent": [], "aligned_work": None, "index": None,
            "caps": 0, "ladder": [], "vis": "trend", "as_of": None, "pct_note": None,
            "pending_why": None,
        }

        def kpi_state(k):
            if k is None:
                return "Pending definition", None
            row = con.execute(
                "SELECT Value, PeriodEnd, SubmittedBy, ValueNote, DataSource FROM KpiValues"
                " WHERE KpiValueId=? ORDER BY PeriodEnd DESC LIMIT 1",
                (k["KpiId"],)).fetchone()
            if row is None:
                return ("Pending source" if k["KpiOwner"] else "Pending definition"), None
            freq_days = {"Monthly": 31, "Quarterly": 92, "Semiannual": 183, "Annual": 366}.get(k["Frequency"], 92)
            days_since = (as_of - date.fromisoformat(row["PeriodEnd"])).days
            st = "Stale" if days_since > 2 * freq_days else "Live"
            return st, row

        if headline is not None:
            st, row = kpi_state(headline)
            g["state"] = st
            g["owner"] = headline["KpiOwner"]
            g["uom"] = headline["UnitOfMeasure"] or ""
            if row is not None:
                g["headline_value"] = int(row["Value"]) if row["Value"] == int(row["Value"]) else row["Value"]
                g["headline_target"] = int(headline["Target"]) if headline["Target"] and headline["Target"] == int(headline["Target"]) else headline["Target"]
                g["as_of"] = row["PeriodEnd"]
                # provenance (strategy-kpi-data spec): source, as-of, submitter visible
                g["source_note"] = (row["ValueNote"] or "").strip() or headline["Method"] or "KPI owner submission"
                g["submitter"] = row["SubmittedBy"]
                # origin tag (data-sourcing spec): fabricated never masquerades as real
                ds = row["DataSource"] or "demo-seed"
                g["origin"] = "fabricated demo data" if ds == "demo-seed" else ds
                if headline["Target"]:
                    g["pct"] = min(round(100 * row["Value"] / headline["Target"], 1), 100)
                    g["pct_f"] = g["pct"]
                # pace (D3): expected-today = linear interpolation on basis
                basis = headline["Basis"] or "Cumulative"
                start = date.fromisoformat(headline["CountingStart"]) if headline["CountingStart"] else WINDOW_START
                end = date.fromisoformat(headline["TargetDate"]) if headline["TargetDate"] else WINDOW_END
                if basis == "PointInTime":
                    expected = headline["Target"]
                elif basis == "Index":
                    expected = None  # first assessment anchors; show Not yet measurable
                else:
                    frac = min(max((as_of - start).days / max((end - start).days, 1), 0), 1)
                    expected = (headline["Baseline"] or 0) + ((headline["Target"] or 0) - (headline["Baseline"] or 0)) * frac
                if st == "Live" and expected:
                    ratio = row["Value"] / expected if expected else 1
                    g["pace"] = ("On pace" if ratio >= 0.95 else
                                 "Behind" if ratio >= 0.80 else "Well behind")
                # approved trajectory?
                appr = con.execute(
                    "SELECT COUNT(*) FROM KpiTrajectories WHERE KpiId=? AND Approved=1",
                    (headline["KpiId"],)).fetchone()[0]
                if appr:
                    g["pace_label"] = "Approved trajectory"
                if st == "Live":
                    live_count += 1
            elif st == "Pending definition":
                g["pending_why"] = "definition of the counting rule pending (see open questions)"

        if secondary is not None:
            st2, row2 = kpi_state(secondary)
            g["secondary"] = {
                "name": secondary["KpiName"], "state": st2,
                "value": row2["Value"] if row2 else None,
                "target": secondary["Target"],
            }

        # signature visuals per goal
        g["vis"] = {"1": "ring", "2": "map", "3": "trend", "4": "gauge", "5": "maturity"}.get(g["no"], "trend")
        if g["no"] == "5":
            idx_row = con.execute(
                "SELECT AVG(Level) AS idx, COUNT(*) AS n FROM Capabilities WHERE InScope=1").fetchone()
            g["index"] = round(idx_row["idx"], 1) if idx_row["idx"] else None
            g["caps"] = idx_row["n"]
            dist = con.execute(
                "SELECT Level, COUNT(*) AS n FROM Capabilities WHERE InScope=1 GROUP BY Level").fetchall()
            by_lvl = {d["Level"]: d["n"] for d in dist}
            top = max(by_lvl.values()) if by_lvl else 1
            g["ladder"] = [
                {"label": f"L{lvl}", "on": by_lvl.get(lvl, 0) == top} for lvl in (1, 2, 3, 4, 5)
            ] if by_lvl else []
            # capability heatmap: areas x levels (task 3.3)
            areas = con.execute(
                """SELECT Area, SUM(CASE WHEN Level=1 THEN 1 ELSE 0 END) AS l1,
                          SUM(CASE WHEN Level=2 THEN 1 ELSE 0 END) AS l2,
                          SUM(CASE WHEN Level=3 THEN 1 ELSE 0 END) AS l3,
                          SUM(CASE WHEN Level=4 THEN 1 ELSE 0 END) AS l4,
                          SUM(CASE WHEN Level=5 THEN 1 ELSE 0 END) AS l5
                   FROM Capabilities WHERE InScope=1 GROUP BY Area ORDER BY Area""").fetchall()
            g["heatmap"] = [{"area": a["Area"], "cells": [a["l1"], a["l2"], a["l3"], a["l4"], a["l5"]]}
                            for a in areas]

        # trend series for the headline KPI (task 3.3: term/credential/expenditure trends)
        if headline is not None:
            series = con.execute(
                "SELECT PeriodEnd, Value FROM KpiValues WHERE KpiValueId=? ORDER BY PeriodEnd",
                (headline["KpiId"],)).fetchall()
            maxv = max((s["Value"] for s in series), default=0) or 1
            g["trend"] = [{"label": s["PeriodEnd"][:7], "value": s["Value"],
                           "h": max(2, int(36 * s["Value"] / maxv))} for s in series]
            # hub timeline (goal 2): hub openings by year from activity
            if g["no"] == "2":
                hubs = con.execute(
                    """SELECT substr(ActDate,1,4) AS yr, COUNT(*) AS n, SUM(ActValue) AS v
                       FROM StrategyActivity WHERE ActPriorityId=? AND Type IN ('HubOpening','StartupAdopted')
                       GROUP BY yr ORDER BY yr""", (pid,)).fetchall()
                g["hub_timeline"] = [{"yr": h["yr"], "n": h["v"] or h["n"]} for h in hubs]
        # expenditure gauge (goal 4): latest FY value vs $20M target
        if g["no"] == "4":
            fy = con.execute(
                "SELECT Value, PeriodEnd FROM KpiValues WHERE KpiValueId='KPI-010' ORDER BY PeriodEnd DESC LIMIT 1").fetchone()
            if fy:
                g["gauge"] = {"value": fy["Value"], "target": 20000000,
                              "pct": min(round(100 * fy["Value"] / 20000000, 1), 100)}

        recent = con.execute(
            "SELECT * FROM StrategyActivity WHERE ActPriorityId=? ORDER BY ActDate DESC LIMIT 3",
            (pid,)).fetchall()
        g["recent"] = [{"date": a["ActDate"], "title": a["ActTitle"],
                        "value": int(a["ActValue"]) if a["ActValue"] and a["ActValue"] == int(a["ActValue"]) else a["ActValue"],
                        "uom": a["ActUoM"] or ""} for a in recent]

        goals.append(g)

    con.close()
    return templates.TemplateResponse(request, "strategy.html", {
        "request": request, "role": r, "goals": goals,
        "elapsed_pct": elapsed_pct, "remaining_pct": round(100 - elapsed_pct, 1),
        "days_remaining": days_remaining,
        "business_days_remaining": bd_remaining if bd_remaining is not None else "—",
        "elapsed_px": int(1000 * elapsed_pct / 100),
        "as_of": as_of.isoformat(),
        "live_count": live_count,
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

@app.get("/readiness", response_class=HTMLResponse)
def readiness_page(request: Request):
    import demo.readiness as readiness
    gates, has_blocking, has_warn = readiness.evaluate()
    return templates.TemplateResponse(request, "readiness.html", {
        "request": request, "role": role(request),
        "gates": gates, "has_blocking": has_blocking, "has_warn": has_warn,
    })

# ---------- Data feed (data-feed spec) ----------

@app.get("/api/feed")
def feed_manifest():
    """Feed manifest; refreshes the export then serves metadata. College-level
    aggregates by construction (design D4) — no item-level rows, so no role filter
    is needed beyond the app itself."""
    from demo.export_feed import export_feed
    import json as _json
    manifest = export_feed()
    return _json.loads((Path(__file__).resolve().parent / "output" / "feed" / "manifest.json").read_text(encoding="utf-8"))

@app.get("/api/feed/{name}")
def feed_file(name: str):
    """Serve one feed file by name (only known feed names)."""
    from fastapi.responses import FileResponse, PlainTextResponse
    allowed = {"kpis.csv", "rag-counts.csv", "currency.csv", "intake-aging.csv",
               "readiness.json", "findings.json", "coverage.json", "manifest.json"}
    if name not in allowed:
        return PlainTextResponse("unknown feed file", status_code=404)
    path = Path(__file__).resolve().parent / "output" / "feed" / name
    if not path.exists():
        return PlainTextResponse("feed not exported yet", status_code=503)
    return FileResponse(path)

@app.get("/coverage", response_class=HTMLResponse)
def coverage_page(request: Request):
    """data-sourcing spec: per-need sourced/partial/unsourced, grouped by
    consumer view, with UNDEFINED needs surfaced for sponsor routing."""
    con = db()
    needs = [dict(r) for r in con.execute(
        "SELECT * FROM DataNeeds ORDER BY ConsumerView, NeedId").fetchall()]
    unmatched = [dict(r) for r in con.execute(
        "SELECT * FROM SourceDeclarations WHERE MatchedNeedId IS NULL").fetchall()]
    con.close()

    def coverage_state(n):
        if n["SourceState"] == "HAVE":
            return "sourced"
        if n["SourceState"] == "PARTIAL":
            return "partial"
        return "unsourced"

    by_view = {}
    for n in needs:
        n["coverage"] = coverage_state(n)
        by_view.setdefault(n["ConsumerView"], []).append(n)
    view_summary = {v: {
        "sourced": sum(1 for n in rows if n["coverage"] == "sourced"),
        "partial": sum(1 for n in rows if n["coverage"] == "partial"),
        "unsourced": sum(1 for n in rows if n["coverage"] == "unsourced"),
    } for v, rows in by_view.items()}
    undefined = [n for n in needs if n["DefinitionState"].startswith("UNDEFINED")]

    return templates.TemplateResponse(request, "coverage.html", {
        "request": request, "role": role(request),
        "by_view": by_view, "view_summary": view_summary,
        "undefined": undefined, "unmatched": unmatched,
        "totals": {"sourced": sum(1 for n in needs if n["coverage"] == "sourced"),
                   "partial": sum(1 for n in needs if n["coverage"] == "partial"),
                   "unsourced": sum(1 for n in needs if n["coverage"] == "unsourced")},
    })

# ---------- Phase 1 views ----------

@app.get("/overview", response_class=HTMLResponse)
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

    # Phase 2: capacity summary for the overview (over-allocated units this period)
    import demo.capacity as _capacity
    _units = [u["UnitId"] for u in priorities and con.execute(
        "SELECT UnitId FROM Units WHERE UnitActive=1").fetchall()]
    over_allocated_units = []
    for u in _units:
        _c, _a, _s, _st = _capacity.utilization(con, u, "2026-09-30")
        if _s == "over-allocated":
            over_allocated_units.append(u)

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
        "over_allocated_units": over_allocated_units,
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

@app.get("/governance", response_class=HTMLResponse)
def governance(request: Request):
    con = db()
    reqs = con.execute(
        """SELECT r.*, (COALESCE(r.ScoreAlignment,0)*0.25 + COALESCE(r.ScoreValue,0)*0.25 +
               COALESCE(r.ScoreUrgency,0)*0.15 + COALESCE(r.ScoreCapacity,0)*0.15 +
               COALESCE(r.ScoreEffort,0)*0.10 + COALESCE(r.ScoreRisk,0)*0.10) AS ScoreTotal,
               CAST(JULIANDAY('2026-09-19') - JULIANDAY(r.SubmittedDate) AS INTEGER) AS age_days
           FROM IntakeRequests r
           WHERE r.Status NOT IN ('Approved','Declined')
           ORDER BY r.Status, ScoreTotal DESC""").fetchall()
    tier2 = con.execute(
        """SELECT r.* FROM IntakeRequests r WHERE r.Status='Approved' AND r.Tier='2'""").fetchall()
    decisions = con.execute(
        "SELECT * FROM Decisions ORDER BY DecisionDate DESC LIMIT 8").fetchall()
    # finding-tracker: governance sees findings escalated to 3+ occurrences
    from demo.findings import open_findings
    escalated_findings = [dict(f) for f in open_findings(con, min_occurrences=3)]
    # Phase 2: cross-unit over-allocations surface in governance (needs attention)
    import demo.capacity as capacity
    over_allocs = capacity.cross_unit_overallocations(con, "2026-09-30")
    con.close()
    return templates.TemplateResponse(request, "governance.html", {
        "request": request, "role": role(request),
        "requests": [dict(r) for r in reqs],
        "tier2": [dict(t) for t in tier2],
        "decisions": [dict(d) for d in decisions],
        "escalated_findings": escalated_findings,
        "over_allocs": over_allocs,
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

    # finding-tracker: recurring markers on this unit's items (2+ occurrences)
    from demo.findings import open_findings, escalation_level
    unit_findings = {f["AffectedItemId"]: f for f in open_findings(con, unit=eff_unit, min_occurrences=2)}
    con.close()
    return templates.TemplateResponse(request, "unit.html", {
        "request": request, "role": r, "unit": dict(unit) if unit else {"UnitId": unit_id, "Name": unit_id},
        "items": [dict(i) for i in items],
        "statuses": {k: dict(v) for k, v in su.items()},
        "action_needed": action_needed,
        "milestones": [dict(m) for m in milestones],
        "unit_findings": {k: dict(v) for k, v in unit_findings.items()},
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
    # Phase 2: sync state + schedule risk on Tier 1 detail (task 2.3)
    from demo.phase2_routes import item_sync_context
    sync_ctx = item_sync_context(con, item_id)
    # Phase 2: draft flow - synced item's period update arrives pre-populated (task 2.2)
    draft = None
    if sync_ctx.get("sync_enabled"):
        from demo.sync_engine import load_plan
        plan = load_plan(item_id)
        if plan:
            draft = {"percent_complete": plan.get("percent_complete"),
                     "source": "plan sync (last %s)" % sync_ctx.get("last_sync"),
                     "confirmed": bool(con.execute(
                         "SELECT COUNT(*) FROM StatusUpdates WHERE ItemId=? AND PeriodEnd='2026-09-30'",
                         (item_id,)).fetchone()[0])}
    con.close()
    return templates.TemplateResponse(request, "item.html", {
        "request": request, "role": r,
        "item": dict(item), "unit_name": unit["Name"] if unit else item["LeadUnitId"],
        "history": [dict(h) for h in history],
        "milestones": [dict(m) for m in milestones],
        "decisions": [dict(d) for d in decisions],
        "sync_ctx": sync_ctx, "draft": draft,
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
    kpis = [dict(k) for k in kpis]
    for k in kpis:
        row = con.execute(
            "SELECT Value, PeriodEnd, SubmittedBy, ValueNote FROM KpiValues WHERE KpiValueId=?"
            " ORDER BY PeriodEnd DESC LIMIT 1", (k["KpiId"],)).fetchone()
        if row:
            k["LatestValue"] = row["Value"]
            k["AsOf"] = row["PeriodEnd"]
            k["Submitter"] = row["SubmittedBy"]
            k["SourceNote"] = (row["ValueNote"] or "").strip() or k["Method"] or "KPI owner submission"
        else:
            k["LatestValue"] = None
            k["AsOf"] = None
            k["Submitter"] = None
            k["SourceNote"] = None
    su = latest_status(con, [i["ItemId"] for i in items])
    con.close()
    return templates.TemplateResponse(request, "priority.html", {
        "request": request, "role": r,
        "priority": dict(pri), "kpis": [dict(k) for k in kpis],
        "items": [dict(i) for i in items],
        "statuses": {k: dict(v) for k, v in su.items()},
        "masked": masked,
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })