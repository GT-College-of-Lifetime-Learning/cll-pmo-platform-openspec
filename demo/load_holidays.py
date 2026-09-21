# CLL-SPM holiday calendar loader — the first P3 integration increment.
# Takes a confirmed Institute holiday calendar (sharepoint/seed/gt-holidays.csv,
# Date,Name) and regenerates the business-day calendar from it, recording the
# origin on the catalog row (DN-019). Replaces the REVIEW-flagged placeholders
# in gen_business_days.py.

import csv
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "demo" / "cll_spm.db"
HOLIDAYS_CSV = ROOT / "sharepoint" / "seed" / "gt-holidays.csv"
BD_CSV = ROOT / "sharepoint" / "lists" / "business-days.csv"

START, END = "2026-09-01", "2027-12-31"


def read_confirmed(path=HOLIDAYS_CSV):
    """Confirmed holiday dates from the steward-provided file."""
    dates = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            dates[row["Date"].strip()] = (row.get("Name") or "").strip()
    return dates


def regenerate_business_days(holidays):
    """Write sharepoint/lists/business-days.csv using the confirmed calendar."""
    import datetime as dt
    start = dt.date.fromisoformat(START)
    end = dt.date.fromisoformat(END)
    hol = {dt.date.fromisoformat(d) for d in holidays}

    BD_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(BD_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Date", "IsBusinessDay", "BDOfYear", "MonthEnd", "QuarterEnd", "IsHoliday"])
        d = start
        bd_year = 0
        while d <= end:
            bd = d.weekday() < 5 and d not in hol
            if d.month == 1 and d.day == 1:
                bd_year = 0
            if bd:
                bd_year += 1
            month_end = (d + dt.timedelta(days=1)).month != d.month
            quarter_end = month_end and d.month in (3, 6, 9, 12)
            w.writerow([d.isoformat(), int(bd), bd_year if bd else "",
                        int(month_end), int(quarter_end), int(d in hol)])
            d += dt.timedelta(days=1)


def run(today=None):
    holidays = read_confirmed()
    regenerate_business_days(holidays)

    # rebuild the demo DB's BusinessDays table from the regenerated CSV FIRST
    # (build_db re-seeds the catalog, so the DN-019 flip must come after)
    subprocess.run([sys.executable, str(ROOT / "demo" / "build_db.py")],
                   cwd=ROOT, capture_output=True)

    con = sqlite3.connect(DB)
    con.execute("UPDATE DataNeeds SET SourceState='HAVE', SourceSystem='steward-confirmed calendar',"
                " SourceFormat='gt-holidays.csv', SourceRefresh='annual', Steward='Strategic Operations',"
                " Notes='confirmed calendar imported ' || ? WHERE NeedId='DN-019'", (today or "",))
    con.commit()
    con.close()
    return len(holidays)


if __name__ == "__main__":
    n = run(today="2026-09-19")
    print(f"Imported {n} confirmed holidays; business-day calendar regenerated;"
          f" demo DB rebuilt; DN-019 flipped to HAVE.")