-- Truncate the leave_requests table and cascade the operation
TRUNCATE TABLE leave_requests CASCADE;

-- Insert distinct records into the leave_requests table
INSERT INTO leave_requests (
    id,
    "userId",
    "leaveIssuerId",
    "currentLeaveIssuerId",
    "leaveIssuerFirstName",
    "leaveIssuerLastName",
    "currentLeaveIssuerEmail",
    "departmentDescription",
    "startDate",
    "endDate",
    "leaveDays",
    "reason",
    "status",
    "remarks",
    "leaveTypeId",
    "createdAt",
    "updatedAt",
    "isConverted",
    "fiscalId"
)
SELECT DISTINCT
    id,
    "userId",
    "leaveIssuerId",
    "currentLeaveIssuerId",
    "leaveIssuerFirstName",
    "leaveIssuerLastName",
    "currentLeaveIssuerEmail",
    "departmentDescription",
    "startDate",
    "endDate",
    "leaveDays",
    "reason",
    "status",
    "remarks",
    "leaveTypeId",
    "createdAt",
    "updatedAt",
    "isConverted",
    "fiscalId"
FROM raw_leave_data rld;
