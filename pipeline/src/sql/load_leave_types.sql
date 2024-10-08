-- Truncate the leave_types table and cascade the operation
TRUNCATE TABLE leave_types CASCADE;

-- Insert distinct records into the leave_types table
INSERT INTO leave_types (
    "leaveTypeId",
    "leaveTypeName",
    "defaultDays",
    "transferableDays",
    "isConsecutive"
)
SELECT DISTINCT
    "leaveTypeId",
    "leaveTypeName",
    "defaultDays",
    "transferableDays",
    "isConsecutive"
FROM raw_leave_data rld;
