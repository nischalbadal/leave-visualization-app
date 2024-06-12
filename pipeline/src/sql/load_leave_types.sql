truncate table leave_types cascade;
insert into leave_types ("leaveTypeId", "leaveTypeName", "defaultDays", "transferableDays", "isConsecutive")
select distinct "leaveTypeId" , "leaveTypeName", "defaultDays", "transferableDays", "isConsecutive"
from raw_leave_data rld;
