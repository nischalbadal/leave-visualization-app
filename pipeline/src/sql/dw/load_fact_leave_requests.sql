WITH upsert AS (
    SELECT
        id,
        "userId",
        flr."leaveIssuerId",
        "leaveDays",
        "leaveTypeId",
        "currentLeaveIssuerId",
        "departmentDescription",
        "startDate",
        "endDate",
        reason,
        status,
        remarks,
        "createdAt",
        "updatedAt",
        "isConverted",
        "fiscalId"
    FROM leave_requests flr
    INNER JOIN dim_leave_issuer dli ON flr."leaveIssuerId" = dli."leaveIssuerId"
    AND flr."currentLeaveIssuerId" = dli."leaveIssuerId"
)
INSERT INTO fact_leave_requests (id, "userId", "leaveIssuerId", "leaveDays", "leaveTypeId", "currentLeaveIssuerId",
    "departmentDescription", "startDate", "endDate",
    reason, status, remarks, "createdAt", "updatedAt", "isConverted", "fiscalId")
SELECT id, "userId", "leaveIssuerId", "leaveDays", "leaveTypeId", "currentLeaveIssuerId",
    "departmentDescription", "startDate", "endDate",
    reason, status, remarks, "createdAt", "updatedAt", "isConverted", "fiscalId"
FROM upsert
WHERE NOT EXISTS (
    SELECT 1 FROM fact_leave_requests WHERE id = upsert.id
);
