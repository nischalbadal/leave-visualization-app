WITH upsert AS (
    SELECT
        COALESCE("currentLeaveIssuerId", "leaveIssuerId") AS "leaveIssuerId",
        MAX("leaveIssuerFirstName") AS "leaveIssuerFirstName",
        MAX("leaveIssuerLastName") AS "leaveIssuerLastName",
        MAX("currentLeaveIssuerEmail") AS "currentLeaveIssuerEmail"
    FROM leave_requests
    WHERE COALESCE("currentLeaveIssuerId", "leaveIssuerId") IS NOT NULL
      AND COALESCE("currentLeaveIssuerId", "leaveIssuerId") IN (SELECT "userId" FROM dim_users)
    GROUP BY COALESCE("currentLeaveIssuerId", "leaveIssuerId")
)
INSERT INTO dim_leave_issuer ("leaveIssuerId", "leaveIssuerFirstName", "leaveIssuerLastName", "leaveIssuerEmail")
SELECT "leaveIssuerId", "leaveIssuerFirstName", "leaveIssuerLastName", "currentLeaveIssuerEmail"
FROM upsert
ON CONFLICT ("leaveIssuerId") DO UPDATE
SET "leaveIssuerFirstName" = EXCLUDED."leaveIssuerFirstName",
    "leaveIssuerLastName" = EXCLUDED."leaveIssuerLastName",
    "leaveIssuerEmail" = EXCLUDED."leaveIssuerEmail";
