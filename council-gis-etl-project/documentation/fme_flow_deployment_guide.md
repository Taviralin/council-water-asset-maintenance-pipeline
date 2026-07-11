# FME Flow Deployment Guide

## FME Form Versus FME Flow

FME Form is the desktop authoring tool. You use it to build, run, debug, and save the workspace.

FME Flow is the server automation platform. You use it to publish the finished workspace, schedule jobs, monitor runs, manage resources, and notify people when something fails.

## Deployment Scenario

The council reporting pipeline runs every night at 2:00 am. It reads updated source files, writes reporting outputs, and leaves logs and exception files for review.

## Step 1: Prepare The Workspace In FME Form

- Confirm all readers use paths that can be recreated on FME Flow.
- Use published parameters for source and destination folders.
- Run the workspace locally against the mock files.
- Confirm the four expected outputs are produced.
- Save the workspace with a clear version name, for example `CouncilWaterAssetReporting_v1.fmw`.

## Step 2: Create A Repository In FME Flow

- Sign in to FME Flow.
- Go to Repositories.
- Create a repository such as `CouncilWaterAssets`.
- Use repositories to group related workspaces, resources, and versions.

## Step 3: Publish The Workspace

- In FME Form, choose Publish to FME Flow.
- Select the `CouncilWaterAssets` repository.
- Upload the workspace.
- Include any custom resources required by the workspace.
- Check that published parameters appear in FME Flow.

## Step 4: Upload Project Resources

Upload or place these files where FME Flow can access them:

- `water_assets.geojson`
- `maintenance_records.csv`
- `service_areas.geojson`
- `asset_type_mapping.csv`

For a simple demo, use FME Flow Resources. In production, the files may come from network folders, databases, APIs, or GIS services.

## Step 5: Configure Paths

Use published parameters such as:

- `SOURCE_ASSET_PATH`
- `SOURCE_MAINTENANCE_PATH`
- `SOURCE_SERVICE_AREA_PATH`
- `REFERENCE_MAPPING_PATH`
- `OUTPUT_FOLDER`

This avoids hard-coding local desktop paths that will not exist on the server.

## Step 6: Run Manually

- Open the workspace in FME Flow.
- Enter or confirm the parameter values.
- Run the job.
- Review output files and job logs.

Manual runs are useful before enabling a schedule and when rerunning after a source-data fix.

## Step 7: Create A 2:00 AM Schedule

- Go to Schedules.
- Create a new schedule.
- Choose the published workspace.
- Set frequency to daily.
- Set time to 2:00 am.
- Confirm the server timezone.
- Save and enable the schedule.

## Step 8: Monitor Job Status

Use the Jobs page to check:

- Running jobs
- Completed jobs
- Failed jobs
- Queued jobs
- Runtime duration
- Log messages

For this project, a successful job should create the reporting dataset, rejected asset output, unmatched maintenance output, and data-quality summary.

## Step 9: Read Job Logs

Job logs help answer:

- Did each reader find its source file?
- How many records were read?
- How many records were rejected?
- Did any writer fail?
- Did the workspace finish successfully?

In a real support process, logs should be reviewed after failures and sampled after successful scheduled runs.

## Step 10: Identify Failed Jobs

Common failure causes:

- Missing source file
- Invalid file path
- Permission issue
- Database connection failure
- Schema change
- Unexpected nulls or data type changes

The workspace should fail clearly when required source files are missing, rather than producing silent incomplete output.

## Step 11: Notifications

Conceptually, configure email or notification alerts for:

- Job failure
- Repeated warnings
- Output row count below an agreed threshold
- Rejected records above an agreed threshold

Notification setup depends on the organisation's mail server, FME Flow configuration, and support process.

## Step 12: Rerun A Failed Job

- Fix the source file, path, permission, or database issue.
- Open the failed job details.
- Rerun with the same parameters, or start a new manual run.
- Confirm the output was replaced or versioned according to the agreed process.

## Step 13: Manage Workspace Versions

Recommended approach:

- Keep a version number in the workspace name or repository notes.
- Record changes in a short change log.
- Test in a non-production repository first.
- Promote only tested versions to the scheduled production job.
- Keep at least one known-good previous version for rollback.

## Power BI Refresh Support

FME Flow can refresh the reporting data files or SQL Server tables that Power BI reads from. It does not automatically refresh a Power BI report unless a separate integration is configured.

Possible approaches:

- CSV output: Power BI Service may need files in SharePoint, OneDrive, or another supported location.
- SQL Server output: Power BI Service usually needs an on-premises data gateway if SQL Server is not cloud-accessible.
- Separate schedule: Power BI Service can have its own refresh schedule after the 2:00 am FME job.
- API integration: a Power BI REST API refresh can be triggered, but this requires tenant permissions, authentication, and explicit configuration.

Practical interview explanation: FME Flow prepares and monitors the data pipeline; Power BI refresh is a related but separately configured reporting step.

