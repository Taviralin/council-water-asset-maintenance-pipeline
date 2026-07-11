# Business Requirements

## Project Background

Rotorua-style council water assets are represented in a GIS asset layer, while operational maintenance activity is represented in a separate work-order dataset. This project simulates how those datasets can be integrated into a reporting-ready layer for management reporting and Power BI.

This is a self-directed learning project and does not represent Rotorua Lakes Council's actual systems or data.

## Business Problem

Infrastructure teams need a single view of water assets, their location, condition, maintenance history, open work, and cost. When spatial data and operational data are separate, reporting can be slow, inconsistent, and difficult to validate.

## Objectives

- Integrate spatial assets with non-spatial maintenance records.
- Standardise asset type, status, condition, date, and numeric fields.
- Detect rejected assets and unmatched maintenance records.
- Assign assets to service areas through a spatial relationship.
- Aggregate maintenance history to asset level.
- Produce CSV or SQL Server reporting tables suitable for Power BI.
- Document a workflow that could be built in FME Form and automated in FME Flow.

## Stakeholders

- Infrastructure Operations
- Asset Management
- Data and Insights
- Finance
- Service Delivery
- GIS Team
- Reporting and Management

## Source Systems

- GIS asset system: simulated by `water_assets.geojson`
- Operational maintenance system: simulated by `maintenance_records.csv`
- GIS service area layer: simulated by `service_areas.geojson`
- Reference data: simulated by `asset_type_mapping.csv`

## Scope

- Water pipes, hydrants, manholes, valves, and pumps.
- Basic data cleansing and validation.
- Asset-level reporting output.
- Exception outputs for rejected assets and unmatched maintenance records.
- SQL Server table design and reporting query examples.
- Power BI dashboard plan.

## Out Of Scope

- Live council system integration.
- Advanced hydraulic modelling or network tracing.
- Machine learning.
- Complex cloud infrastructure.
- Real-time streaming.
- Production security design.
- Claims about Rotorua Lakes Council's internal architecture.

## Business Rules

- Each valid asset must have a unique asset ID.
- Asset type must map to a standard asset type.
- Install dates must be valid and not in the future.
- Diameter must be numeric and greater than zero.
- Condition must be Good, Fair, Poor, or Critical.
- Operational status must be Active, Inactive, Planned, or Under Repair.
- Asset geometry must exist and be valid enough for reporting.
- Maintenance records must reference a valid cleaned asset to be included in asset reporting.
- Service area is assigned using the asset point or asset line centroid.

## Data-Quality Requirements

- Rejected asset records must include a rejection reason.
- Unmatched maintenance records must be separated into an exception output.
- Data-quality metrics must be produced for reconciliation.
- The final reporting dataset must contain one row per valid asset.

## Refresh Frequency

The simulated production schedule is nightly at 2:00 am. Manual runs should also be possible for testing and recovery.

## Expected Outputs

- `asset_reporting_dataset.csv`
- `rejected_assets.csv`
- `unmatched_maintenance_records.csv`
- `data_quality_summary.csv`
- Optional SQL Server tables for cleaned assets, clean maintenance records, reporting output, rejects, and ETL run logs.

## Success Criteria

- Source files can be regenerated consistently.
- The reporting output validates with no critical failures.
- The workflow can be explained clearly to a non-technical stakeholder.
- The project demonstrates ETL, spatial integration, automation thinking, and Power BI reporting design.

## Risks And Assumptions

- Mock data is simplified and fictional.
- Spatial polygons are illustrative service areas, not official boundaries.
- FME and Power BI steps are documented for manual build, not executed automatically by this repository.
- Production deployment would require access controls, environment configuration, monitoring, and stakeholder sign-off.

