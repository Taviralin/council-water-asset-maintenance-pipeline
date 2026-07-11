# Interview Explanation

## 30-Second Summary

I had not previously used FME, so I built a small end-to-end project to understand how spatial and non-spatial data could be integrated for reporting. The project simulates council water assets in GeoJSON, maintenance work orders in CSV, service-area polygons, data-quality checks, an FME-style ETL workflow, SQL Server reporting tables, and a Power BI dashboard plan.

## 90-Second Explanation

This is a self-directed learning project based on a realistic council reporting scenario. A council may have GIS asset data for water pipes, hydrants, manholes, valves, and pumps, while maintenance work orders and costs sit in a separate operational system.

I created mock spatial and maintenance datasets, intentionally added realistic data-quality issues, and designed an ETL process that standardises fields, validates records, rejects bad assets, separates unmatched work orders, assigns assets to service areas using spatial overlay, aggregates maintenance history, and outputs an asset-level reporting dataset.

The project also includes SQL Server table designs, validation queries, a Power BI dashboard plan, and FME Form and FME Flow implementation guides. My aim was not to claim professional GIS or FME experience, but to show that I understand ETL principles and can learn a domain tool by building a clear, business-relevant pipeline.

## 2-Minute STAR Explanation

**Situation:** I was preparing for a Data and Reporting Officer interview where spatial data, reporting, and workflow automation could be relevant.

**Task:** I wanted to build a small project that demonstrated ETL thinking, data quality, GIS integration, SQL, and Power BI reporting without overstating my experience.

**Action:** I created a fictional council water asset maintenance pipeline. I generated GeoJSON assets around Rotorua, maintenance records, service-area polygons, and reference mapping. I documented how FME Form would read, clean, validate, spatially enrich, aggregate, and write the outputs. I also documented how FME Flow could schedule the process nightly, how SQL Server tables could store the results, and how Power BI could present KPIs such as poor or critical assets, maintenance cost, open work orders, and asset age.

**Result:** The project gives me a working example I can talk through in an interview. It shows that I understand how to move from messy source data to reporting-ready outputs, how to communicate data-quality issues, and how my existing SSIS and ETL background can transfer into FME.

## Likely Follow-Up Questions And Answers

### Why did you choose this project?

I chose it because it is close to the kind of reporting problem a council could face: combining GIS asset information with operational maintenance data so teams can make decisions using one trusted view.

### What business problem does it solve?

It helps infrastructure, asset management, finance, and reporting teams understand where assets are, what condition they are in, how much maintenance they require, and which service areas may need attention.

### What did you use FME Form for?

In this project, FME Form is the design tool for the ETL workflow. I would use it to read GeoJSON and CSV data, trim and standardise attributes, map source asset types, validate data quality, perform spatial overlay, aggregate maintenance records, and write reporting outputs.

### What did you use FME Flow for?

FME Flow would be used to automate and monitor the completed workspace. For example, the workflow could run every night at 2:00 am, write outputs, record logs, and alert someone if the job fails.

### What data-quality problems did you identify?

I included duplicate asset IDs, missing IDs, invalid dates, future install dates, missing geometry, invalid line geometry, inconsistent asset type values, invalid condition values, negative or text values in numeric fields, unmatched work orders, and total-cost reconciliation issues.

### What is the difference between a relational join and a spatial join?

A relational join matches records using common attribute values, such as `asset_id`. A spatial join uses location or geometry relationships, such as assigning an asset to a service-area polygon because the asset falls inside it.

### What was the most challenging part?

The most challenging part was thinking clearly about which records should be rejected, which should be routed to exception output, and which could still be used with a data-quality flag. That is important because not every issue should stop a reporting process, but critical issues must be visible.

### What would you improve in a production environment?

I would use real source-system connections, formal data-quality thresholds, audit logging, role-based access, automated notifications, version-controlled FME workspaces, test environments, stakeholder sign-off, and a proper Power BI semantic model with separate asset and maintenance tables.

### How would you ensure data accuracy?

I would agree validation rules with business owners, reconcile record counts, track rejects and exceptions, compare outputs with source-system totals, sample records with GIS and operations users, and monitor trends in data-quality failures after each scheduled run.

### How does your SSIS and ETL experience help you learn FME?

The concepts transfer well: readers are similar to sources, writers are similar to destinations, and transformers are similar to data-flow transformations. The important thinking is still about mapping, cleansing, validation, joins, error handling, and repeatable outputs.

### How would you work with a senior GIS Analyst?

I would ask them to confirm spatial assumptions, coordinate systems, service-area boundaries, geometry validation rules, and the correct spatial relationship to use. I would bring the ETL and reporting perspective, but rely on their GIS expertise for authoritative spatial decisions.

### What did you personally build and understand?

I built the mock data, validation scripts, SQL examples, documentation, FME workflow design, FME Flow deployment plan, and Power BI dashboard plan. I understand the purpose of each step and can explain how the data moves from raw source files to a reporting-ready dataset.

