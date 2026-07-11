/*
Validation queries for the Council Water Asset Maintenance Reporting Pipeline.
Run these against staging or reporting tables after an ETL load.
*/

-- Duplicate asset IDs in a staging table.
SELECT asset_id, COUNT(*) AS record_count
FROM dbo.cleaned_assets
GROUP BY asset_id
HAVING COUNT(*) > 1;

-- Missing mandatory asset fields.
SELECT *
FROM dbo.cleaned_assets
WHERE asset_id IS NULL
   OR standard_asset_type IS NULL
   OR install_date IS NULL
   OR condition IS NULL
   OR operational_status IS NULL;

-- Invalid or future asset dates.
SELECT asset_id, install_date, last_inspection_date
FROM dbo.cleaned_assets
WHERE install_date > CAST(GETDATE() AS date)
   OR last_inspection_date > DATEADD(day, 7, CAST(GETDATE() AS date));

-- Negative or impossible maintenance costs.
SELECT work_order_id, material_cost, labour_cost, total_cost
FROM dbo.maintenance_records_clean
WHERE material_cost < 0
   OR labour_cost < 0
   OR total_cost < 0;

-- Maintenance records whose asset ID does not exist in cleaned assets.
SELECT m.work_order_id, m.asset_id
FROM dbo.maintenance_records_clean AS m
LEFT JOIN dbo.cleaned_assets AS a
    ON a.asset_id = m.asset_id
WHERE a.asset_id IS NULL;

-- Invalid condition values.
SELECT asset_id, condition
FROM dbo.cleaned_assets
WHERE condition NOT IN ('Good', 'Fair', 'Poor', 'Critical');

-- Invalid operational status values.
SELECT asset_id, operational_status
FROM dbo.cleaned_assets
WHERE operational_status NOT IN ('Active', 'Inactive', 'Planned', 'Under Repair');

-- Completion dates before maintenance dates.
SELECT work_order_id, maintenance_date, completion_date
FROM dbo.maintenance_records_clean
WHERE completion_date IS NOT NULL
  AND completion_date < maintenance_date;

-- Total cost reconciliation outside a small rounding tolerance.
SELECT work_order_id, material_cost, labour_cost, total_cost
FROM dbo.maintenance_records_clean
WHERE ABS(total_cost - (material_cost + labour_cost)) > 0.05;

-- Reporting records not assigned to a service area.
SELECT asset_id, standard_asset_type, latitude, longitude
FROM dbo.asset_reporting
WHERE service_area IS NULL
   OR service_area = ''
   OR service_area = 'Unassigned';

-- Asset records missing geometry coordinates for map reporting.
SELECT asset_id, latitude, longitude, geometry_type
FROM dbo.cleaned_assets
WHERE latitude IS NULL
   OR longitude IS NULL
   OR geometry_type IS NULL;

