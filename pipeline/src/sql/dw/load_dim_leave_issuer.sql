with cte_leave_issuer as (
select distinct coalesce("currentLeaveIssuerId", "leaveIssuerId") as "leaveIssuerId" , "leaveIssuerFirstName", "leaveIssuerLastName", "currentLeaveIssuerEmail"  
from leave_requests
)
insert into dim_leave_issuer ("leaveIssuerId", "leaveIssuerFirstName", "leaveIssuerLastName", "leaveIssuerEmail")
select "leaveIssuerId", "leaveIssuerFirstName", "leaveIssuerLastName", "currentLeaveIssuerEmail" from cte_leave_issuer
inner join dim_users on dim_users."userId" = cte_leave_issuer."leaveIssuerId"