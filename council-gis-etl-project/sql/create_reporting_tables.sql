/*
Council Water Asset Maintenance Reporting Pipeline
Microsoft SQL Server reporting-layer table design.

This script is a simulation for interview practice. It assumes geometry is
stored as WKT text for portability; in production, SQL Server geography or
geometry columns may be preferred.
*/

CREATE TABLE dbo.cleaned_assets (
    asset_id                 varchar(30)   NOT NULL,
    standard_asset_type       varchar(50)   NOT NULL,
    asset_subtype             varchar(80)   NULL,
    service_area              varchar(50)   NULL,
    install_date              date          NOT NULL,
    material                  varchar(40)   NULL,
    diameter_mm               decimal(10,2) NOT NULL,
    condition                 varchar(20)   NOT NULL,
    operational_status        varchar(30)   NOT NULL,
    last_inspection_date      date          NULL,
    responsible_team          varchar(80)   NULL,
    latitude                  decimal(9,6)  NULL,
    longitude                 decimal(9,6)  NULL,
    geometry_type             varchar(30)   NOT NULL,
    geometry_wkt              nvarchar(max) NULL,
    etl_run_id                bigint        NULL,
    CONSTRAINT pk_cleaned_assets PRIMARY KEY (asset_id),
    CONSTRAINT ck_cleaned_assets_condition CHECK (condition IN ('Good', 'Fair', 'Poor', 'Critical')),
    CONSTRAINT ck_cleaned_assets_status CHECK (operational_status IN ('Active', 'Inactive', 'Planned', 'Under Repair')),
    CONSTRAINT ck_cleaned_assets_diameter CHECK (diameter_mm > 0),
    CONSTRAINT ck_cleaned_assets_install_date CHECK (install_date <= CAST(GETDATE() AS date))
);

CREATE TABLE dbo.maintenance_records_clean (
    work_order_id       varchar(30)    NOT NULL,
    asset_id            varchar(30)    NOT NULL,
    maintenance_date    date           NOT NULL,
    maintenance_type    varchar(60)    NOT NULL,
    description         nvarchar(500)  NULL,
    priority            varchar(20)    NOT NULL,
    status              varchar(30)    NOT NULL,
    contractor          varchar(100)   NULL,
    labour_hours        decimal(10,2)  NULL,
    material_cost       decimal(12,2)  NOT NULL DEFAULT 0,
    labour_cost         decimal(12,2)  NOT NULL DEFAULT 0,
    total_cost          decimal(12,2)  NOT NULL,
    completion_date     date           NULL,
    etl_run_id          bigint         NULL,
    CONSTRAINT pk_maintenance_records_clean PRIMARY KEY (work_order_id),
    CONSTRAINT fk_maintenance_asset FOREIGN KEY (asset_id) REFERENCES dbo.cleaned_assets(asset_id),
    CONSTRAINT ck_maintenance_priority CHECK (priority IN ('Low', 'Medium', 'High', 'Urgent')),
    CONSTRAINT ck_maintenance_status CHECK (status IN ('Open', 'In Progress', 'Completed', 'Cancelled')),
    CONSTRAINT ck_maintenance_costs CHECK (material_cost >= 0 AND labour_cost >= 0 AND total_cost >= 0),
    CONSTRAINT ck_maintenance_completion CHECK (completion_date IS NULL OR completion_date >= maintenance_date)
);

CREATE TABLE dbo.asset_reporting (
    asset_id                     varchar(30)    NOT NULL,
    standard_asset_type           varchar(50)    NOT NULL,
    asset_subtype                 varchar(80)    NULL,
    service_area                  varchar(50)    NULL,
    install_date                  date           NOT NULL,
    install_year                  int            NOT NULL,
    asset_age_years               int            NOT NULL,
    material                      varchar(40)    NULL,
    diameter_mm                   decimal(10,2)  NOT NULL,
    condition                     varchar(20)    NOT NULL,
    operational_status            varchar(30)    NOT NULL,
    last_inspection_date          date           NULL,
    latest_maintenance_date       date           NULL,
    latest_maintenance_type       varchar(60)    NULL,
    maintenance_count             int            NOT NULL,
    total_maintenance_cost        decimal(14,2)  NOT NULL,
    average_maintenance_cost      decimal(14,2)  NOT NULL,
    open_work_order_count         int            NOT NULL,
    urgent_work_order_count       int            NOT NULL,
    days_since_last_maintenance   int            NULL,
    data_quality_flag             varchar(30)    NOT NULL,
    latitude                      decimal(9,6)   NULL,
    longitude                     decimal(9,6)   NULL,
    geometry_type                 varchar(30)    NOT NULL,
    etl_processed_timestamp       datetime2(0)   NOT NULL,
    CONSTRAINT pk_asset_reporting PRIMARY KEY (asset_id)
);

CREATE TABLE dbo.rejected_records (
    rejected_record_id        bigint IDENTITY(1,1) NOT NULL,
    source_record_identifier  varchar(100)         NULL,
    rejection_reason          nvarchar(1000)       NOT NULL,
    source_file               varchar(200)         NOT NULL,
    rejected_timestamp        datetime2(0)         NOT NULL,
    raw_payload               nvarchar(max)        NULL,
    etl_run_id                bigint               NULL,
    CONSTRAINT pk_rejected_records PRIMARY KEY (rejected_record_id)
);

CREATE TABLE dbo.etl_run_log (
    etl_run_id             bigint IDENTITY(1,1) NOT NULL,
    workspace_name         varchar(200)         NOT NULL,
    start_time             datetime2(0)         NOT NULL,
    end_time               datetime2(0)         NULL,
    run_status             varchar(30)          NOT NULL,
    source_asset_count     int                  NULL,
    source_work_order_count int                 NULL,
    output_asset_count     int                  NULL,
    rejected_count         int                  NULL,
    unmatched_count        int                  NULL,
    message                nvarchar(1000)       NULL,
    CONSTRAINT pk_etl_run_log PRIMARY KEY (etl_run_id),
    CONSTRAINT ck_etl_run_status CHECK (run_status IN ('Started', 'Succeeded', 'Failed', 'Warning'))
);

CREATE INDEX ix_cleaned_assets_type_area ON dbo.cleaned_assets (standard_asset_type, service_area);
CREATE INDEX ix_cleaned_assets_condition ON dbo.cleaned_assets (condition);
CREATE INDEX ix_maintenance_asset_date ON dbo.maintenance_records_clean (asset_id, maintenance_date DESC);
CREATE INDEX ix_maintenance_status_priority ON dbo.maintenance_records_clean (status, priority);
CREATE INDEX ix_asset_reporting_area_condition ON dbo.asset_reporting (service_area, condition);
CREATE INDEX ix_rejected_records_etl_run ON dbo.rejected_records (etl_run_id);

