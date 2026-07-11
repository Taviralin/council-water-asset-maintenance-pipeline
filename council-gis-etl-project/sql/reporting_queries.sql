/*
Example reporting queries for Power BI, ad hoc analysis, and interview demos.
*/

-- Total assets by type.
SELECT standard_asset_type, COUNT(*) AS total_assets
FROM dbo.asset_reporting
GROUP BY standard_asset_type
ORDER BY total_assets DESC;

-- Assets by condition.
SELECT condition, COUNT(*) AS asset_count
FROM dbo.asset_reporting
GROUP BY condition
ORDER BY CASE condition WHEN 'Critical' THEN 1 WHEN 'Poor' THEN 2 WHEN 'Fair' THEN 3 ELSE 4 END;

-- Poor and critical assets by service area.
SELECT service_area, condition, COUNT(*) AS asset_count
FROM dbo.asset_reporting
WHERE condition IN ('Poor', 'Critical')
GROUP BY service_area, condition
ORDER BY service_area, condition;

-- Maintenance cost by month.
SELECT
    DATEFROMPARTS(YEAR(maintenance_date), MONTH(maintenance_date), 1) AS maintenance_month,
    SUM(total_cost) AS total_maintenance_cost
FROM dbo.maintenance_records_clean
GROUP BY DATEFROMPARTS(YEAR(maintenance_date), MONTH(maintenance_date), 1)
ORDER BY maintenance_month;

-- Maintenance cost by service area.
SELECT a.service_area, SUM(m.total_cost) AS total_maintenance_cost
FROM dbo.maintenance_records_clean AS m
INNER JOIN dbo.cleaned_assets AS a
    ON a.asset_id = m.asset_id
GROUP BY a.service_area
ORDER BY total_maintenance_cost DESC;

-- Assets with no maintenance in the last 12 months.
SELECT asset_id, standard_asset_type, service_area, latest_maintenance_date
FROM dbo.asset_reporting
WHERE latest_maintenance_date IS NULL
   OR latest_maintenance_date < DATEADD(month, -12, CAST(GETDATE() AS date))
ORDER BY latest_maintenance_date;

-- Urgent open work orders.
SELECT work_order_id, asset_id, maintenance_date, maintenance_type, priority, status, contractor
FROM dbo.maintenance_records_clean
WHERE priority = 'Urgent'
  AND status IN ('Open', 'In Progress')
ORDER BY maintenance_date;

-- Oldest assets.
SELECT TOP (20) asset_id, standard_asset_type, service_area, install_date, asset_age_years, condition
FROM dbo.asset_reporting
ORDER BY asset_age_years DESC;

-- Highest-cost assets.
SELECT TOP (20) asset_id, standard_asset_type, service_area, maintenance_count, total_maintenance_cost
FROM dbo.asset_reporting
ORDER BY total_maintenance_cost DESC;

-- Maintenance frequency by asset type.
SELECT
    standard_asset_type,
    COUNT(*) AS asset_count,
    SUM(maintenance_count) AS total_work_orders,
    AVG(CAST(maintenance_count AS decimal(10,2))) AS average_work_orders_per_asset
FROM dbo.asset_reporting
GROUP BY standard_asset_type
ORDER BY average_work_orders_per_asset DESC;

