# CLL-SPM seed loader — loads sharepoint/seed/*.csv into the registry lists.
# Tasks 2.6 (Units, UnitAccess), 2.7 (StrategicPriorities, StrategicObjectives, portfolios),
# 2.8 (KPIs) of add-portfolio-registry-and-exec-dashboards.
#
# CSV column names match the seed files; this script maps them onto the list schema
# in sharepoint/registry-lists.json so a `--check` run validates seed data against
# the schema WITHOUT a live tenant.
#
# Usage:
#   python seed_loader.py --check                  # validate CSVs against schema, no tenant
#   python seed_loader.py --check --strict-provisional   # fail if any non-provisional row found
#
# Live loading (once OIT task 0.7 delivers the site) goes through PnP PowerShell:
#   Invoke-PnPListItemRest / Add-PnPDataRowsToSiteTemplate are the candidates; the
#   export side of this script emits a PnP-consumable data XML per list.

import argparse
import csv
import json
import sys
import xml.sax.saxutils as sax
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "sharepoint" / "registry-lists.json"
SEED = ROOT / "sharepoint" / "seed"

# CSV column -> list field internal name, per list.
# Only lists that carry seed data have a mapping here.
MAPPINGS = {
    "Units": {
        "file": "units.csv",
        "columns": {
            "UnitId": "UnitId",
            "Name": "Name",
            "Head": "Head",
            "Active": "UnitActive",
            "PilotWave": "PilotWave",
            "Note": "UnitNote",
        },
        # units.csv notes say to remove the TODO row before loading; enforce that.
        "skip_rows_where": {"Note": "Remove this row"},
        "required": ["UnitId", "Name", "Active"],
    },
    "StrategicPriorities": {
        "file": "strategic-priorities.csv",
        "columns": {
            "PriorityId": "PriorityId",
            "Title": "Title",
            "ExecOwner": "ExecOwner",
            "EffectiveFrom": "EffectiveFrom",
            "EffectiveTo": "EffectiveTo",
            "Provisional": "Provisional",
            "Source": "Source",
        },
        "required": ["PriorityId", "Title"],
        "must_be_provisional": True,
    },
    "StrategicObjectives": {
        "file": "strategic-objectives.csv",
        "columns": {
            "ObjectiveId": "ObjectiveId",
            "PriorityId": "ObjPriorityId",
            "Title": "ObjTitle",
            "Provisional": "ObjProvisional",
        },
        "required": ["ObjectiveId", "PriorityId", "Title"],
        "must_be_provisional": True,
    },
    "KPIs": {
        "file": "kpis.csv",
        "columns": {
            "KpiId": "KpiId",
            "Name": "KpiName",
            "PriorityId": "KpiPriorityId",
            "ObjectiveId": "KpiObjectiveId",
            "UnitOfMeasure": "UnitOfMeasure",
            "Direction": "Direction",
            "Baseline": "Baseline",
            "Target": "Target",
            "TargetDate": "TargetDate",
            "Frequency": "Frequency",
            "Method": "Method",
            "Provisional": "ProvisionalFlag",
            "Owner": "KpiOwner",
            "Note": "KpiNote",
        },
        "required": ["KpiId", "Name", "PriorityId", "Frequency"],
        # Target/TargetDate may be blank when the target is defined relative to a
        # pending baseline (KPI-008) or the source plan states no date (KPI-009,
        # KPI-011) — the spec's "Baseline pending" scenario covers display.
        "must_be_provisional": True,
        # Definition column is optional in seed; carries into KpiDefinition when present.
        "optional_columns": {"Definition": "KpiDefinition"},
    },
    "WorkItems": {
        "file": "work-items-backfill.csv",
        "columns": {
            "ItemId": "ItemId",
            "Level": "Level",
            "Title": "Title",
            "ParentId": "ParentId",
            "PortfolioId": "WorkPortfolioId",
            "PrimaryPriorityId": "PrimaryPriorityId",
            "PrimaryObjectiveId": "PrimaryObjectiveId",
            "AlignmentCategory": "AlignmentCategory",
            "AlignmentJustification": "AlignmentJustification",
            "Tier": "Tier",
            "LeadUnitId": "LeadUnitId",
            "ContributingUnitIds": "ContributingUnitIds",
            "Sponsor": "Sponsor",
            "Lead": "Lead",
            "Stage": "Stage",
            "StartDate": "StartDate",
            "TargetEndDate": "TargetEndDate",
            "EffortEstimateHrs": "EffortEstimateHrs",
            "CostEstimate": "CostEstimate",
            "ExecutionTool": "ExecutionTool",
            "ExecutionLink": "ExecutionLink",
            "Confidential": "Confidential",
            "Backfilled": "Backfilled",
        },
        "required": ["ItemId", "Level", "Title", "Tier", "LeadUnitId", "Stage"],
        "note": "Backfill import path — full import automation is task 2.10; this row (CLL-26-0001) is the standing template.",
    },
}

TRUTHY = {"TRUE", "T", "YES", "Y", "1"}
FALSY = {"FALSE", "F", "NO", "N", "0", ""}


def coerce(value: str, field_type: str):
    """Coerce CSV text to the JSON type the schema declares."""
    v = value.strip()
    if field_type == "Boolean":
        if v.upper() in TRUTHY:
            return True
        if v.upper() in FALSY:
            return False
        raise ValueError(f"cannot coerce {value!r} to Boolean")
    if field_type == "Number":
        return float(v) if v else None
    if field_type == "Choice":
        # Choice values must exist in the schema's choices list; blank passes through.
        return v or None
    return v or None


def load_schema():
    with open(SCHEMA, encoding="utf-8-sig") as fh:
        return {lst["title"]: lst for lst in json.load(fh)["lists"]}


def check(strict_provisional: bool) -> int:
    schema = load_schema()
    errors = []

    for list_name, mapping in MAPPINGS.items():
        path = SEED / mapping["file"]
        if not path.exists():
            errors.append(f"{list_name}: missing seed file {mapping['file']}")
            continue
        lst = schema.get(list_name)
        if lst is None:
            errors.append(f"{list_name}: not in schema")
            continue
        fields = {f["internalName"]: f for f in lst["fields"]}
        columns = dict(mapping["columns"])
        columns.update(mapping.get("optional_columns", {}))

        with open(path, encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))

        if not rows:
            errors.append(f"{list_name}: {mapping['file']} has no data rows")
            continue

        for n, row in enumerate(rows, start=2):  # line 1 is the header
            prefix = f"{list_name} row {n} ({row.get('Title') or row.get(list(mapping['columns'])[0])})"

            if "skip_rows_where" in mapping and any(
                row.get(k) == v for k, v in mapping["skip_rows_where"].items()
            ):
                continue

            # required columns present and non-empty
            for req in mapping["required"]:
                if not (row.get(req) or "").strip():
                    errors.append(f"{prefix}: missing required field {req}")

            # mapped fields must exist in the schema with a compatible type
            for csv_col, field_name in columns.items():
                raw = (row.get(csv_col) or "").strip()
                if not raw:
                    continue
                field = fields.get(field_name)
                if field is None:
                    errors.append(f"{prefix}: schema has no field {field_name} for CSV column {csv_col}")
                    continue
                try:
                    coerced = coerce(raw, field["type"])
                except ValueError as exc:
                    errors.append(f"{prefix}: {field_name}: {exc}")
                    continue
                if field["type"] == "Choice" and field.get("choices") and coerced not in field["choices"]:
                    errors.append(
                        f"{prefix}: {field_name}: {coerced!r} not in choices {field['choices']}"
                    )

            # provisional discipline: everything seeded from the brochure is Provisional
            if strict_provisional or mapping.get("must_be_provisional"):
                prov = (row.get("Provisional") or "").strip().upper()
                if prov not in TRUTHY and mapping.get("must_be_provisional"):
                    errors.append(f"{prefix}: seed rows must be Provisional=TRUE")

        loaded = len([r for r in rows if not any(
            r.get(k) == v for k, v in mapping.get("skip_rows_where", {}).items())])
        print(f"OK  {list_name}: {loaded} rows validated against schema ({mapping['file']})")

    if errors:
        print()
        for e in errors:
            print(f"ERR {e}", file=sys.stderr)
        return 1
    print("\nAll seed files validate against the registry schema.")
    return 0


def esc(v) -> str:
    return sax.escape(str(v))


def xml_type(v) -> str:
    if isinstance(v, bool):
        return "Boolean" if v else "Boolean"
    if isinstance(v, (int, float)):
        return "Number"
    return "Text"


def emit_pnp_data(list_name: str, mapping: dict, schema: dict, out_dir: Path) -> Path:
    """Emit a PnP provisioning <pnp:File>/DataRows-style XML fragment for one list.

    Task 2.10: the backfill import path. Strategic Operations imports a
    standard spreadsheet (work-items-backfill.csv shape), this emits a
    PnP-consumable XML with <pnp:DataRow> elements that Add-PnPDataRowsToSiteTemplate
    applies to the live site. IDs (CLL-YY-NNNN) are supplied by the template
    itself — the CSV's ItemId column must already be populated (the analyst
    gets IDs from Strategic Operations' counter before import).
    """
    lst = schema[list_name]
    fields = {f["internalName"]: f for f in lst["fields"]}
    columns = dict(mapping["columns"])
    columns.update(mapping.get("optional_columns", {}))

    path = SEED / mapping["file"]
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    out_path = out_dir / f"{list_name}.data.xml"
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write('<?xml version="1.0" encoding="utf-8"?>\n')
        fh.write('<pnp:DataRows xmlns:pnp="http://schemas.microsoft.com/pnp/provisioning/2021/03" '
                 'List="{}">\n'.format(esc(list_name)))
        for row in rows:
            if "skip_rows_where" in mapping and any(
                row.get(k) == v for k, v in mapping["skip_rows_where"].items()
            ):
                continue
            fh.write("  <pnp:DataRow>\n")
            for csv_col, field_name in columns.items():
                raw = (row.get(csv_col) or "").strip()
                if not raw:
                    continue
                field = fields[field_name]
                v = coerce(raw, field["type"])
                if field["type"] == "Boolean":
                    val = "true" if v else "false"
                else:
                    val = esc(v)
                fh.write(f'    <pnp:DataValue FieldName="{esc(field_name)}">{val}</pnp:DataValue>\n')
            fh.write("  </pnp:DataRow>\n")
        fh.write("</pnp:DataRows>\n")
    return out_path


def export(out_dir_name: str) -> int:
    schema = load_schema()
    out_dir = ROOT / "sharepoint" / out_dir_name
    out_dir.mkdir(parents=True, exist_ok=True)
    # Validation gate first: never emit data that fails the check.
    if check(strict_provisional=False) != 0:
        print("Refusing to export: seed data failed validation.", file=sys.stderr)
        return 1
    for list_name in ("Units", "StrategicPriorities", "StrategicObjectives", "KPIs", "WorkItems"):
        p = emit_pnp_data(list_name, MAPPINGS[list_name], schema, out_dir)
        print(f"OK  {p}")
    print(f"\nPnP data XML emitted to {out_dir}")
    print("Apply with: Add-PnPDataRowsToSiteTemplate / Invoke-PnPTemplate against the target site.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Validate (and later load) CLL-SPM seed data")
    ap.add_argument("--check", action="store_true", help="validate seed CSVs against the schema")
    ap.add_argument("--strict-provisional", action="store_true",
                    help="require Provisional=TRUE on every strategy seed row")
    ap.add_argument("--export", action="store_true",
                    help="emit PnP data XML per list (task 2.10 import path)")
    ap.add_argument("--out-dir", default="lists", help="output dir under sharepoint/ for --export")
    args = ap.parse_args()
    if args.export:
        sys.exit(export(args.out_dir))
    if not args.check:
        ap.print_help()
        sys.exit(2)
    sys.exit(check(args.strict_provisional))