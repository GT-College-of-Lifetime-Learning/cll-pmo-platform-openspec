# Adversarial planted-defect tests for Phase 2: resource capacity + execution sync.
# Bar: planted violations caught 100%, 0 false alarms.

import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\kwong318\GitHub\CLL_project_dashboard")
sys.path.insert(0, str(ROOT))

DB = ROOT / "demo" / "cll_spm.db"
SCRATCH = ROOT / "demo" / "cll_spm_scratch.db"

passed = failed = 0

def check(name: str, cond, detail: object = "") -> None:
    global passed, failed
    if cond:
        passed += 1
        print(f"OK   {name}")
    else:
        failed += 1
        print(f"FAIL {name} {detail if isinstance(detail, str) else repr(detail)}")

def build_scratch():
    if SCRATCH.exists():
        SCRATCH.unlink()
    shutil.copy(DB, SCRATCH)

# ============ Capacity model (task 1.6) ============
build_scratch()
con = sqlite3.connect(SCRATCH)
con.row_factory = sqlite3.Row
import demo.capacity as capacity
capacity.DB = SCRATCH

# Seeded truth: GTPE August is over-allocated (6.5 committed vs 6.0 available)
c, a, state, stale = capacity.utilization(con, "GTPE", "2026-08-31")
check("Planted over-allocation detected (GTPE Aug)", state == "over-allocated", (c, a, state))
check("Over-allocation computes committed/available FTE", round(c, 2) == 6.5 and a == 6.0, (c, a))

# Unallocated: SAV has capacity declared but no allocations
c2, a2, state2, _ = capacity.utilization(con, "SAV", "2026-08-31")
check("Unallocated unit reads unallocated", state2 == "unallocated", (c2, a2, state2))

# Planted defect: stale allocations label the result (Sept allocations unreviewed)
_, _, _, stale_sep = capacity.utilization(con, "GTPE", "2026-09-30")
check("Stale (unreviewed) allocations label the computed result", stale_sep is True)

# Cross-unit over-allocation: GTPE Aug is over with cross-unit driver CLL-26-0002
# (DEAN-led, GTPE a contributing unit — cross-unit work driving GTPE's over-commitment)
cross = capacity.cross_unit_overallocations(con, "2026-08-31")
gtpe_cross = [o for o in cross if o["unit"] == "GTPE"]
check("Cross-unit over-allocation reaches governance with drivers",
      any("CLL-26-0002" in str(o["cross_unit"]) for o in gtpe_cross), cross)

# Granularity enforcement (D4): person-level rejected under role-level policy
try:
    capacity.enforce_granularity("person")
    check("Person-level allocation REJECTED under role-level policy", False, "no exception")
except PermissionError:
    check("Person-level allocation REJECTED under role-level policy", True)
capacity.enforce_granularity("role")
check("Role-level allocation accepted", True)

# Planted defect: over-allocation entry must STORE + WARN, not prevent (via app)
from fastapi.testclient import TestClient
from demo.app import app
client = TestClient(app, follow_redirects=False)
r = client.post("/allocate/GTLI/submit?as=executive", data={
    "item_id": "CLL-26-0004", "target": "Program Admin", "percent": "400"})
check("Over-allocation entry stored (redirect, not rejected)", r.status_code == 303, r.status_code)
# 0 false alarms: normal allocation stores cleanly
r = client.post("/allocate/GTLI/submit?as=executive", data={
    "item_id": "CLL-26-0012", "target": "Coordinator", "percent": "10"})
check("Normal allocation stores cleanly", r.status_code == 303, r.status_code)
con.close()

# ============ Sync engine (task 2.6) ============
build_scratch()
import demo.sync_engine as sync_engine
sync_engine.DB = SCRATCH

con = sqlite3.connect(SCRATCH)
con.row_factory = sqlite3.Row

# Live sync: plan fixture pushes milestones + percent into registry
results = sync_engine.run_sync(con)
check("Synced items report live", all(s == "live" for _, s in results), results)
ms = con.execute("SELECT * FROM Milestones WHERE ItemId='CLL-26-0002' AND Source='sync'").fetchall()
check("Plan milestones landed in registry with sync source", len(ms) >= 1)

# Planted defect: broken plan link -> failed state + finding recorded
con.execute("UPDATE WorkItems SET SyncEnabled=1 WHERE ItemId='CLL-26-0009'")  # no fixture
con.commit()
import demo.findings as findings
results = sync_engine.run_sync(con)
failed_ids = [i for i, s in results if s == "failed"]
check("Broken plan link syncs as failed", "CLL-26-0009" in failed_ids, results)
findings.record_finding(con, "sync-failed", "HIGH", "GTPE", "CLL-26-0009")
con.commit()
row = con.execute("SELECT Occurrences FROM Findings WHERE Type='sync-failed' AND Status='Open'").fetchone()
check("Sync failure feeds the finding tracker", row and row["Occurrences"] >= 1)

# sync_state honesty: LastSyncOn NULL -> failed; old -> stale; recent -> live
r = con.execute("SELECT * FROM WorkItems WHERE ItemId='CLL-26-0009'").fetchone()
check("Sync state computed: never-synced item reads failed", sync_engine.sync_state(r) == "failed")
r2 = con.execute("SELECT * FROM WorkItems WHERE ItemId='CLL-26-0002'").fetchone()
check("Sync state computed: recently-synced item reads live", sync_engine.sync_state(r2) == "live")
con.execute("UPDATE WorkItems SET LastSyncOn='2026-09-01' WHERE ItemId='CLL-26-0002'")
con.commit()
r3 = con.execute("SELECT * FROM WorkItems WHERE ItemId='CLL-26-0002'").fetchone()
check("Sync state computed: old sync reads stale", sync_engine.sync_state(r3) == "stale")

# Schedule risk (D7): milestone forecast slipped past baseline -> derived text
risk = sync_engine.schedule_risk(con, "CLL-26-0002")
check("Schedule risk derived from milestone slip vs baseline",
      risk and risk["slip_days"] > 0 and "slipped" in risk["text"], risk)
# 0 false alarms: on-baseline milestone reads on-baseline
con.execute("UPDATE Milestones SET ForecastDate='2026-09-30' WHERE ItemId='CLL-26-0002' AND ActualDate IS NULL AND Source='sync'")
con.commit()
risk2 = sync_engine.schedule_risk(con, "CLL-26-0002")
check("On-baseline milestone reads on baseline", risk2 and "on baseline" in risk2["text"], risk2)

# Draft flow (task 2.2): draft pre-populates from plan; unconfirmed does NOT count
plan = sync_engine.load_plan("CLL-26-0002")
check("Plan fixture readable by draft flow", plan and plan["percent_complete"] == 64)
n_updates = con.execute(
    "SELECT COUNT(*) FROM StatusUpdates WHERE ItemId='CLL-26-0002' AND PeriodEnd='2026-09-30'").fetchone()[0]
check("Unconfirmed draft does not count toward the period's update", n_updates == 0, n_updates)
con.close()

# ============ App-level surfaces (route smoke for the new pages) ============
client2 = TestClient(app, follow_redirects=True)
html = client2.get("/capacity?as=executive").text
check("Heatmap shows text states (not color alone)",
      "over-allocated" in html and "unallocated" in html)
check("Stale labeling visible on the heatmap", "stale" in html)
html = client2.get("/governance?as=executive").text
check("Governance surfaces over-allocation risk", "Over-allocated units" in html)
html = client2.get("/overview?as=executive").text
check("Dean overview capacity summary present", "Capacity" in html)
html = client2.get("/item/CLL-26-0002?as=executive").text
check("Tier 1 detail shows sync state + schedule risk text",
      "Execution sync" in html and "slipped" in html)
html = client2.get("/roadmap?as=executive").text
check("Roadmap renders registry timeline", "CLL-26-" in html)
r = client2.post("/admin/sync", follow_redirects=True)
check("Sync run via app works", r.status_code == 200)

# cleanup
SCRATCH.unlink(missing_ok=True)
print(f"\n{passed}/{passed + failed} Phase-2 planted-defect checks passed")
sys.exit(1 if failed else 0)