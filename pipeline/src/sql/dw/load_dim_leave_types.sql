WITH upsert AS (
    SELECT DISTINCT "leaveTypeId", "leaveTypeName", "defaultDays", "transferableDays", "isConsecutive"
    FROM raw_leave_data
)
INSERT INTO dim_leave_types ("leaveTypeId", "leaveTypeName", "defaultDays", "transferableDays", "isConsecutive")
SELECT "leaveTypeId", "leaveTypeName", "defaultDays", "transferableDays", "isConsecutive"
FROM upsert
ON CONFLICT ("leaveTypeId") DO UPDATE
SET "leaveTypeName" = EXCLUDED."leaveTypeName",
    "defaultDays" = EXCLUDED."defaultDays",
    "transferableDays" = EXCLUDED."transferableDays",
    "isConsecutive" = EXCLUDED."isConsecutive";
