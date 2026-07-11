# Data Dictionary

## `water_assets.geojson`

| Field | Business Definition | Data Type | Example | Mandatory | Validation Rule | Source System | Target Field |
|---|---|---|---|---|---|---|---|
| asset_id | Unique water asset identifier | Text | WA-0001 | Yes | Present and unique | GIS asset layer | asset_id |
| asset_type | Source asset category | Text | PIPE | Yes | Must map to standard type | GIS asset layer | standard_asset_type |
| asset_subtype | More specific asset class | Text | Distribution Main | No | Valid business text | GIS asset layer | asset_subtype |
| install_date | Date asset was installed | Date | 2008-04-19 | Yes | Valid date, not future | GIS asset layer | install_date |
| material | Main asset material | Text | PVC | No | Expected material list | GIS asset layer | material |
| diameter_mm | Asset diameter in millimetres | Number | 150 | Yes | Numeric and greater than zero | GIS asset layer | diameter_mm |
| condition | Current condition rating | Text | Fair | Yes | Good, Fair, Poor, Critical | GIS asset layer | condition |
| operational_status | Current operational status | Text | Active | Yes | Active, Inactive, Planned, Under Repair | GIS asset layer | operational_status |
| last_inspection_date | Most recent inspection date | Date | 2025-11-04 | No | Valid date | GIS asset layer | last_inspection_date |
| responsible_team | Team responsible for asset | Text | Water Networks | No | Valid business text | GIS asset layer | responsible_team |
| geometry | Asset spatial shape | Geometry | Point or LineString | Yes | Valid GeoJSON geometry | GIS asset layer | geometry_type, latitude, longitude |

## `maintenance_records.csv`

| Field | Business Definition | Data Type | Example | Mandatory | Validation Rule | Source System | Target Field |
|---|---|---|---|---|---|---|---|
| work_order_id | Unique maintenance work order | Text | WO-00001 | Yes | Present and unique | Maintenance system | work_order_id |
| asset_id | Asset referenced by work order | Text | WA-0001 | Yes | Must match cleaned asset | Maintenance system | asset_id |
| maintenance_date | Date work began or was recorded | Date | 2025-03-15 | Yes | Valid date | Maintenance system | latest_maintenance_date |
| maintenance_type | Type of maintenance activity | Text | Leak Repair | Yes | Expected activity list | Maintenance system | latest_maintenance_type |
| description | Work-order notes | Text | Leak repair completed | No | Free text | Maintenance system | Not directly reported |
| priority | Work priority | Text | High | Yes | Low, Medium, High, Urgent | Maintenance system | urgent_work_order_count |
| status | Work-order status | Text | Completed | Yes | Open, In Progress, Completed, Cancelled | Maintenance system | open_work_order_count |
| contractor | Contractor or internal crew | Text | Arawa Civil | No | Optional text | Maintenance system | Not directly reported |
| labour_hours | Labour hours spent | Number | 4.5 | No | Numeric and non-negative | Maintenance system | Not directly reported |
| material_cost | Material cost | Currency | 250.00 | Yes | Numeric and non-negative | Maintenance system | total_maintenance_cost |
| labour_cost | Labour cost | Currency | 480.00 | Yes | Numeric and non-negative | Maintenance system | total_maintenance_cost |
| total_cost | Total maintenance cost | Currency | 730.00 | Yes | Numeric, non-negative, reconciles to labour plus material | Maintenance system | total_maintenance_cost |
| completion_date | Date work was completed | Date | 2025-03-18 | No | Blank or after maintenance date | Maintenance system | Not directly reported |

## `service_areas.geojson`

| Field | Business Definition | Data Type | Example | Mandatory | Validation Rule | Source System | Target Field |
|---|---|---|---|---|---|---|---|
| service_area_id | Unique service area identifier | Text | SA02 | Yes | Present and unique | GIS service areas | Not directly reported |
| service_area_name | Service area name | Text | Central | Yes | Expected service-area name | GIS service areas | service_area |
| area_manager | Responsible manager | Text | James Patel | No | Valid business text | GIS service areas | Not directly reported |
| maintenance_target_days | Target response time | Number | 10 | No | Numeric and positive | GIS service areas | Not directly reported |
| geometry | Service area polygon | Geometry | Polygon | Yes | Valid polygon | GIS service areas | service_area spatial lookup |

## `asset_type_mapping.csv`

| Field | Business Definition | Data Type | Example | Mandatory | Validation Rule | Source System | Target Field |
|---|---|---|---|---|---|---|---|
| source_asset_type | Raw source asset type value | Text | water_pipe | Yes | Trimmed value should be unique enough for mapping | Reference data | Lookup key |
| standard_asset_type | Standard reporting asset type | Text | Water Pipe | Yes | Water Pipe, Hydrant, Manhole, Valve, Pump | Reference data | standard_asset_type |

## `asset_reporting_dataset.csv`

| Field | Business Definition | Data Type | Example | Mandatory | Validation Rule | Source System | Target Field |
|---|---|---|---|---|---|---|---|
| asset_id | Unique reporting asset identifier | Text | WA-0001 | Yes | Unique | ETL output | Power BI asset key |
| standard_asset_type | Standard asset category | Text | Water Pipe | Yes | Expected standard type | ETL output | Power BI category |
| asset_subtype | Detailed asset type | Text | Distribution Main | No | Valid text | ETL output | Power BI attribute |
| service_area | Assigned service area | Text | Central | Yes | Should not be blank | Spatial overlay | Power BI slicer |
| install_date | Date installed | Date | 2008-04-19 | Yes | Valid date | GIS asset layer | Power BI date |
| install_year | Year installed | Integer | 2008 | Yes | Derived from install date | ETL calculation | Power BI slicer |
| asset_age_years | Approximate asset age | Integer | 18 | Yes | Non-negative | ETL calculation | KPI |
| material | Asset material | Text | PVC | No | Expected material list | GIS asset layer | Power BI attribute |
| diameter_mm | Diameter in millimetres | Number | 150 | Yes | Positive number | GIS asset layer | Power BI attribute |
| condition | Condition rating | Text | Poor | Yes | Good, Fair, Poor, Critical | GIS asset layer | KPI and visuals |
| operational_status | Asset status | Text | Active | Yes | Expected status list | GIS asset layer | Slicer |
| last_inspection_date | Last inspection date | Date | 2025-11-04 | No | Valid date | GIS asset layer | Detail page |
| latest_maintenance_date | Most recent maintenance date | Date | 2026-01-12 | No | Valid date or blank | Maintenance aggregation | Detail page |
| latest_maintenance_type | Most recent maintenance type | Text | Inspection | No | Expected activity list | Maintenance aggregation | Detail page |
| maintenance_count | Number of valid work orders | Integer | 4 | Yes | Non-negative | Maintenance aggregation | KPI support |
| total_maintenance_cost | Total cost for asset | Currency | 3250.50 | Yes | Non-negative | Maintenance aggregation | KPI |
| average_maintenance_cost | Average work-order cost | Currency | 812.63 | Yes | Non-negative | Maintenance aggregation | KPI |
| open_work_order_count | Count of open or in-progress work | Integer | 1 | Yes | Non-negative | Maintenance aggregation | KPI |
| urgent_work_order_count | Count of urgent work orders | Integer | 0 | Yes | Non-negative | Maintenance aggregation | KPI |
| days_since_last_maintenance | Days from latest maintenance to ETL date | Integer | 94 | No | Non-negative or blank | ETL calculation | Risk analysis |
| data_quality_flag | Reporting quality indicator | Text | OK | Yes | OK or Review | ETL calculation | Filter |
| latitude | Representative latitude | Decimal | -38.136100 | Yes | Valid latitude | Geometry calculation | Map |
| longitude | Representative longitude | Decimal | 176.251100 | Yes | Valid longitude | Geometry calculation | Map |
| geometry_type | Source geometry type | Text | LineString | Yes | Point or LineString | GIS asset layer | Detail page |
| etl_processed_timestamp | ETL processing timestamp | DateTime | 2026-07-10T02:00:00Z | Yes | Valid timestamp | ETL runtime | Audit |

## Exception Outputs

| Dataset | Field | Business Definition | Data Type | Example | Mandatory | Validation Rule | Source System | Target Field |
|---|---|---|---|---|---|---|---|---|
| rejected_assets.csv | source_record_identifier | Asset ID or row identifier | Text | WA-0007 | Yes | Present | ETL validation | Reject audit |
| rejected_assets.csv | rejection_reason | Reason the record failed | Text | Missing asset_id | Yes | Present | ETL validation | Reject audit |
| rejected_assets.csv | source_file | File where record came from | Text | water_assets.geojson | Yes | Present | ETL validation | Reject audit |
| rejected_assets.csv | rejected_timestamp | Time rejected | DateTime | 2026-07-10T02:00:00Z | Yes | Valid timestamp | ETL runtime | Reject audit |
| unmatched_maintenance_records.csv | exception_reason | Why work order did not join | Text | Asset ID not found | Yes | Present | ETL validation | Exception audit |
| data_quality_summary.csv | metric | Quality metric name | Text | rejected_asset_records | Yes | Present | ETL validation | Quality summary |
| data_quality_summary.csv | value | Metric value | Number | 12 | Yes | Numeric | ETL validation | Quality summary |
| data_quality_summary.csv | notes | Metric note | Text | Generated mock validation metric | No | Optional | ETL validation | Quality summary |

