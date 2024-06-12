insert into fact_leave_requests (id, "userId", "leaveIssuerId", "leaveDays", "leaveTypeId", "currentLeaveIssuerId",
"departmentDescription", "startDate", "endDate",
reason, status, remarks, "createdAt", "updatedAt", "isConverted", "fiscalId")
select id, "userId", flr."leaveIssuerId", "leaveDays", "leaveTypeId", "currentLeaveIssuerId",
"departmentDescription", "startDate", "endDate",
reason, status, remarks, "createdAt", "updatedAt", "isConverted", "fiscalId" from leave_requests flr
inner join dim_leave_issuer dli on flr."leaveIssuerId"  = dli."leaveIssuerId"  and flr."currentLeaveIssuerId" = dli."leaveIssuerId"
