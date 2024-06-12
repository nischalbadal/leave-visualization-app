truncate table fiscal_years cascade;
insert into fiscal_years ("fiscalId", "fiscalStartDate", "fiscalEndDate", "fiscalIsCurrent")
select distinct "fiscalId", "fiscalStartDate", "fiscalEndDate", "fiscalIsCurrent" 
from raw_leave_data rld;
