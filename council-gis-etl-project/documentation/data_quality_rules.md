# Data Quality Rules

| Rule ID | Area | Rule | Handling |
|---|---|---|---|
| DQ-001 | Asset ID | `asset_id` must be present. | Reject asset. |
| DQ-002 | Asset ID | `asset_id` must be unique after trimming. | Reject duplicate assets. |
| DQ-003 | Asset type | Source asset type must map to a standard type. | Reject asset or send for reference mapping update. |
| DQ-004 | Install date | `install_date` must parse as a date. | Reject asset. |
| DQ-005 | Install date | `install_date` must not be in the future. | Reject asset. |
| DQ-006 | Condition | Condition must be Good, Fair, Poor, or Critical. | Reject asset. |
| DQ-007 | Operational status | Status must be Active, Inactive, Planned, or Under Repair. | Reject asset. |
| DQ-008 | Diameter | Diameter must be numeric and greater than zero. | Reject asset. |
| DQ-009 | Geometry | Geometry must be present. | Reject asset. |
| DQ-010 | Geometry | LineString geometry must have at least two coordinate pairs. | Reject asset. |
| DQ-011 | Maintenance asset | Work order must reference a cleaned asset. | Route to unmatched maintenance output. |
| DQ-012 | Work order ID | `work_order_id` must be unique. | Exclude from clean maintenance aggregation. |
| DQ-013 | Maintenance date | `maintenance_date` must parse as a date. | Exclude from clean maintenance aggregation. |
| DQ-014 | Completion date | Completion date cannot be before maintenance date. | Exclude from clean maintenance aggregation. |
| DQ-015 | Cost | Labour, material, and total cost must be numeric and non-negative. | Exclude from clean maintenance aggregation. |
| DQ-016 | Cost reconciliation | Total cost should equal labour cost plus material cost within tolerance. | Flag for review. |
| DQ-017 | Service area | Asset should be assigned to a service area through spatial overlay. | Flag as `Review` if unassigned. |

These rules are intentionally simple enough for an interview demonstration. In production, each rule should have an owner, severity, tolerance, and remediation process.

