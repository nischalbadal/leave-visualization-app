WITH upsert AS (
    SELECT DISTINCT "userId", "empId", "teamManagerId", "firstName", "middleName", "lastName", "email", "isHr", "isSupervisor", "designationId"
    FROM raw_leave_data
)
INSERT INTO dim_users("userId", "empId", "teamManagerId", "firstName", "middleName", "lastName", "email", "isHr", "isSupervisor", "designationId")
SELECT "userId", "empId", "teamManagerId", "firstName", "middleName", "lastName", "email", "isHr", "isSupervisor", "designationId"
FROM upsert
ON CONFLICT ("userId") DO UPDATE
SET "empId" = EXCLUDED."empId",
    "teamManagerId" = EXCLUDED."teamManagerId",
    "firstName" = EXCLUDED."firstName",
    "middleName" = EXCLUDED."middleName",
    "lastName" = EXCLUDED."lastName",
    "email" = EXCLUDED."email",
    "isHr" = EXCLUDED."isHr",
    "isSupervisor" = EXCLUDED."isSupervisor",
    "designationId" = EXCLUDED."designationId";
