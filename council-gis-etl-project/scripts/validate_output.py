"""Validate generated reporting outputs for the council GIS ETL project.

The script uses pandas when it is installed and falls back to standard-library
CSV checks when it is not. That keeps the interview project runnable on a
fresh Windows machine while still supporting richer dataframe checks.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any, Iterable

try:  # pandas is helpful, but this project should still validate without it.
    import pandas as pd  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - environment dependent
    pd = None


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
OUT_DIR = BASE_DIR / "data" / "expected_output"

REQUIRED_REPORT_COLUMNS = {
    "asset_id",
    "standard_asset_type",
    "asset_subtype",
    "service_area",
    "install_date",
    "install_year",
    "asset_age_years",
    "material",
    "diameter_mm",
    "condition",
    "operational_status",
    "last_inspection_date",
    "latest_maintenance_date",
    "latest_maintenance_type",
    "maintenance_count",
    "total_maintenance_cost",
    "average_maintenance_cost",
    "open_work_order_count",
    "urgent_work_order_count",
    "days_since_last_maintenance",
    "data_quality_flag",
    "latitude",
    "longitude",
    "geometry_type",
    "etl_processed_timestamp",
}
MANDATORY_REPORT_COLUMNS = [
    "asset_id",
    "standard_asset_type",
    "service_area",
    "install_date",
    "condition",
    "operational_status",
    "latitude",
    "longitude",
]
NUMERIC_COLUMNS = [
    "diameter_mm",
    "asset_age_years",
    "maintenance_count",
    "total_maintenance_cost",
    "average_maintenance_cost",
    "latitude",
    "longitude",
]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def ok(message: str) -> None:
    print(f"OK: {message}")


def read_csv_rows(path: Path, failures: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"Missing required file: {path}", failures)
        return []
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
    except Exception as exc:  # pragma: no cover - command-line script
        fail(f"Could not read {path.name}: {exc}", failures)
        return []


def read_csv_any(path: Path, failures: list[str]) -> Any:
    if pd is not None:
        if not path.exists():
            fail(f"Missing required file: {path}", failures)
            return pd.DataFrame()
        try:
            return pd.read_csv(path)
        except Exception as exc:  # pragma: no cover - command-line script
            fail(f"Could not read {path.name}: {exc}", failures)
            return pd.DataFrame()
    return read_csv_rows(path, failures)


def is_empty(data: Any) -> bool:
    return bool(data.empty) if pd is not None else len(data) == 0


def columns(data: Any) -> set[str]:
    return set(data.columns) if pd is not None else (set(data[0].keys()) if data else set())


def validate_geojson(path: Path, failures: list[str]) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.name} is not valid JSON: {exc}", failures)
        return
    if data.get("type") != "FeatureCollection" or not isinstance(data.get("features"), list):
        fail(f"{path.name} is not a GeoJSON FeatureCollection", failures)
    else:
        ok(f"{path.name} is valid GeoJSON structure")


def require_columns(data: Any, required: Iterable[str], label: str, failures: list[str]) -> None:
    missing = sorted(set(required) - columns(data))
    if missing:
        fail(f"{label} missing columns: {', '.join(missing)}", failures)
    else:
        ok(f"{label} contains required columns")


def parse_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_date(value: Any) -> date | None:
    try:
        if value is None or str(value) == "":
            return None
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def validate_report_stdlib(rows: list[dict[str, str]], failures: list[str]) -> None:
    ids = [row["asset_id"] for row in rows]
    if len(ids) != len(set(ids)):
        fail("Reporting dataset contains duplicate asset_id values", failures)
    else:
        ok("Reporting asset IDs are unique")
    if any(not row.get(col) for row in rows for col in MANDATORY_REPORT_COLUMNS):
        fail("Reporting dataset has missing mandatory values", failures)
    else:
        ok("Reporting mandatory fields are populated")
    for col in NUMERIC_COLUMNS:
        values = [parse_float(row.get(col)) for row in rows]
        if any(value is None for value in values):
            fail(f"Column {col} contains non-numeric values", failures)
    if any((parse_float(row.get("diameter_mm")) or 0) <= 0 for row in rows):
        fail("diameter_mm contains zero or negative values", failures)
    if any(parse_date(row.get("install_date")) is None for row in rows):
        fail("install_date contains invalid dates", failures)
    if all((parse_float(row.get("maintenance_count")) or 0) >= 0 and (parse_float(row.get("total_maintenance_cost")) or 0) >= 0 for row in rows):
        ok("Maintenance count and cost fields are non-negative")


def validate_report_pandas(report: Any, failures: list[str]) -> None:
    if report["asset_id"].duplicated().any():
        fail("Reporting dataset contains duplicate asset_id values", failures)
    else:
        ok("Reporting asset IDs are unique")
    missing_mandatory = report[MANDATORY_REPORT_COLUMNS].isna().any().any() or (report[MANDATORY_REPORT_COLUMNS].astype(str).eq("").any().any())
    if missing_mandatory:
        fail("Reporting dataset has missing mandatory values", failures)
    else:
        ok("Reporting mandatory fields are populated")
    for col in NUMERIC_COLUMNS:
        numeric = pd.to_numeric(report[col], errors="coerce")
        if numeric.isna().any():
            fail(f"Column {col} contains non-numeric values", failures)
    if (pd.to_numeric(report["diameter_mm"], errors="coerce") <= 0).any():
        fail("diameter_mm contains zero or negative values", failures)
    if pd.to_datetime(report["install_date"], errors="coerce").isna().any():
        fail("install_date contains invalid dates", failures)
    reconciled = (
        report["maintenance_count"].fillna(0).astype(int).ge(0).all()
        and pd.to_numeric(report["total_maintenance_cost"], errors="coerce").ge(0).all()
    )
    if reconciled:
        ok("Maintenance count and cost fields are non-negative")


def main() -> int:
    failures: list[str] = []
    if pd is None:
        print("INFO: pandas is not installed; using standard-library validation fallback.")

    for geojson_name in ["water_assets.geojson", "service_areas.geojson"]:
        validate_geojson(RAW_DIR / geojson_name, failures)

    report = read_csv_any(OUT_DIR / "asset_reporting_dataset.csv", failures)
    rejected = read_csv_any(OUT_DIR / "rejected_assets.csv", failures)
    unmatched = read_csv_any(OUT_DIR / "unmatched_maintenance_records.csv", failures)
    summary = read_csv_any(OUT_DIR / "data_quality_summary.csv", failures)
    maintenance = read_csv_any(RAW_DIR / "maintenance_records.csv", failures)

    if is_empty(report):
        fail("Reporting dataset is empty", failures)
    else:
        require_columns(report, REQUIRED_REPORT_COLUMNS, "asset_reporting_dataset.csv", failures)
        if pd is not None:
            validate_report_pandas(report, failures)
        else:
            validate_report_stdlib(report, failures)

    if not is_empty(rejected):
        ok(f"Rejected asset output contains {len(rejected)} rows")
    if not is_empty(unmatched):
        ok(f"Unmatched maintenance output contains {len(unmatched)} rows")
    if not is_empty(summary):
        require_columns(summary, {"metric", "value", "notes"}, "data_quality_summary.csv", failures)

    if not is_empty(maintenance) and not is_empty(unmatched):
        if pd is not None:
            raw_unmatched_ids = set(unmatched["work_order_id"].astype(str))
            maintenance_ids = set(maintenance["work_order_id"].astype(str))
        else:
            raw_unmatched_ids = {row["work_order_id"] for row in unmatched}
            maintenance_ids = {row["work_order_id"] for row in maintenance}
        if not raw_unmatched_ids.issubset(maintenance_ids):
            fail("Unmatched output contains work orders not present in source maintenance data", failures)
        else:
            ok("Unmatched work orders reconcile to the source maintenance data")

    print("\nValidation summary")
    print(f"Critical failures: {len(failures)}")
    for item in failures:
        print(f"- {item}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
