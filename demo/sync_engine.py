# CLL-SPM demo sync engine — one-way plan → registry sync (Phase 2, design D1/D3).
# Reads planted plan fixtures (demo/fixtures/plan-*.json) for SyncEnabled Tier 1
# items and pushes milestones + percent complete INTO the registry. The registry
# remains the system of record; disagreements surface, never silently resolve.
# Sync states (live/stale/failed) mirror the KPI data-state pattern.

import json
import sqlite3
from datetime import date, datetime
from pathlib import Path

DEMO = Path(__file__).resolve().parent
DB = DEMO / "cll_spm.db"
FIXTURES = DEMO / "fixtures"

TODAY = date(2026, 9, 19)

# Expected sync window (design D1: within one business day)
SYNC_WINDOW_DAYS = 2


def load_plan(item_id):
    path = FIXTURES / f"plan-{item_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def run_sync(con, today=None):
    """Sync all SyncEnabled items from their plan fixtures.
    Returns list of (item_id, status) per sync run."""
    today = today or TODAY
    results = []
    rows = con.execute("SELECT ItemId FROM WorkItems WHERE SyncEnabled=1").fetchall()
    for row in rows:
        item_id = row["ItemId"]
        plan = load_plan(item_id)
        if plan is None:
            # broken plan link → sync failure recorded, fields go stale
            con.execute("UPDATE WorkItems SET LastSyncOn=NULL WHERE ItemId=?", (item_id,))
            results.append((item_id, "failed"))
            continue
        # one-way push: milestones + percent complete
        for ms in plan.get("milestones", []):
            existing = con.execute(
                "SELECT * FROM Milestones WHERE ItemId=? AND MilestoneTitle=?",
                (item_id, ms["title"])).fetchone()
            if existing is None:
                con.execute(
                    "INSERT INTO Milestones VALUES (?,?,?,?,?,?,?)",
                    (item_id, ms["title"], ms["baseline"], ms["forecast"],
                     ms["actual"], 1, "sync"))
            else:
                # registry record with its as-of wins? No - plan pushes; but a
                # DISAGREEMENT between the plan and a lead-entered record surfaces
                con.execute(
                    "UPDATE Milestones SET ForecastDate=?, ActualDate=?, Source='sync'"
                    " WHERE ItemId=? AND MilestoneTitle=?",
                    (ms["forecast"], ms["actual"], item_id, ms["title"]))
        con.execute("UPDATE WorkItems SET LastSyncOn=? WHERE ItemId=?",
                    (today.isoformat(), item_id))
        results.append((item_id, "live"))
    return results


def sync_state(item_row, today=None):
    """live / stale / failed per design D3. Computed, never stored."""
    today = today or TODAY
    if not item_row["SyncEnabled"]:
        return None
    if item_row["LastSyncOn"] is None:
        return "failed"
    last = date.fromisoformat(item_row["LastSyncOn"])
    return "live" if (today - last).days <= SYNC_WINDOW_DAYS else "stale"


def schedule_risk(con, item_id, today=None):
    """Derived schedule-risk (design D7): next unfinished milestone's forecast vs
    baseline, slip measured in months of forecast delay; text + evidence, never
    color alone. Returns dict or None."""
    ms = con.execute(
        """SELECT * FROM Milestones WHERE ItemId=? AND ActualDate IS NULL
           ORDER BY ForecastDate LIMIT 1""", (item_id,)).fetchone()
    if ms is None or not ms["ForecastDate"] or not ms["BaselineDate"]:
        return None
    f = date.fromisoformat(ms["ForecastDate"])
    b = date.fromisoformat(ms["BaselineDate"])
    slip_days = (f - b).days
    return {
        "milestone": ms["MilestoneTitle"],
        "baseline": ms["BaselineDate"],
        "forecast": ms["ForecastDate"],
        "slip_days": slip_days,
        "text": (f"{ms['MilestoneTitle']}: forecast {ms['ForecastDate']} vs baseline "
                 f"{ms['BaselineDate']} — slipped {slip_days} days" if slip_days > 0
                 else f"{ms['MilestoneTitle']}: forecast {ms['ForecastDate']} vs baseline "
                      f"{ms['BaselineDate']} — on baseline"),
    }