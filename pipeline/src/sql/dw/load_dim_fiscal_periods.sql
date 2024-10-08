WITH upsert AS (
    SELECT DISTINCT "fiscalId", "fiscalStartDate", "fiscalEndDate", "fiscalIsCurrent"
    FROM raw_leave_data
)
INSERT INTO dim_fiscal_periods ("fiscalId", "fiscalStartDate", "fiscalEndDate", "fiscalIsCurrent")
SELECT "fiscalId", "fiscalStartDate", "fiscalEndDate", "fiscalIsCurrent"
FROM upsert
ON CONFLICT ("fiscalId") DO UPDATE
SET "fiscalStartDate" = EXCLUDED."fiscalStartDate",
    "fiscalEndDate" = EXCLUDED."fiscalEndDate",
    "fiscalIsCurrent" = EXCLUDED."fiscalIsCurrent";
