insert into dim_designations ("designationId", "designationName")
select distinct "designationId", "designationName" 
from designations d