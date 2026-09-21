# CLL-SPM data-source matrix generator.
# Renders docs/data-source-matrix.md from the DataNeeds catalog (the source of
# truth). Drift check (data-sourcing spec): a hand-edited committed matrix is
# detected, reported, and replaced with catalog truth.
#
#   python demo/generate_matrix.py            # generate + drift-check + write
#   python demo/generate_matrix.py --check    # exit 1 if the committed file drifts

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "demo" / "cll_spm.db"
MATRIX = ROOT / "docs" / "data-source-matrix.md"

STATE_EMOJI = {"HAVE": "sourced", "PARTIAL": "partial", "MISSING": "unsourced"}


def render() -> str:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    needs = [dict(r) for r in con.execute(
        "SELECT * FROM DataNeeds ORDER BY ConsumerView, NeedId").fetchall()]
    unmatched = [dict(r) for r in con.execute(
        "SELECT * FROM SourceDeclarations WHERE MatchedNeedId IS NULL").fetchall()]
    con.close()

    lines = [
        "# Data Source Matrix",
        "",
        "GENERATED from the DataNeeds catalog — do not edit by hand; regenerate with",
        "`python demo/generate_matrix.py` (drift is detected and replaced with catalog truth).",
        "",
        "The P2/P3 workflow: steward declares a source → row state flips → loader increment",
        "imports it tagged → coverage reflects it. UNDEFINED rows route to the sponsor first.",
        "",
    ]
    totals = {}
    for n in needs:
        totals[n["SourceState"]] = totals.get(n["SourceState"], 0) + 1
    lines += [
        f"**Coverage:** {totals.get('HAVE', 0)} sourced · {totals.get('PARTIAL', 0)} partial · "
        f"{totals.get('MISSING', 0)} unsourced · "
        f"{sum(1 for n in needs if n['DefinitionState'].startswith('UNDEFINED'))} definition-gated (sponsor first)",
        "",
    ]

    by_view = {}
    for n in needs:
        by_view.setdefault(n["ConsumerView"], []).append(n)
    for view, rows in sorted(by_view.items()):
        lines += [f"## {view}", "",
                  "| Need | Element | Cadence | Definition | State | System | Steward | Notes |",
                  "|---|---|---|---|---|---|---|---|"]
        for n in rows:
            notes = (n["Notes"] or "").replace("|", "\\|")
            sys_ = (n["SourceSystem"] or "—").replace("|", "\\|")
            lines.append(
                f"| {n['NeedId']} | {n['Element']} | {n['Cadence']} | {n['DefinitionState']} "
                f"| **{n['SourceState']}** | {sys_} | {n['Steward'] or '—'} | {notes} |")
        lines.append("")

    if unmatched:
        lines += ["## Unmatched declarations (review queue)", "",
                  "| Element | System | Steward | Recorded |", "|---|---|---|---|"]
        for d in unmatched:
            lines.append(f"| {d['Element']} | {d['System']} | {d['Steward']} | {d['RecordedOn']} |")
        lines.append("")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="fail (exit 1) if the committed matrix differs from catalog truth")
    args = ap.parse_args()

    truth = render()
    if MATRIX.exists():
        committed = MATRIX.read_text(encoding="utf-8")
        if committed != truth:
            if args.check:
                print("DRIFT: docs/data-source-matrix.md differs from the catalog.")
                print("Regenerate with: python demo/generate_matrix.py")
                return 1
            print("DRIFT detected: committed matrix differs from catalog truth;")
            print("hand edits are rejected — replacing with catalog rendering.")
    MATRIX.write_text(truth, encoding="utf-8")
    print(f"Generated {MATRIX.relative_to(ROOT)} from {len(truth.splitlines())} lines of catalog truth")
    return 0


if __name__ == "__main__":
    sys.exit(main())