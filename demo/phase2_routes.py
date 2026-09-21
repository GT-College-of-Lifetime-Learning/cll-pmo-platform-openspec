# CLL-SPM Phase 2 routes: allocations, capacity heatmap, roadmap, sync, drafts.
# Registered on the shared app by app.py.

import sqlite3
from datetime import date, datetime
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from demo.app import templates


def role(request):
    """Demo persona from ?as= (same convention as app.py; duplicated to avoid a
    circular import at app-init time)."""
    as_param = request.query_params.get("as", "executive")
    if as_param.startswith("unit:"):
        return {"kind": "Unit", "unit": as_param.split(":", 1)[1]}
    return {"kind": "Executive", "unit": None}

DEMO = Path(__file__).resolve().parent
DB = DEMO / "cll_spm.db"
TODAY = date(2026, 9, 19)

PERIODS = ["2026-07-31", "2026-08-31", "2026-09-30"]


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def register_phase2_routes(app: FastAPI):

    # ---------- Allocation entry (unit head) ----------

    @app.get("/allocate/{unit_id}", response_class=HTMLResponse)
    def allocation_form(request: Request, unit_id: str):
        con = db()
        import demo.capacity as capacity
        items = [dict(r) for r in con.execute(
            "SELECT ItemId, Title, Tier FROM WorkItems WHERE LeadUnitId=?"
            " AND Stage IN ('Active','On Hold') ORDER BY ItemId", (unit_id,)).fetchall()]
        existing = [dict(r) for r in con.execute(
            "SELECT * FROM Allocations WHERE UnitId=? AND Period=?",
            (unit_id, PERIODS[-1])).fetchall()]
        cap = con.execute("SELECT AvailableFte FROM UnitCapacity WHERE UnitId=? AND Period=?",
                          (unit_id, PERIODS[-1])).fetchone()
        unit = con.execute("SELECT * FROM Units WHERE UnitId=?", (unit_id,)).fetchone()
        con.close()
        committed = sum(a["Percent"] for a in existing) / 100.0
        return templates.TemplateResponse(request, "allocate.html", {
            "request": request, "role": role(request),
            "unit": dict(unit) if unit else {"UnitId": unit_id, "Name": unit_id},
            "items": items, "existing": existing,
            "period": PERIODS[-1],
            "available": cap["AvailableFte"] if cap else None,
            "committed": round(committed, 2),
            "granularity": capacity.GRANULARITY,
            "over": committed > ((cap["AvailableFte"] if cap else 99) or 99),
        })

    @app.post("/allocate/{unit_id}/submit")
    def allocation_submit(request: Request, unit_id: str,
                          item_id: str = Form(...),
                          target: str = Form(...),
                          percent: float = Form(...),
                          granularity: str = Form("role")):
        con = db()
        import demo.capacity as capacity
        try:
            capacity.enforce_granularity(granularity)
        except PermissionError as e:
            con.close()
            return HTMLResponse(f"<h3>Rejected</h3><p>{e}</p>", status_code=403)
        # visible, never prevented: store + warn if over capacity
        con.execute(
            "INSERT INTO Allocations (Period, ItemId, UnitId, Granularity, Target,"
            " Percent, AllocatedBy, AllocatedOn) VALUES (?,?,?,?,?,?,?,?)",
            (PERIODS[-1], item_id, unit_id, granularity, target, percent,
             "unit head", TODAY.isoformat()))
        cap = con.execute("SELECT AvailableFte FROM UnitCapacity WHERE UnitId=? AND Period=?",
                          (unit_id, PERIODS[-1])).fetchone()
        committed = (con.execute("SELECT COALESCE(SUM(Percent),0) FROM Allocations"
                                 " WHERE UnitId=? AND Period=?",
                                 (unit_id, PERIODS[-1])).fetchone()[0]) / 100.0
        available = (cap["AvailableFte"] if cap else None) or 0.0
        over = committed > available
        con.commit()
        con.close()
        suffix = ("?over=1" if over else "")
        return RedirectResponse(f"/allocate/{unit_id}?as={request.query_params.get('as','executive')}{suffix}",
                                status_code=303)

    # ---------- Capacity heatmap ----------

    @app.get("/capacity", response_class=HTMLResponse)
    def capacity_page(request: Request):
        con = db()
        import demo.capacity as capacity
        units = [dict(r) for r in con.execute(
            "SELECT * FROM Units WHERE UnitActive=1 ORDER BY UnitId").fetchall()]
        grid = {}
        for u in units:
            for p in PERIODS:
                committed, available, state, stale = capacity.utilization(con, u["UnitId"], p)
                grid[(u["UnitId"], p)] = {
                    "committed": round(committed, 2), "available": available,
                    "state": state, "stale": stale,
                    "pct": round(100 * committed / available, 0) if available else 0,
                }
        cross = capacity.cross_unit_overallocations(con, PERIODS[-1])
        # dean summary: over-allocated units this period
        over_units = [u for u in units
                      if grid[(u["UnitId"], PERIODS[-1])]["state"] == "over-allocated"]
        con.close()
        return templates.TemplateResponse(request, "capacity.html", {
            "request": request, "role": role(request),
            "units": units, "periods": PERIODS, "grid": grid,
            "cross": cross, "over_units": over_units,
        })

    # ---------- Roadmap view ----------

    @app.get("/roadmap", response_class=HTMLResponse)
    def roadmap_page(request: Request):
        con = db()
        rows = [dict(r) for r in con.execute(
            """SELECT ItemId, Level, Title, Stage, StartDate, TargetEndDate,
                      LeadUnitId, SyncEnabled
               FROM WorkItems WHERE Stage NOT IN ('Closed','Cancelled')
               AND Level IN ('Program','Project') ORDER BY StartDate""").fetchall()]
        con.close()
        return templates.TemplateResponse(request, "roadmap.html", {
            "request": request, "role": role(request), "items": rows,
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

    # ---------- Sync admin ----------

    @app.post("/admin/sync")
    def sync_run(request: Request):
        con = db()
        import demo.sync_engine as sync_engine
        import demo.findings as findings
        results = sync_engine.run_sync(con)
        # sync-failed findings feed the tracker (2/3/4 ladder applies)
        for item_id, status in results:
            if status == "failed":
                unit = con.execute("SELECT LeadUnitId FROM WorkItems WHERE ItemId=?",
                                   (item_id,)).fetchone()
                findings.record_finding(con, "sync-failed", "HIGH",
                                        unit["LeadUnitId"] if unit else None, item_id)
        con.commit()
        con.close()
        from fastapi.templating import Jinja2Templates
        return templates.TemplateResponse(request, "sync_result.html", {
            "request": request, "role": role(request), "results": results,
        })


def item_sync_context(con, item_id):
    """Shared context for item detail: sync state + schedule risk (task 2.3)."""
    import demo.sync_engine as sync_engine
    row = con.execute("SELECT * FROM WorkItems WHERE ItemId=?", (item_id,)).fetchone()
    if row is None or not row["SyncEnabled"]:
        return {}
    return {
        "sync_state": sync_engine.sync_state(row),
        "last_sync": row["LastSyncOn"],
        "plan_url": row["PlanUrl"],
        "schedule_risk": sync_engine.schedule_risk(con, item_id),
        "sync_enabled": True,
    }