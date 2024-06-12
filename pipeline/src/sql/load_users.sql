truncate table users cascade;
insert into users("userId", "empId", "teamManagerId", "firstName", "middleName", "lastName", "email", "isHr", "isSupervisor", "designationId")
select distinct "userId", "empId", "teamManagerId", "firstName", "middleName", "lastName", "email", "isHr", "isSupervisor", "designationId" 
from raw_leave_data rld ;
