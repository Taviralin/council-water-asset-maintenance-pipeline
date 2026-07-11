# Power BI Dashboard Plan

# Council Water Asset Maintenance Overview

## Purpose

The dashboard gives council users a one-page overview of water asset condition, maintenance demand, cost, and service-area risk.

## KPI Cards

| KPI | Column or Measure | Purpose |
|---|---|---|
| Total Assets | `Total Assets` | Size of the reporting asset base. |
| Assets in Poor or Critical Condition | `Poor or Critical Assets` | Highlights renewal and risk pressure. |
| Total Maintenance Cost | `Total Maintenance Cost` | Shows maintenance spend. |
| Open Work Orders | `Open Work Orders` | Shows current operational workload. |
| Urgent Work Orders | `Urgent Work Orders` | Shows high-priority demand. |
| Average Asset Age | `Average Asset Age` | Provides lifecycle context. |

## Recommended Visuals

| Visual | Columns | Use |
|---|---|---|
| Stacked bar: asset condition by service area | `service_area`, `condition`, `asset_id` count | Compare condition profile across service areas. |
| Line chart: maintenance cost trend by month | `latest_maintenance_date` or maintenance fact month, `total_maintenance_cost` | Identify cost trends and spikes. |
| Donut or bar: assets by type | `standard_asset_type`, `asset_id` count | Show asset mix. |
| Bar: open work orders by priority | `priority`, open work-order count from maintenance table | Prioritise operational follow-up. |
| Table: top assets by maintenance cost | `asset_id`, `standard_asset_type`, `service_area`, `total_maintenance_cost`, `maintenance_count` | Identify high-cost assets. |
| Map: asset locations | `latitude`, `longitude`, `standard_asset_type`, `condition` | Show spatial distribution. |
| Table: high-risk assets | `asset_id`, `condition`, `service_area`, `asset_age_years`, `open_work_order_count` | Focus on poor or critical assets with open work. |

## Filters And Slicers

- Service area
- Standard asset type
- Condition
- Operational status
- Material
- Install year range
- Data quality flag

## Drill Through

Create an asset detail page using `asset_id` as the drill-through field. Include asset attributes, service area, location, condition, maintenance count, latest maintenance date, total maintenance cost, and open work orders.

## Questions The Dashboard Answers

- How many water assets are in poor or critical condition?
- Which service areas have the highest risk profile?
- Which asset types drive maintenance cost?
- Where are urgent open work orders located?
- Which assets have repeated or expensive maintenance history?
- Are there assets with stale maintenance activity?

## Example DAX Measures

```DAX
Total Assets =
DISTINCTCOUNT(asset_reporting[asset_id])

Total Maintenance Cost =
SUM(asset_reporting[total_maintenance_cost])

Poor or Critical Assets =
CALCULATE(
    [Total Assets],
    asset_reporting[condition] IN { "Poor", "Critical" }
)

Open Work Orders =
SUM(asset_reporting[open_work_order_count])

Urgent Work Orders =
SUM(asset_reporting[urgent_work_order_count])

Average Asset Age =
AVERAGE(asset_reporting[asset_age_years])

Percentage of Assets in Poor or Critical Condition =
DIVIDE([Poor or Critical Assets], [Total Assets])

Average Maintenance Cost per Asset =
DIVIDE([Total Maintenance Cost], [Total Assets])
```

For a production semantic model, keep maintenance records as a separate fact table and relate them to the asset dimension by `asset_id`.

