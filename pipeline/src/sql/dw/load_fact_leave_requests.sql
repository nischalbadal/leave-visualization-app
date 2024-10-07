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
ON CONFLICT (id) DO UPDATE
SET "userId" = EXCLUDED."userId",
    "leaveIssuerId" = EXCLUDED."leaveIssuerId",
    "leaveDays" = EXCLUDED."leaveDays",
    "leaveTypeId" = EXCLUDED."leaveTypeId",
    "currentLeaveIssuerId" = EXCLUDED."currentLeaveIssuerId",
    "departmentDescription" = EXCLUDED."departmentDescription",
    "startDate" = EXCLUDED."startDate",
    "endDate" = EXCLUDED."endDate",
    reason = EXCLUDED.reason,
    status = EXCLUDED.status,
    remarks = EXCLUDED.remarks,
    "createdAt" = EXCLUDED."createdAt",
    "updatedAt" = EXCLUDED."updatedAt",
    "isConverted" = EXCLUDED."isConverted",
    "fiscalId" = EXCLUDED."fiscalId";
