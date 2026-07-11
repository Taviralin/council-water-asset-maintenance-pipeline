"""Generate mock council water asset maintenance data.

The data is fictional and designed for interview practice. It deliberately
contains a small number of quality issues so an ETL workflow can demonstrate
validation, rejection, exception handling, aggregation, and spatial enrichment.
"""

from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


SEED = 20260710
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
REF_DIR = BASE_DIR / "data" / "reference"
OUT_DIR = BASE_DIR / "data" / "expected_output"
NOW = datetime.now(timezone.utc).replace(microsecond=0)

ASSET_TYPES = {
    "Water Pipe": ["Distribution Main", "Rider Main", "Service Line"],
    "Hydrant": ["Fire Hydrant", "Marker Hydrant"],
    "Manhole": ["Access Manhole", "Inspection Chamber"],
    "Valve": ["Isolation Valve", "Scour Valve", "Air Valve"],
    "Pump": ["Booster Pump", "Transfer Pump"],
}
TYPE_VARIANTS = {
    "Water Pipe": ["Water Pipe", "water pipe", "WaterPipe", "PIPE", "pipe", "water_pipe", " Water Pipe "],
    "Hydrant": ["Hydrant", "HYDRANT", "hydrant", "fire hydrant", " Hydrant "],
    "Manhole": ["Manhole", "MANHOLE", "man hole", "maintenance hole", " Manhole "],
    "Valve": ["Valve", "VALVE", "valve", "water valve", " Valve "],
    "Pump": ["Pump", "PUMP", "pump", "pump station", " Pump "],
}
MATERIALS = ["PVC", "concrete", "steel", "cast iron", "polyethylene"]
CONDITIONS = ["Good", "Fair", "Poor", "Critical"]
STATUSES = ["Active", "Inactive", "Planned", "Under Repair"]
TEAMS = ["Water Networks", "Reactive Maintenance", "Asset Renewals", "Operations North", "Operations South"]
MAINT_TYPES = [
    "Inspection",
    "Preventive Maintenance",
    "Leak Repair",
    "Pipe Replacement",
    "Hydrant Testing",
    "Pump Service",
    "Emergency Repair",
]
PRIORITIES = ["Low", "Medium", "High", "Urgent"]
WORK_STATUSES = ["Open", "In Progress", "Completed", "Cancelled"]
CONTRACTORS = ["Arawa Civil", "Bay Utility Services", "Rotorua Water Works", "Council Internal Crew", "PipeTech NZ"]


def ensure_dirs() -> None:
    for path in (RAW_DIR, REF_DIR, OUT_DIR):
        path.mkdir(parents=True, exist_ok=True)


def random_point() -> tuple[float, float]:
    """Return a plausible lon/lat around urban Rotorua."""
    return (round(random.uniform(176.205, 176.305), 6), round(random.uniform(-38.185, -38.095), 6))


def random_line() -> list[list[float]]:
    lon, lat = random_point()
    return [
        [lon, lat],
        [round(lon + random.uniform(0.001, 0.006), 6), round(lat + random.uniform(-0.003, 0.003), 6)],
    ]


def iso_date(start_year: int = 1970, end_year: int = 2025) -> str:
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).isoformat()


def service_areas() -> dict[str, Any]:
    areas = [
        ("SA01", "Western", "Mereana Kingi", 12, 176.190, -38.190, 176.235, -38.090),
        ("SA02", "Central", "James Patel", 10, 176.235, -38.175, 176.270, -38.105),
        ("SA03", "Eastern", "Anika Roberts", 14, 176.270, -38.185, 176.320, -38.095),
        ("SA04", "Northern", "Hemi Wilson", 16, 176.225, -38.105, 176.310, -38.055),
        ("SA05", "Southern", "Sarah Thompson", 18, 176.215, -38.225, 176.300, -38.175),
    ]
    features = []
    for area_id, name, manager, target, minx, miny, maxx, maxy in areas:
        ring = [[minx, miny], [maxx, miny], [maxx, maxy], [minx, maxy], [minx, miny]]
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "service_area_id": area_id,
                    "service_area_name": name,
                    "area_manager": manager,
                    "maintenance_target_days": target,
                },
                "geometry": {"type": "Polygon", "coordinates": [ring]},
            }
        )
    return {"type": "FeatureCollection", "features": features}


def point_in_polygon(lon: float, lat: float, polygon: list[list[float]]) -> bool:
    xs = [p[0] for p in polygon]
    ys = [p[1] for p in polygon]
    return min(xs) <= lon <= max(xs) and min(ys) <= lat <= max(ys)


def asset_centroid(feature: dict[str, Any]) -> tuple[float | None, float | None]:
    geom = feature.get("geometry")
    if not geom:
        return None, None
    if geom.get("type") == "Point":
        coords = geom.get("coordinates", [])
        return (coords[0], coords[1]) if len(coords) >= 2 else (None, None)
    if geom.get("type") == "LineString":
        coords = geom.get("coordinates", [])
        if not coords:
            return None, None
        return (sum(p[0] for p in coords) / len(coords), sum(p[1] for p in coords) / len(coords))
    return None, None


def standard_type(raw_value: Any) -> str | None:
    text = str(raw_value or "").strip().lower().replace("_", " ")
    mappings = {
        "water pipe": "Water Pipe",
        "waterpipe": "Water Pipe",
        "pipe": "Water Pipe",
        "hydrant": "Hydrant",
        "fire hydrant": "Hydrant",
        "manhole": "Manhole",
        "man hole": "Manhole",
        "maintenance hole": "Manhole",
        "valve": "Valve",
        "water valve": "Valve",
        "pump": "Pump",
        "pump station": "Pump",
    }
    return mappings.get(text)


def generate_assets() -> dict[str, Any]:
    features: list[dict[str, Any]] = []
    weights = ["Water Pipe"] * 45 + ["Hydrant"] * 20 + ["Valve"] * 18 + ["Manhole"] * 12 + ["Pump"] * 5
    for i in range(1, 101):
        base_type = random.choice(weights)
        geom = {"type": "LineString", "coordinates": random_line()} if base_type == "Water Pipe" else {"type": "Point", "coordinates": list(random_point())}
        diameter: int | str = random.choice([50, 80, 100, 150, 200, 250, 300, 450])
        feature = {
            "type": "Feature",
            "properties": {
                "asset_id": f"WA-{i:04d}",
                "asset_type": random.choice(TYPE_VARIANTS[base_type]),
                "asset_subtype": random.choice(ASSET_TYPES[base_type]),
                "install_date": iso_date(),
                "material": random.choice(MATERIALS),
                "diameter_mm": diameter,
                "condition": random.choices(CONDITIONS, weights=[45, 35, 15, 5])[0],
                "operational_status": random.choices(STATUSES, weights=[82, 5, 5, 8])[0],
                "last_inspection_date": iso_date(2021, 2026),
                "responsible_team": random.choice(TEAMS),
            },
            "geometry": geom,
        }
        features.append(feature)

    issue_plan = {
        3: {"asset_id": "WA-0002"},
        7: {"asset_id": ""},
        12: {"install_date": ""},
        18: {"install_date": "not-a-date"},
        23: {"install_date": "2032-05-01"},
        29: {"condition": ""},
        34: {"condition": "Excellent"},
        40: {"diameter_mm": -150},
        45: {"diameter_mm": "one hundred"},
        51: {"asset_type": "PIPE "},
        56: {"asset_type": "unknown fixture"},
        62: {"geometry": None},
        70: {"geometry": {"type": "LineString", "coordinates": [[176.25, -38.14]]}},
        78: {"operational_status": "active"},
        84: {"operational_status": "Retired"},
    }
    for idx, issues in issue_plan.items():
        for key, value in issues.items():
            if key == "geometry":
                features[idx]["geometry"] = value
            else:
                features[idx]["properties"][key] = value
    return {"type": "FeatureCollection", "features": features}


def generate_maintenance(asset_ids: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for i in range(1, 201):
        asset_id = random.choice(asset_ids)
        maint_date = date.fromisoformat(iso_date(2022, 2026))
        status = random.choices(WORK_STATUSES, weights=[12, 10, 72, 6])[0]
        completion = "" if status in {"Open", "In Progress"} else (maint_date + timedelta(days=random.randint(0, 20))).isoformat()
        labour_hours: float | str = round(random.uniform(1, 18), 1)
        labour_cost: float | str = round(float(labour_hours) * random.uniform(85, 135), 2)
        material_cost: float | str = round(random.uniform(0, 4500), 2)
        total_cost: float | str = round(float(labour_cost) + float(material_cost), 2)
        rows.append(
            {
                "work_order_id": f"WO-{i:05d}",
                "asset_id": asset_id,
                "maintenance_date": maint_date.isoformat(),
                "maintenance_type": random.choice(MAINT_TYPES),
                "description": f"{random.choice(MAINT_TYPES)} completed for asset {asset_id}",
                "priority": random.choices(PRIORITIES, weights=[32, 40, 20, 8])[0],
                "status": status,
                "contractor": random.choice(CONTRACTORS),
                "labour_hours": labour_hours,
                "material_cost": material_cost,
                "labour_cost": labour_cost,
                "total_cost": total_cost,
                "completion_date": completion,
            }
        )

    issues = {
        5: {"asset_id": "WA-9999"},
        11: {"work_order_id": "WO-00010"},
        17: {"asset_id": ""},
        24: {"maintenance_date": "31/31/2025"},
        33: {"completion_date": "2024-01-01", "maintenance_date": "2024-02-01"},
        41: {"material_cost": -300, "total_cost": -50},
        57: {"maintenance_type": "leak repair"},
        63: {"priority": ""},
        75: {"status": "Complete"},
        89: {"labour_hours": "two"},
        101: {"contractor": ""},
        116: {"total_cost": 99999},
        138: {"asset_id": "WA-8888"},
    }
    for idx, patch in issues.items():
        rows[idx].update(patch)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_mapping() -> None:
    rows = []
    for standard, variants in TYPE_VARIANTS.items():
        for variant in variants:
            rows.append({"source_asset_type": variant, "standard_asset_type": standard})
    write_csv(REF_DIR / "asset_type_mapping.csv", rows, ["source_asset_type", "standard_asset_type"])


def parse_date(value: Any) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def parse_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def clean_assets(asset_fc: dict[str, Any], area_fc: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, str]]:
    counts = Counter(f["properties"].get("asset_id") for f in asset_fc["features"] if f["properties"].get("asset_id"))
    clean: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    service_lookup: dict[str, str] = {}
    for index, feature in enumerate(asset_fc["features"], start=1):
        props = feature["properties"]
        asset_id = str(props.get("asset_id") or "").strip()
        reasons: list[str] = []
        std_type = standard_type(props.get("asset_type"))
        install = parse_date(props.get("install_date"))
        last_inspection = parse_date(props.get("last_inspection_date"))
        diameter = parse_float(props.get("diameter_mm"))
        lon, lat = asset_centroid(feature)
        geom = feature.get("geometry")
        if not asset_id:
            reasons.append("Missing asset_id")
        if asset_id and counts[asset_id] > 1:
            reasons.append("Duplicate asset_id")
        if not std_type:
            reasons.append("Unmapped asset_type")
        if not install:
            reasons.append("Invalid or missing install_date")
        elif install > date.today():
            reasons.append("Future install_date")
        if props.get("condition") not in CONDITIONS:
            reasons.append("Invalid or missing condition")
        if str(props.get("operational_status") or "").strip() not in STATUSES:
            reasons.append("Invalid operational_status")
        if diameter is None or diameter <= 0:
            reasons.append("Invalid diameter_mm")
        if not geom:
            reasons.append("Missing geometry")
        elif geom.get("type") == "LineString" and len(geom.get("coordinates", [])) < 2:
            reasons.append("Invalid LineString geometry")
        elif lon is None or lat is None:
            reasons.append("Invalid geometry coordinates")

        if reasons:
            rejected.append(
                {
                    "source_record_identifier": asset_id or f"water_assets_row_{index}",
                    "rejection_reason": "; ".join(reasons),
                    "source_file": "water_assets.geojson",
                    "rejected_timestamp": NOW.isoformat(),
                }
            )
            continue

        service_area = "Unassigned"
        for area in area_fc["features"]:
            ring = area["geometry"]["coordinates"][0]
            if lon is not None and lat is not None and point_in_polygon(lon, lat, ring):
                service_area = area["properties"]["service_area_name"]
                break
        service_lookup[asset_id] = service_area
        clean.append({"feature": feature, "standard_asset_type": std_type, "install": install, "diameter": diameter, "lon": lon, "lat": lat, "service_area": service_area})
    return clean, rejected, service_lookup


def valid_maintenance(rows: list[dict[str, Any]], valid_asset_ids: set[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    clean: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []
    counts = Counter(row["work_order_id"] for row in rows)
    for row in rows:
        asset_id = row.get("asset_id", "").strip()
        maint = parse_date(row.get("maintenance_date"))
        comp = parse_date(row.get("completion_date")) if row.get("completion_date") else None
        labour = parse_float(row.get("labour_cost"))
        material = parse_float(row.get("material_cost"))
        total = parse_float(row.get("total_cost"))
        critical_invalid = (
            counts[row["work_order_id"]] > 1
            or not asset_id
            or not maint
            or (comp is not None and comp < maint)
            or labour is None
            or material is None
            or total is None
            or labour < 0
            or material < 0
            or total < 0
        )
        if asset_id not in valid_asset_ids:
            unmatched.append({**row, "exception_reason": "Asset ID not found in cleaned asset dataset"})
            continue
        if critical_invalid:
            continue
        clean.append(row)
    return clean, unmatched


def reporting_dataset(clean_assets_rows: list[dict[str, Any]], maintenance_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_asset: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in maintenance_rows:
        by_asset[row["asset_id"]].append(row)
    report_rows: list[dict[str, Any]] = []
    for item in clean_assets_rows:
        props = item["feature"]["properties"]
        asset_id = props["asset_id"].strip()
        maint = by_asset.get(asset_id, [])
        dated = sorted(maint, key=lambda r: r["maintenance_date"], reverse=True)
        total_cost = round(sum(float(r["total_cost"]) for r in maint), 2)
        latest_date = dated[0]["maintenance_date"] if dated else ""
        latest_type = dated[0]["maintenance_type"] if dated else ""
        latest_dt = parse_date(latest_date)
        age = date.today().year - item["install"].year
        report_rows.append(
            {
                "asset_id": asset_id,
                "standard_asset_type": item["standard_asset_type"],
                "asset_subtype": props["asset_subtype"],
                "service_area": item["service_area"],
                "install_date": item["install"].isoformat(),
                "install_year": item["install"].year,
                "asset_age_years": age,
                "material": props["material"],
                "diameter_mm": int(item["diameter"]) if item["diameter"].is_integer() else item["diameter"],
                "condition": props["condition"],
                "operational_status": props["operational_status"].strip(),
                "last_inspection_date": props["last_inspection_date"],
                "latest_maintenance_date": latest_date,
                "latest_maintenance_type": latest_type,
                "maintenance_count": len(maint),
                "total_maintenance_cost": total_cost,
                "average_maintenance_cost": round(total_cost / len(maint), 2) if maint else 0,
                "open_work_order_count": sum(1 for r in maint if r["status"] in {"Open", "In Progress"}),
                "urgent_work_order_count": sum(1 for r in maint if r["priority"] == "Urgent"),
                "days_since_last_maintenance": (date.today() - latest_dt).days if latest_dt else "",
                "data_quality_flag": "Review" if item["service_area"] == "Unassigned" else "OK",
                "latitude": round(item["lat"], 6),
                "longitude": round(item["lon"], 6),
                "geometry_type": item["feature"]["geometry"]["type"],
                "etl_processed_timestamp": NOW.isoformat(),
            }
        )
    return report_rows


def data_quality_summary(total_assets: int, clean_assets_count: int, rejected: list[dict[str, Any]], maintenance: list[dict[str, Any]], unmatched: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reasons = " ".join(row["rejection_reason"] for row in rejected)
    duplicate_work_orders = len(maintenance) - len({r["work_order_id"] for r in maintenance})
    metrics = {
        "total_asset_records": total_assets,
        "valid_asset_records": clean_assets_count,
        "rejected_asset_records": len(rejected),
        "duplicate_asset_records": reasons.count("Duplicate asset_id"),
        "missing_asset_ids": reasons.count("Missing asset_id") + sum(1 for r in maintenance if not r["asset_id"].strip()),
        "invalid_dates": reasons.count("install_date") + sum(1 for r in maintenance if parse_date(r["maintenance_date"]) is None),
        "unmatched_maintenance_records": len(unmatched),
        "invalid_geometries": reasons.count("geometry"),
        "duplicate_work_orders": duplicate_work_orders,
        "total_validation_failures": len(rejected) + len(unmatched) + duplicate_work_orders,
    }
    return [{"metric": key, "value": value, "notes": "Generated mock validation metric"} for key, value in metrics.items()]


def main() -> None:
    random.seed(SEED)
    ensure_dirs()
    areas = service_areas()
    assets = generate_assets()
    asset_ids = [f["properties"]["asset_id"] for f in assets["features"] if f["properties"].get("asset_id")]
    maintenance = generate_maintenance(asset_ids)
    write_mapping()

    (RAW_DIR / "service_areas.geojson").write_text(json.dumps(areas, indent=2), encoding="utf-8")
    (RAW_DIR / "water_assets.geojson").write_text(json.dumps(assets, indent=2), encoding="utf-8")
    write_csv(
        RAW_DIR / "maintenance_records.csv",
        maintenance,
        [
            "work_order_id",
            "asset_id",
            "maintenance_date",
            "maintenance_type",
            "description",
            "priority",
            "status",
            "contractor",
            "labour_hours",
            "material_cost",
            "labour_cost",
            "total_cost",
            "completion_date",
        ],
    )

    clean_assets_rows, rejected, _service_lookup = clean_assets(assets, areas)
    clean_maint, unmatched = valid_maintenance(maintenance, {row["feature"]["properties"]["asset_id"].strip() for row in clean_assets_rows})
    report_rows = reporting_dataset(clean_assets_rows, clean_maint)
    write_csv(OUT_DIR / "asset_reporting_dataset.csv", report_rows, list(report_rows[0].keys()))
    write_csv(OUT_DIR / "rejected_assets.csv", rejected, ["source_record_identifier", "rejection_reason", "source_file", "rejected_timestamp"])
    write_csv(OUT_DIR / "unmatched_maintenance_records.csv", unmatched, list(unmatched[0].keys()))
    write_csv(OUT_DIR / "data_quality_summary.csv", data_quality_summary(len(assets["features"]), len(clean_assets_rows), rejected, maintenance, unmatched), ["metric", "value", "notes"])
    print(f"Generated {len(assets['features'])} assets, {len(maintenance)} work orders, and {len(report_rows)} reporting rows.")


if __name__ == "__main__":
    main()
