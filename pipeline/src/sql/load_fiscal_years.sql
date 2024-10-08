-- Truncate the fiscal_years table and cascade the operation
TRUNCATE TABLE fiscal_years CASCADE;

-- Insert distinct records into the fiscal_years table
INSERT INTO fiscal_years ("fiscalId", "fiscalStartDate", "fiscalEndDate", "fiscalIsCurrent")
SELECT DISTINCT "fiscalId", "fiscalStartDate", "fiscalEndDate", "fiscalIsCurrent"
FROM raw_leave_data rld;
