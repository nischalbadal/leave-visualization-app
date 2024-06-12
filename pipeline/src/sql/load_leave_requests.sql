truncate table leave_requests cascade;
insert into leave_requests (id, "userId", "leaveIssuerId", "currentLeaveIssuerId", "leaveIssuerFirstName" , "leaveIssuerLastName", "currentLeaveIssuerEmail", "departmentDescription", "startDate", "endDate", "leaveDays", "reason", "status", "remarks", "leaveTypeId", "createdAt", "updatedAt", "isConverted", "fiscalId" )
select distinct id, "userId", "leaveIssuerId", "currentLeaveIssuerId", "leaveIssuerFirstName" , "leaveIssuerLastName", "currentLeaveIssuerEmail", "departmentDescription", "startDate", "endDate", "leaveDays", "reason", "status", "remarks", "leaveTypeId", "createdAt", "updatedAt", "isConverted", "fiscalId"
from raw_leave_data rld;
