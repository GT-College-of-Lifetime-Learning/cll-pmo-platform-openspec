# CLL-SPM source declaration loader.
# Captures steward declarations (sharepoint/seed/source-declarations.csv format):
# matches each row to a DataNeeds element, records system/format/refresh/steward,
# flips the catalog row's SourceState, and routes unmatched declarations to the
# review queue (never silently creating catalog rows).

import csv
import sqlite3
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "demo" / "cll_spm.db"

TODAY = date(2026, 9, 19).isoformat()

DECLARATION_HEADER = ["Element", "System", "Format", "Refresh", "Steward", "Notes"]


def _normalize(s):
    return " ".join((s or "").lower().split())


def _match(need_rows, element):
    """Match a declaration element to a catalog row: exact then substring,
    both directions, normalized. Returns NeedId or None."""
    target = _normalize(element)
    best = None
    for n in need_rows:
        name = _normalize(n["Element"])
        if name == target:
            return n["NeedId"]
        # strip KPI parentheticals for looser match: "Learner touchpoints (KPI-006)" -> "learner touchpoints"
        base = name.split(" (")[0].strip()
        if target and (base in target or target in base) and len(target) > 5:
            best = best or n["NeedId"]
    return best


def load_declarations(con, csv_path, today=None):
    """Capture declarations. Returns (matched, unmatched) lists of
    (element, need_id) / (element, reason) tuples."""
    today = today or TODAY
    with open(csv_path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    needs = [dict(r) for r in con.execute("SELECT NeedId, Element FROM DataNeeds").fetchall()]

    matched, unmatched = [], []
    n = 0
    for row in rows:
        element = (row.get("Element") or "").strip()
        if not element:
            continue
        n += 1
        # example rows in the template are not real declarations
        if element.lower().startswith("(example)"):
            continue
        need_id = _match(needs, element)
        dec_id = f"SD-{len(str(n)):04d}"
        con.execute(
            "INSERT OR REPLACE INTO SourceDeclarations VALUES (?,?,?,?,?,?,?,?,?)",
            (dec_id, element, row.get("System") or None, row.get("Format") or None,
             row.get("Refresh") or None, row.get("Steward") or None, row.get("Notes") or None,
             need_id, today))
        if need_id:
            # declaration upgrades the catalog row (MISSING -> HAVE/PARTIAL)
            state = "PARTIAL" if (row.get("System") or "").strip().lower() in ("", "tbd") else "HAVE"
            con.execute(
                "UPDATE DataNeeds SET SourceState=?, SourceSystem=?, SourceFormat=?,"
                " SourceRefresh=?, Steward=? WHERE NeedId=?",
                (state, row.get("System") or None, row.get("Format") or None,
                 row.get("Refresh") or None, row.get("Steward") or None, need_id))
            matched.append((element, need_id, state))
        else:
            unmatched.append((element, "no catalog match — review queue"))

    return matched, unmatched


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else ROOT / "sharepoint" / "seed" / "source-declarations.csv"
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    matched, unmatched = load_declarations(con, path)
    con.commit()
    con.close()
    for e, nid, st in matched:
        print(f"matched: {e} -> {nid} (state {st})")
    for e, why in unmatched:
        print(f"unmatched: {e} ({why})")