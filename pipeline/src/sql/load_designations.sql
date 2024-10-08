-- Truncate the designations table
TRUNCATE TABLE designations CASCADE;

-- Insert distinct records into the designations table
INSERT INTO designations ("designationId", "designationName")
SELECT DISTINCT "designationId", "designationName"
FROM raw_leave_data rld;
