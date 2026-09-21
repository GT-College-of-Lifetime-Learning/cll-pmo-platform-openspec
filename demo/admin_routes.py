# CLL-SPM admin/development panel — all operational and dev actions in one place
# (moved out of the site header). Registered on the shared app by app.py.

import json
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from demo.app import templates

ROOT = Path(__file__).resolve().parent.parent
DEMO = Path(__file__).resolve().parent
DB = DEMO / "cll_spm.db"
PY = sys.executable


def _role(request: Request):
    as_param = request.query_params.get("as", "executive")
    if as_param.startswith("unit:"):
        return {"kind": "Unit", "unit": as_param.split(":", 1)[1]}
    return {"kind": "Executive", "unit": None}


def _counts(con):
    out = {}
    for t in ("WorkItems", "StatusUpdates", "IntakeRequests", "KpiValues",
              "Findings", "Allocations", "DataNeeds"):
        out[t] = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    out["Findings (open)"] = con.execute(
        "SELECT COUNT(*) FROM Findings WHERE Status='Open'").fetchone()[0]
    return out


def register_admin_routes(app: FastAPI):

    @app.get("/admin", response_class=HTMLResponse)
    def admin_panel(request: Request):
        con = sqlite3.connect(DB)
        con.row_factory = sqlite3.Row
        counts = _counts(con)
        con.close()

        import demo.readiness as readiness
        gates, has_blocking, has_warn = readiness.evaluate()

        manifest = None
        mpath = DEMO / "output" / "feed" / "manifest.json"
        if mpath.exists():
            try:
                manifest = json.loads(mpath.read_text(encoding="utf-8"))
            except ValueError:
                manifest = None

        return templates.TemplateResponse(request, "admin.html", {
            "request": request, "role": _role(request),
            "counts": counts, "gates": gates,
            "has_blocking": has_blocking, "has_warn": has_warn,
            "manifest": manifest,
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

    @app.post("/admin/export-feed")
    def admin_export_feed(request: Request):
        from demo.export_feed import export_feed
        manifest = export_feed()
        lines = [f"{name}: {rows} rows" for name, rows in manifest["files"].items()]
        lines.append(f"feed_version {manifest['feed_version']} · generated {manifest['generated_at']}")
        return templates.TemplateResponse(request, "admin_done.html", {
            "request": request, "role": _role(request),
            "title": "Data feed exported",
            "lines": lines,
            "back": "/admin",
        })

    @app.post("/admin/matrix")
    def admin_matrix(request: Request):
        r = subprocess.run([PY, str(DEMO / "generate_matrix.py")],
                           cwd=ROOT, capture_output=True, text=True)
        ok = r.returncode == 0
        lines = (r.stdout + r.stderr).strip().splitlines() or ["(no output)"]
        if not ok:
            lines.append("generation FAILED")
        return templates.TemplateResponse(request, "admin_done.html", {
            "request": request, "role": _role(request),
            "title": "Data-source matrix regenerated" if ok else "Matrix regeneration failed",
            "lines": lines, "back": "/admin",
        })

    @app.post("/admin/rebuild")
    def admin_rebuild(request: Request):
        r = subprocess.run([PY, str(DEMO / "build_db.py")],
                           cwd=ROOT, capture_output=True, text=True)
        ok = r.returncode == 0
        lines = (r.stdout + r.stderr).strip().splitlines() or ["(no output)"]
        if not ok:
            lines.append("rebuild FAILED")
        else:
            lines.append("demo database rebuilt from the deterministic seeds")
        return templates.TemplateResponse(request, "admin_done.html", {
            "request": request, "role": _role(request),
            "title": "Demo database rebuilt" if ok else "Rebuild failed",
            "lines": lines, "back": "/admin",
        })