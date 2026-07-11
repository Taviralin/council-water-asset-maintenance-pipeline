# FME Form Build Guide

## Goal

Build an FME Form workspace that reads GIS assets, service-area polygons, reference mapping, and maintenance records, then produces reporting-ready outputs for Power BI or SQL Server.

Assumption: you are new to FME. FME Form is the desktop design tool where you build and test the workflow.

## Workspace Diagram

```text
GeoJSON Reader: water_assets
    -> AttributeManager
    -> AttributeTrimmer
    -> StringCaseChanger
    -> ValueMapper: standard asset type
    -> DuplicateFilter
    -> DateTimeConverter
    -> Tester: mandatory/date/numeric rules
    -> GeometryValidator
        -> Valid Assets
            -> PointOnAreaOverlayer <- GeoJSON Reader: service_areas
            -> FeatureJoiner <- Aggregated Maintenance Data
            -> AttributeCreator / AttributeManager
            -> CSV Writer: asset_reporting_dataset.csv
        -> Invalid / Failed
            -> CSV Writer: rejected_assets.csv

CSV Reader: maintenance_records
    -> AttributeTrimmer
    -> StringCaseChanger
    -> DateTimeConverter
    -> Tester: maintenance quality rules
    -> FeatureJoiner with valid asset IDs
        -> Matched
            -> StatisticsCalculator / Aggregator
            -> Sorter
            -> Sampler: latest maintenance record
        -> Unjoined
            -> CSV Writer: unmatched_maintenance_records.csv

CSV Writer: data_quality_summary.csv
Optional Microsoft SQL Server Writer: cleaned and reporting tables
```

## Step 1: Add Readers

### GeoJSON Reader: `water_assets.geojson`

Why: reads the spatial asset layer, including points and lines.

Important configuration:

- Format: GeoJSON
- Dataset: `data/raw/water_assets.geojson`
- Feature type: water assets

Input ports: none because it starts the workflow.

Output ports: one feature stream containing asset attributes and geometry.

Business problem solved: brings GIS asset data into the ETL process.

### CSV Reader: `maintenance_records.csv`

Why: reads operational work-order records.

Important configuration:

- Format: CSV
- Dataset: `data/raw/maintenance_records.csv`
- Confirm header row is enabled.

Output ports: maintenance records.

Business problem solved: brings non-spatial maintenance data into the workflow.

### GeoJSON Reader: `service_areas.geojson`

Why: reads polygon boundaries used to assign assets to service areas.

Important configuration:

- Format: GeoJSON
- Dataset: `data/raw/service_areas.geojson`

Business problem solved: adds the spatial context needed for service-area reporting.

### CSV Reader: `asset_type_mapping.csv`

Why: reads the reference table for standardising inconsistent asset type values.

Important configuration:

- Format: CSV
- Dataset: `data/reference/asset_type_mapping.csv`

Business problem solved: turns values like `PIPE`, `pipe`, and `WaterPipe` into `Water Pipe`.

## Step 2: Standardise Asset Attributes

### AttributeManager

Why: renames, keeps, removes, and creates attributes in one place.

Important configuration:

- Keep fields required for reporting.
- Rename fields if source names are inconsistent.
- Create working fields such as `source_record_identifier`.

Input ports: asset features.

Output ports: cleaned attribute stream.

Business problem solved: makes the rest of the workspace easier to read and maintain.

### AttributeTrimmer

Why: removes leading and trailing spaces.

Important configuration:

- Apply to key text fields: `asset_id`, `asset_type`, `condition`, `operational_status`, `material`.

Input ports: attributes with possible whitespace.

Output ports: trimmed attributes.

Business problem solved: prevents false duplicates and failed lookups caused by hidden spaces.

### StringCaseChanger

Why: standardises text casing where exact values matter.

Important configuration:

- Convert comparison fields to a consistent case in temporary working attributes.
- Keep final display fields in business-friendly title case.

Input ports: trimmed attributes.

Output ports: case-standardised attributes.

Business problem solved: treats `active`, `Active`, and `ACTIVE` consistently during validation.

### ValueMapper

Why: maps source asset type variants to standard asset types.

Important configuration:

- Source attribute: trimmed asset type.
- Mapping source: values from `asset_type_mapping.csv` or manually entered pairs.
- Destination attribute: `standard_asset_type`.
- Unmapped values should be sent for rejection or review.

Input ports: asset features.

Output ports: mapped features.

Business problem solved: creates consistent categories for reporting.

## Step 3: Validate Assets

### DuplicateFilter

Why: detects duplicate asset IDs.

Important configuration:

- Key attribute: `asset_id`.
- Treat blank IDs separately with a Tester before or after this step.

Input ports: mapped asset features.

Output ports:

- `Unique`: first valid occurrence.
- `Duplicate`: duplicate records.

Business problem solved: protects the reporting layer from double-counted assets.

### DateTimeConverter

Why: parses dates into consistent date values.

Important configuration:

- Convert `install_date` and `last_inspection_date`.
- Expected input format: ISO date where possible.
- Failed conversions should be flagged.

Input ports: asset records.

Output ports: converted features, with failed conversions available for testing.

Business problem solved: makes date calculations reliable.

### Tester

Why: applies business validation rules.

Important configuration:

- `asset_id` is not empty.
- `standard_asset_type` is not empty.
- `install_date` is valid and not future dated.
- `condition` is one of Good, Fair, Poor, Critical.
- `operational_status` is one of Active, Inactive, Planned, Under Repair.
- `diameter_mm` is numeric and greater than zero.

Input ports: asset features.

Output ports:

- `Passed`: valid business rules.
- `Failed`: rejected asset records.

Business problem solved: separates usable records from records that need correction.

### GeometryValidator

Why: checks whether geometries are valid enough for spatial processing.

Important configuration:

- Validate points and lines.
- Repair simple issues only if the business accepts automatic repair.
- Send failed geometries to the rejected output.

Input ports: features with geometry.

Output ports:

- `Valid`: can continue to spatial overlay.
- `Invalid`: rejected with geometry reason.

Business problem solved: prevents spatial joins from producing misleading results.

## Step 4: Prepare Maintenance Records

### AttributeTrimmer And StringCaseChanger

Use these for `work_order_id`, `asset_id`, `maintenance_type`, `priority`, `status`, and `contractor`.

Business problem solved: consistent operational values before validation and joins.

### DateTimeConverter

Convert `maintenance_date` and `completion_date`.

Business problem solved: supports latest-maintenance calculations and checks completion dates.

### Tester

Validate:

- Work order ID is present.
- Asset ID is present.
- Maintenance date is valid.
- Completion date is blank or after maintenance date.
- Costs and labour hours are numeric and non-negative.
- Priority and status are valid.

Failed records can be written to an exception file or excluded from aggregation, depending on the severity.

## Step 5: Join Maintenance To Assets

### FeatureJoiner Or FeatureMerger

Why: joins maintenance records to valid asset IDs.

Important configuration:

- Left/requestor: maintenance records.
- Right/supplier: valid assets.
- Join key: `asset_id`.

Input ports:

- Maintenance features.
- Valid asset features.

Output ports:

- `Joined`: maintenance records that reference valid assets.
- `UnjoinedLeft` or equivalent: unmatched maintenance records.

Business problem solved: detects work orders that cannot be trusted for asset-level reporting.

## Step 6: Aggregate Maintenance

### StatisticsCalculator Or Aggregator

Why: summarises many maintenance records into one row per asset.

Important configuration:

- Group by: `asset_id`.
- Count: work orders.
- Sum: `total_cost`.
- Average: `total_cost`.
- Count open statuses and urgent priorities using conditional attributes before aggregation.

Input ports: matched maintenance records.

Output ports: asset-level maintenance summary.

Business problem solved: converts transactional maintenance history into dashboard metrics.

### Sorter And Sampler

Why: finds the latest maintenance record per asset.

Important configuration:

- Sort by `asset_id`, then `maintenance_date` descending.
- Sample first record per `asset_id`.

Business problem solved: captures latest maintenance date and latest maintenance type.

## Step 7: Assign Service Area

### PointOnAreaOverlayer Or SpatialFilter

Why: assigns each asset to the polygon it falls inside.

Important configuration:

- Area input: service-area polygons.
- Point or representative asset input: asset point or line midpoint/centroid.
- Transfer `service_area_name` to the asset.

Input ports:

- Asset features.
- Service-area polygons.

Output ports:

- Overlaid/matched features.
- Unmatched assets if outside all polygons.

Business problem solved: enables reporting by service area.

For line assets, create a representative point first using a centre-point transformer or use a spatial relationship appropriate for line-on-area overlay.

## Step 8: Create Reporting Fields

### AttributeCreator Or AttributeManager

Create:

- `install_year`
- `asset_age_years`
- `days_since_last_maintenance`
- `data_quality_flag`
- `etl_processed_timestamp`
- `latitude`
- `longitude`
- `geometry_type`

Business problem solved: produces a clean, analyst-friendly reporting dataset.

## Step 9: Write Outputs

### CSV Writer

Create four feature types:

- `asset_reporting_dataset.csv`
- `rejected_assets.csv`
- `unmatched_maintenance_records.csv`
- `data_quality_summary.csv`

Business problem solved: gives Power BI and business users simple files to inspect.

### Microsoft SQL Server Writer Optional Extension

Why: writes the same outputs into database tables.

Important configuration:

- Connection: SQL Server database.
- Tables: `cleaned_assets`, `maintenance_records_clean`, `asset_reporting`, `rejected_records`, `etl_run_log`.
- Use truncate-and-load for a small demo, or incremental load in production.

Business problem solved: supports governed reporting and scheduled refresh.

## Step 10: Build Rejection Reasons

Before each failed output, use AttributeCreator to populate:

- `source_record_identifier`
- `rejection_reason`
- `source_file`
- `rejected_timestamp`

This is important because a reject file without reasons is difficult for business users to fix.

