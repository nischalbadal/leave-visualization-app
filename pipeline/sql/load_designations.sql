TRUNCATE TABLE designations CASCADE;
insert into designations ("designationId", "designationName")
select distinct "designationId", "designationName" 
from raw_leave_data rld ;