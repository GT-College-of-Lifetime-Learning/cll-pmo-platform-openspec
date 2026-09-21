# CLL-SPM capacity model (Phase 2, design D4/D5).
# Committed = sum of allocations per unit-period; Available = the unit's declared
# capacity; Utilization states: unallocated (<10%), allocated, at capacity (90-100%),
# over-allocated (>100%). Text labels everywhere; stale allocations label the result.

import sqlite3
from datetime import date
from pathlib import Path

DEMO = Path(__file__).resolve().parent
DB = DEMO / "cll_spm.db"
TODAY = date(2026, 9, 19)

# Granularity policy flag (Dean Q2). Role-level is the enforced default until
# the Dean answers; enforced at the QUERY layer, not just hidden in the UI.
GRANULARITY = "role"

STATES = ("unallocated", "allocated", "at capacity", "over-allocated")


def utilization(con, unit, period):
    """(committed_fte, available_fte, state, stale, driving_items) for a unit-period."""
    committed_pct = con.execute(
        "SELECT COALESCE(SUM(Percent),0) FROM Allocations WHERE UnitId=? AND Period=?",
        (unit, period)).fetchone()[0]
    avail_row = con.execute(
        "SELECT AvailableFte FROM UnitCapacity WHERE UnitId=? AND Period=?",
        (unit, period)).fetchone()
    available = (avail_row[0] if avail_row else None) or 0.0
    committed = committed_pct / 100.0

    # stale: any allocation in this unit-period not reviewed within its cycle
    stale_row = con.execute(
        "SELECT COUNT(*) FROM Allocations WHERE UnitId=? AND Period=?"
        " AND (ReviewedOn IS NULL OR ReviewedOn < ?)",
        (unit, period, period)).fetchone()[0]
    stale = stale_row > 0

    if committed < 0.1:
        state = "unallocated"
    elif committed > available + 0.001:
        state = "over-allocated"
    elif committed >= available * 0.9:
        state = "at capacity"
    else:
        state = "allocated"
    return committed, available, state, stale


def driving_items(con, unit, period):
    return [dict(r) for r in con.execute(
        """SELECT a.ItemId, a.Target, a.Percent, w.Title, w.ContributingUnitIds
           FROM Allocations a JOIN WorkItems w ON w.ItemId = a.ItemId
           WHERE a.UnitId=? AND a.Period=?
           ORDER BY a.Percent DESC""", (unit, period)).fetchall()]


def cross_unit_overallocations(con, period):
    """Over-allocated unit-periods whose driving items include cross-unit work
    (governance surfaces these — college risk, not just unit risk)."""
    out = []
    for row in con.execute("SELECT DISTINCT UnitId FROM UnitCapacity WHERE Period=?",
                           (period,)).fetchall():
        unit = row["UnitId"]
        committed, available, state, stale = utilization(con, unit, period)
        if state == "over-allocated":
            items = driving_items(con, unit, period)
            # cross-unit driver: the item involves more than this unit — the unit
            # is a contributing unit (led elsewhere) OR the item declares
            # contributing units beyond its lead
            def is_cross(i):
                if not i["ContributingUnitIds"]:
                    return False
                others = [u.strip() for u in i["ContributingUnitIds"].split(",") if u.strip()]
                return len(others) >= 1 and unit in others
            cross = [i for i in items if is_cross(i)]
            out.append({"unit": unit, "committed": round(committed, 2),
                        "available": available, "driving": items,
                        "cross_unit": cross})
    return out


def enforce_granularity(target_kind):
    """D4: role-level selected => person-addressable allocation is rejected
    at the query layer. target_kind: 'role' | 'person'."""
    if target_kind == "person" and GRANULARITY == "role":
        raise PermissionError(
            "allocation granularity is role-level (Dean Q2 pending); "
            "person-level allocation is not addressable")
    return True