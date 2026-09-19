# CLL-SPM business-day calendar generator (task 2.11).
# Produces sharepoint/lists/business-days.csv — one row per calendar day with
# business-day flags and month/quarter period ends, consumed by:
#   - flows F5/F6/F7 (reminders, escalation, call-up window close) via a lookup
#   - Power BI due/stale measures (task 4.6)
#
# Georgia Tech holidays 2026-2027 are PLACEHOLDERS marked REVIEW: confirm the
# official holiday calendar with Strategic Operations before go-live.

import csv
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "sharepoint" / "lists" / "business-days.csv"

# REVIEW: official GT holiday calendar — placeholder dates only.
HOLIDAYS = {
    # 2026
    dt.date(2026, 11, 26), dt.date(2026, 11, 27),  # Thanksgiving (placeholder)
    dt.date(2026, 12, 24), dt.date(2026, 12, 25),   # Winter break (placeholder)
    dt.date(2026, 12, 31),
    # 2027
    dt.date(2027, 1, 1), dt.date(2027, 1, 18),     # New Year / MLK Day (placeholder)
    dt.date(2027, 5, 31),                           # Memorial Day (placeholder)
    dt.date(2027, 7, 5),                            # Independence Day observed (placeholder)
    dt.date(2027, 9, 6),                            # Labor Day (placeholder)
    dt.date(2027, 11, 24), dt.date(2027, 11, 25),   # Thanksgiving (placeholder)
    dt.date(2027, 12, 23), dt.date(2027, 12, 24),   # Winter break (placeholder)
}

START = dt.date(2026, 9, 1)
END = dt.date(2027, 12, 31)

def is_business_day(d: dt.date) -> bool:
    return d.weekday() < 5 and d not in HOLIDAYS

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Business-day ordinal: 1 = first business day of the period.
    # BusinessDaysToDate accumulates within the calendar year for simple
    # "add N business days" math in flows and measures.
    bd_year = 0
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Date", "IsBusinessDay", "BDOfYear", "MonthEnd", "QuarterEnd", "IsHoliday"])
        d = START
        while d <= END:
            bd = is_business_day(d)
            if d.month == 1 and d.day == 1:
                bd_year = 0
            if bd:
                bd_year += 1
            month_end = (d + dt.timedelta(days=1)).month != d.month
            q_month = d.month
            quarter_end = (d + dt.timedelta(days=1)).month != q_month and q_month in (3, 6, 9, 12)
            w.writerow([d.isoformat(), int(bd), bd_year if bd else "", int(month_end), int(quarter_end), int(d in HOLIDAYS)])
            d += dt.timedelta(days=1)
    print(f"Wrote {OUT} ({(END - START).days + 1} days)")

if __name__ == "__main__":
    main()