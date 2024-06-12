insert into dim_leave_types
select distinct "leaveTypeId" , "leaveTypeName", "defaultDays", "transferableDays", "isConsecutive"
from leave_types rld;
