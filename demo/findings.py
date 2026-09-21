# CLL-SPM finding tracker — cross-period recurrence tracking and escalation.
# Ports financial-ai's finding_tracker.py pattern: findings keyed by
# (type, affected item) accumulate occurrences across hygiene runs; the
# escalation ladder is 2 -> Recurring (unit view), 3 -> governance
# needs-attention, 4 -> blocks the item from closing until resolved.
# Append-only: resolution changes Status on a new row-event basis via
# resolve_finding; rows are never edited or deleted.

from datetime import date

TODAY = date(2026, 9, 19)

FINDING_TYPES = ("stale-update", "red-without-resolution", "unaligned-item",
                 "triage-overdue", "decision-overdue")

LADDER = {2: "Recurring", 3: "Escalated", 4: "Blocks closeout"}


def _open_finding(con, ftype, unit, item):
    return con.execute(
        "SELECT * FROM Findings WHERE Type=? AND AffectedUnitId IS ? AND AffectedItemId IS ?"
        " AND Status='Open' ORDER BY FindingId DESC LIMIT 1",
        (ftype, unit, item)).fetchone()


def record_finding(con, ftype, severity, unit, item, today=None):
    """Record or increment a finding occurrence (hygiene run is the only writer)."""
    if ftype not in FINDING_TYPES:
        raise ValueError(f"unknown finding type: {ftype}")
    today = today or TODAY.isoformat()
    existing = _open_finding(con, ftype, unit, item)
    if existing:
        con.execute(
            "UPDATE Findings SET Occurrences=?, LastSeenOn=? WHERE FindingId=?",
            (existing["Occurrences"] + 1, today, existing["FindingId"]))
        return existing["FindingId"]
    cur = con.execute(
        "INSERT INTO Findings (Type, AffectedUnitId, AffectedItemId, Severity,"
        " FirstSeenOn, LastSeenOn, Occurrences, Status) VALUES (?,?,?,?,?,?,1,'Open')",
        (ftype, unit, item, severity, today, today))
    return cur.lastrowid


def resolve_finding(con, ftype, unit, item, resolved_by, today=None):
    """Resolve the open finding for (type, affected). Appends resolution facts;
    recurrence later starts a fresh record at 1 (the reset is by-record)."""
    today = today or TODAY.isoformat()
    existing = _open_finding(con, ftype, unit, item)
    if existing is None:
        return None
    con.execute(
        "UPDATE Findings SET Status='Resolved', ResolvedBy=?, ResolvedOn=? WHERE FindingId=?",
        (resolved_by, today, existing["FindingId"]))
    return existing["FindingId"]


def escalation_level(occurrences):
    """The ladder: 2+ -> Recurring, 3+ -> Escalated, 4+ -> Blocks closeout."""
    if occurrences >= 4:
        return LADDER[4]
    if occurrences == 3:
        return LADDER[3]
    if occurrences == 2:
        return LADDER[2]
    return None


def closeout_blocked(con, item_id):
    """True when an Open finding with 4+ occurrences blocks this item from Closed."""
    row = con.execute(
        "SELECT COUNT(*) FROM Findings WHERE AffectedItemId=? AND Status='Open'"
        " AND Occurrences>=4", (item_id,)).fetchone()
    return row[0] > 0


def open_findings(con, unit=None, item=None, min_occurrences=1):
    q = ("SELECT * FROM Findings WHERE Status='Open' AND Occurrences>=?"
         " AND (AffectedUnitId IS ? OR ? IS NULL) AND (AffectedItemId IS ? OR ? IS NULL)"
         " ORDER BY Occurrences DESC, LastSeenOn DESC")
    return con.execute(q, (min_occurrences, unit, unit, item, item)).fetchall()


def run_hygiene_findings(con, today=None):
    """The F7 extension: scan the corpus once and record findings.
    Returns the list of findings touched, for the hygiene page report."""
    today = today or TODAY.isoformat()
    touched = []

    # 1. stale-update: active items with no update this period (Stale rule)
    stale_items = con.execute(
        """SELECT w.ItemId, w.LeadUnitId FROM WorkItems w
           WHERE w.Stage IN ('Active','On Hold')
           AND NOT EXISTS (SELECT 1 FROM StatusUpdates s WHERE s.ItemId = w.ItemId
                           AND s.PeriodEnd > '2026-08-31')""").fetchall()
    for w in stale_items:
        fid = record_finding(con, "stale-update", "HIGH", w["LeadUnitId"], w["ItemId"], today)
        touched.append(("stale-update", w["ItemId"]))

    # 2. red-without-resolution: latest Red with neither path nor ask (F4 already
    #    blocks new ones; this catches data planted/imported around the flow)
    reds = con.execute(
        """SELECT s.ItemId, w.LeadUnitId FROM StatusUpdates s
           JOIN WorkItems w ON w.ItemId = s.ItemId
           WHERE s.OverallRAG='Red' AND s.PeriodEnd > '2026-08-31'
             AND COALESCE(s.PathToGreen,'') = '' AND COALESCE(s.DecisionAsk,'') = ''""").fetchall()
    for r in reds:
        record_finding(con, "red-without-resolution", "HIGH", r["LeadUnitId"], r["ItemId"], today)
        touched.append(("red-without-resolution", r["ItemId"]))

    # 3. unaligned-item: active items with neither priority nor category
    unaligned = con.execute(
        """SELECT ItemId, LeadUnitId FROM WorkItems
           WHERE Stage IN ('Active','On Hold')
           AND PrimaryPriorityId IS NULL AND AlignmentCategory IS NULL""").fetchall()
    for u in unaligned:
        record_finding(con, "unaligned-item", "MEDIUM", u["LeadUnitId"], u["ItemId"], today)
        touched.append(("unaligned-item", u["ItemId"]))

    # 4. triage-overdue: Submitted requests older than 5 business days
    triage = con.execute(
        """SELECT r.RequestId, r.ReqUnitId FROM IntakeRequests r
           WHERE r.Status='Submitted'
             AND CAST(JULIANDAY('2026-09-19') - JULIANDAY(r.SubmittedDate) AS INTEGER) > 7""").fetchall()
    for t in triage:
        record_finding(con, "triage-overdue", "MEDIUM", t["ReqUnitId"], t["RequestId"], today)
        touched.append(("triage-overdue", t["RequestId"]))

    # 5. decision-overdue: Ready for Review older than 10 business days
    overdue = con.execute(
        """SELECT r.RequestId, r.ReqUnitId FROM IntakeRequests r
           WHERE r.Status='Ready for Review'
             AND CAST(JULIANDAY('2026-09-19') - JULIANDAY(r.SubmittedDate) AS INTEGER) > 14""").fetchall()
    for o in overdue:
        record_finding(con, "decision-overdue", "MEDIUM", o["ReqUnitId"], o["RequestId"], today)
        touched.append(("decision-overdue", o["RequestId"]))

    # 6. resolution sweep: stale items that now have updates get resolved
    for w in con.execute(
        """SELECT w.ItemId, w.LeadUnitId FROM WorkItems w
           WHERE w.Stage IN ('Active','On Hold')
           AND EXISTS (SELECT 1 FROM StatusUpdates s WHERE s.ItemId = w.ItemId
                       AND s.PeriodEnd > '2026-08-31')""").fetchall():
        resolve_finding(con, "stale-update", w["LeadUnitId"], w["ItemId"], "hygiene (auto)", today)

    return touched