insert into dim_users
select distinct "userId", "empId", "teamManagerId", "firstName", "middleName", "lastName", "email", "isHr", "isSupervisor", "designationId" 
from users u ;