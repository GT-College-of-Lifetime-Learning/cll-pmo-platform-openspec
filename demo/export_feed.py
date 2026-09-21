# CLL-SPM data feed exporter — versioned files + manifest for external consumers.
# Ports financial-ai's export_dashboard_feed.py pattern (V-07 injection guard,
# empty-state discipline, manifest with row counts). The /api/feed endpoint serves
# these files; the dashboard queries the DB directly (feed is the external contract).

import csv
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DEMO = Path(__file__).resolve().parent
DB = DEMO / "cll_spm.db"
OUT = DEMO / "output" / "feed"

FEED_VERSION = 1

TODAY = "2026-09-19"


def _neutralize_cell(v):
    """CSV-injection guard: a cell beginning with =, +, -, @ would execute as a
    formula in Excel/Sheets. Prefix a single quote so it renders as text.
    Numeric cells are untouched (they are the feed's payload)."""
    if isinstance(v, (int, float, bool)) or v is None:
        return v
    s = str(v)
    if s and s[0] in ("=", "+", "-", "@"):
        return "'" + s
    return s


def _rows(con, sql, params=()):
    return [dict(r) for r in con.execute(sql, params).fetchall()]


def export_feed(out_dir=None):
    out = Path(out_dir) if out_dir else OUT
    out.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    manifest = {"feed_version": FEED_VERSION,
                 "generated_at": datetime.now().isoformat(timespec="seconds"),
                 "source": "cll_spm.db (demo build)",
                 "files": {}}

    def write(name, header, rows):
        path = out / name
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            for r in rows:
                w.writerow([_neutralize_cell(r.get(h)) for h in header])
        manifest["files"][name] = len(rows)
        return path

    # kpis.csv — headline + all KPIs with latest values and provenance
    kpis = _rows(con, """
        SELECT k.KpiId, k.KpiName, k.KpiPriorityId, k.DashboardRole, k.Basis,
               k.Target, k.Frequency,
               (SELECT Value FROM KpiValues v WHERE v.KpiValueId = k.KpiId
                 ORDER BY v.PeriodEnd DESC LIMIT 1) AS LatestValue,
               (SELECT PeriodEnd FROM KpiValues v WHERE v.KpiValueId = k.KpiId
                 ORDER BY v.PeriodEnd DESC LIMIT 1) AS AsOf,
               (SELECT SubmittedBy FROM KpiValues v WHERE v.KpiValueId = k.KpiId
                 ORDER BY v.PeriodEnd DESC LIMIT 1) AS Submitter
        FROM KPIs k ORDER BY k.KpiId""")
    write("kpis.csv", ["KpiId", "KpiName", "PriorityId", "DashboardRole", "Basis",
                      "Target", "Frequency", "LatestValue", "AsOf", "Submitter"], kpis)

    # rag-counts.csv — G/A/R/Stale counts per priority (college-level aggregate,
    # masked confidential counts included so totals tie to dashboards)
    rag = _rows(con, """
        SELECT w.PrimaryPriorityId AS PriorityId,
               SUM(CASE WHEN s.OverallRAG='Green' THEN 1 ELSE 0 END) AS Green,
               SUM(CASE WHEN s.OverallRAG='Amber' THEN 1 ELSE 0 END) AS Amber,
               SUM(CASE WHEN s.OverallRAG='Red' THEN 1 ELSE 0 END) AS Red,
               SUM(CASE WHEN s.OverallRAG IS NULL OR s.PeriodEnd <= '2026-08-31' THEN 1 ELSE 0 END) AS Stale,
               COUNT(*) AS Total
        FROM WorkItems w
        LEFT JOIN (SELECT ItemId, OverallRAG, PeriodEnd FROM StatusUpdates
                   WHERE PeriodEnd IN (SELECT MAX(PeriodEnd) FROM StatusUpdates GROUP BY ItemId)) s
                   ON s.ItemId = w.ItemId
        WHERE w.Stage IN ('Active','On Hold')
        GROUP BY w.PrimaryPriorityId""")
    masked = _rows(con, """
        SELECT CCPriorityId AS PriorityId, SUM(CCCount) AS ConfidentialCount
        FROM ConfidentialCounts GROUP BY CCPriorityId""")
    masked_by = {r["PriorityId"]: r["ConfidentialCount"] for r in masked}
    for r in rag:
        r["ConfidentialMasked"] = masked_by.get(r["PriorityId"], 0)
    write("rag-counts.csv", ["PriorityId", "Green", "Amber", "Red", "Stale",
                             "Total", "ConfidentialMasked"], rag)

    # currency.csv — status currency summary
    cur = _rows(con, """
        SELECT COUNT(*) AS ActiveItems,
               SUM(CASE WHEN EXISTS (SELECT 1 FROM StatusUpdates s WHERE s.ItemId = w.ItemId
                                     AND s.PeriodEnd > '2026-08-31') THEN 1 ELSE 0 END) AS CurrentItems
        FROM WorkItems w WHERE w.Stage IN ('Active','On Hold')""")
    for r in cur:
        r["CurrencyPct"] = round(100 * (r["CurrentItems"] or 0) / r["ActiveItems"], 1) if r["ActiveItems"] else 100
    write("currency.csv", ["ActiveItems", "CurrentItems", "CurrencyPct"], cur)

    # intake-aging.csv — open pipeline by status with ages
    intake = _rows(con, """
        SELECT Status, COUNT(*) AS Count,
               CAST(AVG(CAST(JULIANDAY('2026-09-19') - JULIANDAY(SubmittedDate) AS REAL)) AS INT) AS AvgAgeDays
        FROM IntakeRequests
        WHERE Status NOT IN ('Approved','Declined')
        GROUP BY Status ORDER BY Status""")
    write("intake-aging.csv", ["Status", "Count", "AvgAgeDays"], intake)

    # readiness.json — the gate states at export time
    import sys
    sys.path.insert(0, str(DEMO.parent))
    import demo.readiness as readiness
    gates, has_blocking, has_warn = readiness.evaluate()
    readiness_doc = {
        "as_of": TODAY,
        "has_blocking": has_blocking,
        "has_warn": has_warn,
        "gates": gates,
    }
    (out / "readiness.json").write_text(json.dumps(readiness_doc, indent=2), encoding="utf-8")
    manifest["files"]["readiness.json"] = len(gates)

    # findings.json — escalated findings summary (aggregate only, masked details)
    escalated = _rows(con, """
        SELECT Type, AffectedUnitId, Occurrences, FirstSeenOn, LastSeenOn
        FROM Findings WHERE Status='Open' AND Occurrences >= 2
        ORDER BY Occurrences DESC""")
    (out / "findings.json").write_text(json.dumps(escalated, indent=2), encoding="utf-8")
    manifest["files"]["findings.json"] = len(escalated)

    # coverage.json — per-need source state + per-view aggregates (data-sourcing spec)
    needs = _rows(con, "SELECT NeedId, Element, ConsumerView, DefinitionState,"
                       " SourceState FROM DataNeeds ORDER BY NeedId")
    cov = {"needs": needs, "undefined": [n for n in needs
                                          if n["DefinitionState"].startswith("UNDEFINED")],
           "totals": {"HAVE": sum(1 for n in needs if n["SourceState"] == "HAVE"),
                      "PARTIAL": sum(1 for n in needs if n["SourceState"] == "PARTIAL"),
                      "MISSING": sum(1 for n in needs if n["SourceState"] == "MISSING")}}
    (out / "coverage.json").write_text(json.dumps(cov, indent=2), encoding="utf-8")
    manifest["files"]["coverage.json"] = len(needs)

    con.close()
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    m = export_feed()
    print(json.dumps(m, indent=2))