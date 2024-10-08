-- Truncate the users table and cascade the operation
TRUNCATE TABLE users CASCADE;

-- Insert distinct records into the users table
INSERT INTO users (
    "userId",
    "empId",
    "teamManagerId",
    "firstName",
    "middleName",
    "lastName",
    "email",
    "isHr",
    "isSupervisor",
    "designationId"
)
SELECT DISTINCT
    "userId",
    "empId",
    "teamManagerId",
    "firstName",
    "middleName",
    "lastName",
    "email",
    "isHr",
    "isSupervisor",
    "designationId"
FROM raw_leave_data rld;
