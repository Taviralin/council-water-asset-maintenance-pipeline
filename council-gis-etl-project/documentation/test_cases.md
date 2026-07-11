# Test Cases

| Test Case ID | Scenario | Input | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|
| TC-001 | Valid asset accepted | Asset with unique ID, valid dates, valid geometry, valid type | Asset appears in `asset_reporting_dataset.csv` | TBD | TBD |
| TC-002 | Duplicate asset rejected | Two assets with same `asset_id` | Duplicate asset records appear in `rejected_assets.csv` | TBD | TBD |
| TC-003 | Missing asset ID rejected | Asset with blank `asset_id` | Asset appears in `rejected_assets.csv` with missing ID reason | TBD | TBD |
| TC-004 | Invalid date rejected | Asset with `install_date = not-a-date` | Asset rejected with invalid date reason | TBD | TBD |
| TC-005 | Unmatched maintenance exception | Work order references `WA-9999` | Work order appears in `unmatched_maintenance_records.csv` | TBD | TBD |
| TC-006 | Invalid geometry rejected | LineString with fewer than two points | Asset rejected with geometry reason | TBD | TBD |
| TC-007 | Asset assigned to service area | Asset coordinates inside Central polygon | Reporting row has `service_area = Central` | TBD | TBD |
| TC-008 | Maintenance aggregation | Multiple valid work orders for one asset | Maintenance count and total cost match source records | TBD | TBD |
| TC-009 | Total cost calculated correctly | Labour cost 100 and material cost 50 | Expected total cost is 150 | TBD | TBD |
| TC-010 | Final output count reconciled | Total asset records minus rejected assets | Reporting row count equals valid asset count | TBD | TBD |
| TC-011 | Workflow succeeds with valid files | All source files present and readable | FME job succeeds and writers produce outputs | TBD | TBD |
| TC-012 | Missing required source file | Remove or rename `maintenance_records.csv` | Workflow fails clearly with missing file message | TBD | TBD |

Use the Python validation script for automated checks, then use this table for interview discussion or manual FME testing evidence.

