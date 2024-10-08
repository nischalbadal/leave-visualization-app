WITH upsert AS (
    SELECT DISTINCT "designationId", "designationName"
    FROM raw_leave_data
)
INSERT INTO dim_designations ("designationId", "designationName")
SELECT "designationId", "designationName"
FROM upsert
ON CONFLICT ("designationId") DO UPDATE
SET "designationName" = EXCLUDED."designationName";
