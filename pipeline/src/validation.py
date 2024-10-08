import argparse
import json
import os
import psycopg2
import logging
from datetime import datetime

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# Set up logging
logging.basicConfig(
    filename="qc_reports/qc_report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_connection():
    """Create a database connection."""
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )


def ingestion_qc_checks(conn):
    """Perform ingestion QC checks on the raw_leave_data table."""
    logging.info("Starting ingestion QC checks...")
    report = {}
    friendly_field_names = {
        "userId": "null_user_id",
        "empId": "null_emp_id",
        "firstName": "null_first_name",
        "lastName": "null_last_name",
        "email": "null_email",
        "duplicate_empId_count": "duplicate_emp_ids_count",
        "negative_leave_days_count": "negative_leave_days_count",
        "invalid_email_count": "invalid_email_count",
        "invalid_date_range_count": "invalid_date_range_count",
    }

    with conn.cursor() as cur:
        # Check for null values in required fields
        required_fields = ["userId", "empId", "firstName", "lastName", "email"]
        for field in required_fields:
            # Corrected query with double quotes
            query = f'SELECT COUNT(*) FROM raw_leave_data WHERE "{field}" IS NULL;'
            cur.execute(query)
            null_count = cur.fetchone()[0]
            report[friendly_field_names[field]] = null_count

        # Check for unique empId
        query = 'SELECT COUNT(DISTINCT "empId"), COUNT(*) FROM raw_leave_data;'
        cur.execute(query)
        distinct_empId_count, total_count = cur.fetchone()
        duplicate_empId_count = total_count - distinct_empId_count
        report[friendly_field_names["duplicate_empId_count"]] = duplicate_empId_count

        # Check for data types and ranges
        query = 'SELECT COUNT(*) FROM raw_leave_data WHERE "leaveDays" < 0;'
        cur.execute(query)
        negative_leave_days_count = cur.fetchone()[0]
        report[
            friendly_field_names["negative_leave_days_count"]
        ] = negative_leave_days_count

        # Check for valid email format
        query = """
        SELECT COUNT(*) FROM raw_leave_data
        WHERE "email" NOT LIKE '%_@__%.__%';
        """
        cur.execute(query)
        invalid_email_count = cur.fetchone()[0]
        report[friendly_field_names["invalid_email_count"]] = invalid_email_count

        # Check for valid date ranges
        query = """
        SELECT COUNT(*) FROM raw_leave_data
        WHERE "startDate" > "endDate";
        """
        cur.execute(query)
        invalid_date_range_count = cur.fetchone()[0]
        report[
            friendly_field_names["invalid_date_range_count"]
        ] = invalid_date_range_count

    logging.info("Ingestion QC checks completed.")
    return report


def transformation_qc_checks(conn):
    """Perform transformation QC checks on various tables."""
    logging.info("Starting transformation QC checks...")
    report = {}

    with conn.cursor() as cur:
        # QC checks for designations table
        # Check for null values in designationId and designationName
        query = """
        SELECT COUNT(*) FROM designations
        WHERE "designationId" IS NULL OR "designationName" IS NULL;
        """
        cur.execute(query)
        designations_null_count = cur.fetchone()[0]
        report["null_designations"] = designations_null_count

        # QC checks for fiscal_years table
        # Check for null values in fiscalId
        query = """
        SELECT COUNT(*) FROM fiscal_years
        WHERE "fiscalId" IS NULL OR "fiscalStartDate" IS NULL OR "fiscalEndDate" IS NULL;
        """
        cur.execute(query)
        fiscal_years_null_count = cur.fetchone()[0]
        report["null_fiscal_years"] = fiscal_years_null_count

        # Check for unique fiscalIds
        query = """
        SELECT COUNT(DISTINCT "fiscalId"), COUNT(*) FROM fiscal_years;
        """
        cur.execute(query)
        distinct_fiscalId_count, total_count = cur.fetchone()
        duplicate_fiscalId_count = total_count - distinct_fiscalId_count
        report["duplicate_fiscalId_count"] = duplicate_fiscalId_count

        # QC checks for leave_types table
        # Check for null values in leaveTypeId and leaveTypeName
        query = """
        SELECT COUNT(*) FROM leave_types
        WHERE "leaveTypeId" IS NULL OR "leaveTypeName" IS NULL;
        """
        cur.execute(query)
        leave_types_null_count = cur.fetchone()[0]
        report["null_leave_types"] = leave_types_null_count

        # Check for unique leaveTypeIds
        query = """
        SELECT COUNT(DISTINCT "leaveTypeId"), COUNT(*) FROM leave_types;
        """
        cur.execute(query)
        distinct_leaveTypeId_count, total_count = cur.fetchone()
        duplicate_leaveTypeId_count = total_count - distinct_leaveTypeId_count
        report["duplicate_leaveTypeId_count"] = duplicate_leaveTypeId_count

        # QC checks for users table
        # Check for null values in userId, empId, firstName, lastName, and email
        query = """
        SELECT COUNT(*) FROM users
        WHERE "userId" IS NULL OR "empId" IS NULL OR "firstName" IS NULL OR "lastName" IS NULL OR "email" IS NULL;
        """
        cur.execute(query)
        users_null_count = cur.fetchone()[0]
        report["null_users"] = users_null_count

        # QC checks for allocations table
        # Check for null values in allocationId and userId
        query = """
        SELECT COUNT(*) FROM allocations
        WHERE "allocationId" IS NULL OR "userId" IS NULL;
        """
        cur.execute(query)
        allocations_null_count = cur.fetchone()[0]
        report["null_allocations"] = allocations_null_count

        # QC checks for leave_requests table
        # Check for null values in required fields
        query = """
        SELECT COUNT(*) FROM leave_requests
        WHERE "userId" IS NULL OR "leaveIssuerId" IS NULL OR "leaveTypeId" IS NULL OR "startDate" IS NULL OR "endDate" IS NULL OR "leaveDays" IS NULL;
        """
        cur.execute(query)
        leave_requests_null_count = cur.fetchone()[0]
        report["null_leave_requests"] = leave_requests_null_count

        # Check for valid foreign keys in leave_requests
        query = """
        SELECT COUNT(*) FROM leave_requests
        WHERE "fiscalId" NOT IN (SELECT "fiscalId" FROM fiscal_years) OR
              "leaveTypeId" NOT IN (SELECT "leaveTypeId" FROM leave_types) OR
              "userId" NOT IN (SELECT "userId" FROM users);
        """
        cur.execute(query)
        invalid_foreign_keys_count = cur.fetchone()[0]
        report["invalid_foreign_keys_in_leave_requests"] = invalid_foreign_keys_count

        # Check for negative leaveDays
        query = """
        SELECT COUNT(*) FROM leave_requests
        WHERE "leaveDays" < 0;
        """
        cur.execute(query)
        negative_leave_days_count = cur.fetchone()[0]
        report[
            "negative_leave_days_count_in_leave_requests"
        ] = negative_leave_days_count

    logging.info("Transformation QC checks completed.")
    return report


def data_transfer_qc_checks(conn):
    """Perform data transfer QC checks on data warehouse tables."""
    logging.info("Starting data transfer QC checks...")
    report = {}

    with conn.cursor() as cur:
        # QC checks for dim_designations table
        # Check for null values in required fields
        query = 'SELECT COUNT(*) FROM dim_designations WHERE "designationId" IS NULL;'
        cur.execute(query)
        report["null_designationId_count"] = cur.fetchone()[0]

        # Check for duplicate designationIds
        query = (
            'SELECT COUNT(DISTINCT "designationId"), COUNT(*) FROM dim_designations;'
        )
        cur.execute(query)
        distinct_designationId_count, total_count = cur.fetchone()
        report["duplicate_designationId_count"] = (
            total_count - distinct_designationId_count
        )

        # QC checks for dim_fiscal_periods table
        # Check for null values in required fields
        query = 'SELECT COUNT(*) FROM dim_fiscal_periods WHERE "fiscalId" IS NULL;'
        cur.execute(query)
        report["null_fiscalId_count"] = cur.fetchone()[0]

        # Check for overlapping fiscal periods
        query = """
        SELECT COUNT(*) FROM dim_fiscal_periods
        WHERE EXISTS (
            SELECT 1 FROM dim_fiscal_periods AS inner_period
            WHERE inner_period."fiscalId" <> dim_fiscal_periods."fiscalId"
            AND inner_period."fiscalStartDate" < dim_fiscal_periods."fiscalEndDate"
            AND inner_period."fiscalEndDate" > dim_fiscal_periods."fiscalStartDate"
        );
        """
        cur.execute(query)
        report["overlapping_fiscal_periods_count"] = cur.fetchone()[0]

        # QC checks for dim_leave_types table
        # Check for null values in required fields
        query = 'SELECT COUNT(*) FROM dim_leave_types WHERE "leaveTypeId" IS NULL;'
        cur.execute(query)
        report["null_leaveTypeId_count"] = cur.fetchone()[0]

        # Check for duplicate leaveTypeIds
        query = 'SELECT COUNT(DISTINCT "leaveTypeId"), COUNT(*) FROM dim_leave_types;'
        cur.execute(query)
        distinct_leaveTypeId_count, total_count = cur.fetchone()
        report["duplicate_leaveTypeId_count"] = total_count - distinct_leaveTypeId_count

        # QC checks for dim_users table
        # Check for null values in required fields
        query = 'SELECT COUNT(*) FROM dim_users WHERE "userId" IS NULL;'
        cur.execute(query)
        report["null_userId_count"] = cur.fetchone()[0]

        # Check for foreign key constraints
        query = """
        SELECT COUNT(*) FROM dim_users
        WHERE "designationId" IS NOT NULL AND "designationId" NOT IN (SELECT "designationId" FROM dim_designations);
        """
        cur.execute(query)
        report["invalid_designationId_count"] = cur.fetchone()[0]

        # QC checks for dim_leave_issuer table
        # Check for null values in required fields
        query = 'SELECT COUNT(*) FROM dim_leave_issuer WHERE "leaveIssuerId" IS NULL;'
        cur.execute(query)
        report["null_leaveIssuerId_count"] = cur.fetchone()[0]

        # Check for duplicate leaveIssuerIds
        query = (
            'SELECT COUNT(DISTINCT "leaveIssuerId"), COUNT(*) FROM dim_leave_issuer;'
        )
        cur.execute(query)
        distinct_leaveIssuerId_count, total_count = cur.fetchone()
        report["duplicate_leaveIssuerId_count"] = (
            total_count - distinct_leaveIssuerId_count
        )

        # QC checks for fact_leave_requests table
        # Check for null values in required fields
        query = 'SELECT COUNT(*) FROM fact_leave_requests WHERE "userId" IS NULL OR "leaveIssuerId" IS NULL;'
        cur.execute(query)
        report["null_userId_leaveIssuerId_count"] = cur.fetchone()[0]

        # Check for negative leaveDays
        query = 'SELECT COUNT(*) FROM fact_leave_requests WHERE "leaveDays" < 0;'
        cur.execute(query)
        report["negative_leaveDays_count"] = cur.fetchone()[0]

        # Validate foreign keys in fact_leave_requests
        query = """
        SELECT COUNT(*) FROM fact_leave_requests
        WHERE "leaveIssuerId" IS NOT NULL AND "leaveIssuerId" NOT IN (SELECT "leaveIssuerId" FROM dim_leave_issuer);
        """
        cur.execute(query)
        report["invalid_foreign_keys_in_fact_leave_requests"] = cur.fetchone()[0]

        # Additional checks for fiscalId
        query = """
        SELECT COUNT(*) FROM fact_leave_requests
        WHERE "fiscalId" IS NOT NULL AND "fiscalId" NOT IN (SELECT "fiscalId" FROM dim_fiscal_periods);
        """
        cur.execute(query)
        report["invalid_fiscalId_count_in_fact_leave_requests"] = cur.fetchone()[0]

        # Additional checks for leaveTypeId
        query = """
        SELECT COUNT(*) FROM fact_leave_requests
        WHERE "leaveTypeId" IS NOT NULL AND "leaveTypeId" NOT IN (SELECT "leaveTypeId" FROM dim_leave_types);
        """
        cur.execute(query)
        report["invalid_leaveTypeId_count_in_fact_leave_requests"] = cur.fetchone()[0]

    logging.info("Data transfer QC checks completed.")
    return report


def log_qc_report(conn, qc_name, qc_json):
    qc_report = {
        "qc_name": qc_name,
        "qc_json": json.dumps(qc_json),
        "created_timestamp": datetime.now(),
    }

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO qc_reports (qc_name, qc_json, created_timestamp) VALUES (%s, %s, %s)",
                (
                    qc_report["qc_name"],
                    qc_report["qc_json"],
                    qc_report["created_timestamp"],
                ),
            )
            conn.commit()
            print(f"QC successful. Report generated {qc_report}.")
            logging.info("QC report logged successfully.")
            print("QC report logged successfully")
    except Exception as e:
        logging.error(f"Error logging QC report: {e}")


def save_report(report, report_type):
    """Save the QC report as a JSON file."""
    os.makedirs("qc_reports", exist_ok=True)
    report_filename = f"qc_reports/{report_type}_qc_report.json"
    with open(report_filename, "w") as json_file:
        json.dump(report, json_file, indent=4)
    logging.info(f"QC report saved to {report_filename}")


def main():
    """Main function to execute QC checks."""
    parser = argparse.ArgumentParser(description="Perform QC checks on the database.")
    parser.add_argument(
        "--type",
        choices=["ingestion", "transformation", "data-transfer"],
        required=True,
        help="Type of QC check to perform.",
    )
    args = parser.parse_args()

    try:
        conn = create_connection()
        report = {}
        if args.type == "ingestion":
            report = ingestion_qc_checks(conn)
        elif args.type == "transformation":
            report = transformation_qc_checks(conn)
        elif args.type == "data-transfer":
            report = data_transfer_qc_checks(conn)

        save_report(report, args.type)

        log_qc_report(conn, args.type, report)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
