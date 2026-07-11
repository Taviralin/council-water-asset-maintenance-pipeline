# Council Water Asset Maintenance Reporting Pipeline

A self-directed data integration and reporting project simulating how a local council could combine GIS water asset data with operational maintenance records to create a reporting-ready dataset and Power BI dashboard.

This project uses fictional data only. It does not represent Rotorua Lakes Council's actual systems, data, or internal architecture.

## Project Purpose

The project was created as interview preparation for a Data & Reporting Officer role. It demonstrates practical understanding of:

- ETL pipeline design
- spatial and non-spatial data integration
- data cleaning and validation
- rejected records and exception handling
- referential integrity checks
- relational joins
- simplified spatial joins
- maintenance aggregation
- reporting-ready dataset design
- Power BI dashboarding
- documentation and business communication

## Business Scenario

A local council manages water infrastructure assets such as:

- water pipes
- hydrants
- valves
- manholes
- pumps

Spatial asset information is stored in a GIS-style asset register, while maintenance records, work orders, asset condition information, and maintenance costs are stored in a separate operational dataset.

The aim is to integrate these sources into a clean asset-level reporting dataset that can support operational reporting and Power BI dashboarding.

## Implementation Note

The original project was designed around FME Form and FME Flow concepts. However, local FME Form installation was blocked by Windows permission issues involving protected shared DLL files.

To continue the project, the ETL workflow was implemented in Databricks Free Edition. The same integration concepts were still demonstrated:

- data ingestion
- cleaning
- validation
- rejected records
- unmatched records
- relational joins
- simplified spatial joins
- aggregation
- reporting outputs
- Power BI dashboarding

The FME documentation remains included as a design reference for how the same workflow could be implemented using FME readers, transformers, writers, and FME Flow scheduling.

## Architecture

```mermaid
flowchart TD
    A[GIS Asset Data<br/>water_assets.geojson]
    B[Maintenance Data<br/>maintenance_records.csv]
    C[Service Area Polygons<br/>service_areas.geojson]
    D[Asset Type Reference Mapping<br/>asset_type_mapping.csv]

    A --> E[Databricks ETL Notebook]
    B --> E
    C --> E
    D --> E

    E --> F[Cleaning and Validation]
    F --> G[Rejected Records]
    F --> H[Referential Integrity Checks]
    H --> I[Unmatched Maintenance Records]
    H --> J[Maintenance Aggregation]
    J --> K[Asset-Level Reporting Dataset]
    K --> L[Power BI Dashboard]
