import os
import requests
import psycopg2
import json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# PostgreSQL database connection parameters from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Function to insert data into the PostgreSQL database
def insert_data_to_db(data, batch_size=1000, data_source='None'):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    # Truncate the table before inserting new data
    print("Truncating the raw_leave_data table before inserting the data.")
    cursor.execute("TRUNCATE TABLE raw_leave_data")
    print("Table truncation successful.")

    insert_query = """
    INSERT INTO raw_leave_data (
        "id", "userId", "empId", "teamManagerId", "designationId", "designationName",
        "firstName", "middleName", "lastName", "email", "isHr", "isSupervisor", "allocations",
        "leaveIssuerId", "currentLeaveIssuerId", "leaveIssuerFirstName", "leaveIssuerLastName",
        "currentLeaveIssuerEmail", "departmentDescription", "startDate", "endDate", "leaveDays",
        "reason", "status", "remarks", "leaveTypeId", "leaveTypeName", "defaultDays",
        "transferableDays", "isConsecutive", "fiscalId", "fiscalStartDate", "fiscalEndDate",
        "fiscalIsCurrent", "createdAt", "updatedAt", "isConverted", "dataSource", "ingestedDateTime"
    ) VALUES (
        %(id)s, %(userId)s, %(empId)s, %(teamManagerId)s, %(designationId)s, %(designationName)s,
        %(firstName)s, %(middleName)s, %(lastName)s, %(email)s, %(isHr)s, %(isSupervisor)s, %(allocations)s,
        %(leaveIssuerId)s, %(currentLeaveIssuerId)s, %(leaveIssuerFirstName)s, %(leaveIssuerLastName)s,
        %(currentLeaveIssuerEmail)s, %(departmentDescription)s, %(startDate)s, %(endDate)s, %(leaveDays)s,
        %(reason)s, %(status)s, %(remarks)s, %(leaveTypeId)s, %(leaveTypeName)s, %(defaultDays)s,
        %(transferableDays)s, %(isConsecutive)s, %(fiscalId)s, %(fiscalStartDate)s, %(fiscalEndDate)s,
        %(fiscalIsCurrent)s, %(createdAt)s, %(updatedAt)s, %(isConverted)s, %(dataSource)s, %(ingestedDateTime)s
    )
    """

    def cast_types(record):
        # Define default values for missing keys
        defaults = {
            'id': None, 'userId': None, 'empId': '', 'teamManagerId': None, 'designationId': None, 'designationName': '',
            'firstName': '', 'middleName': '', 'lastName': '', 'email': '', 'isHr': False, 'isSupervisor': False,
            'allocations': {}, 'leaveIssuerId': None, 'currentLeaveIssuerId': None, 'leaveIssuerFirstName': '',
            'leaveIssuerLastName': '', 'currentLeaveIssuerEmail': '', 'departmentDescription': '', 'startDate': None,
            'endDate': None, 'leaveDays': None, 'reason': '', 'status': '', 'remarks': '', 'leaveTypeId': None,
            'leaveTypeName': '', 'defaultDays': None, 'transferableDays': None, 'isConsecutive': False, 'fiscalId': None,
            'fiscalStartDate': None, 'fiscalEndDate': None, 'fiscalIsCurrent': False, 'createdAt': None, 'updatedAt': None,
            'isConverted': False, 'dataSource': data_source, 'ingestedDateTime': datetime.now()
        }

        # Use default values for missing keys
        for key in defaults:
            if key not in record:
                record[key] = defaults[key]

        # Convert boolean fields
        record['isHr'] = bool(int(record.get('isHr', 0)))
        record['isSupervisor'] = bool(int(record.get('isSupervisor', 0)))
        record['isConsecutive'] = bool(int(record.get('isConsecutive', 0)))
        record['fiscalIsCurrent'] = bool(int(record.get('fiscalIsCurrent', 0)))
        record['isConverted'] = bool(int(record.get('isConverted', 0)))

        # Ensure integer fields are cast correctly
        int_fields = [
            'id', 'userId', 'teamManagerId', 'designationId', 'leaveIssuerId',
            'currentLeaveIssuerId', 'leaveTypeId', 'defaultDays', 'transferableDays', 'fiscalId', 'leaveDays'
        ]
        for field in int_fields:
            if field in record and record[field] is not None:
                record[field] = int(record[field])

        # Ensure string fields are cast correctly
        str_fields = [
            'empId', 'designationName', 'firstName', 'middleName', 'lastName', 'email',
            'leaveIssuerFirstName', 'leaveIssuerLastName', 'currentLeaveIssuerEmail', 'departmentDescription',
            'reason', 'status', 'remarks', 'leaveTypeName', 'dataSource'
        ]
        for field in str_fields:
            if field in record and record[field] is not None:
                record[field] = str(record[field])

        # Ensure JSON fields are cast correctly
        json_fields = ['allocations']
        for field in json_fields:
            if field in record and record[field] is not None:
                record[field] = json.dumps(record[field])  # Convert dict to JSON string

        # Ensure datetime fields are cast correctly
        datetime_fields = ['startDate', 'endDate', 'fiscalStartDate', 'fiscalEndDate', 'createdAt', 'updatedAt']
        for field in datetime_fields:
            if field in record and record[field] is not None:
                record[field] = datetime.fromisoformat(record[field].replace('Z', '+00:00'))

        # Add current timestamp for ingestedDateTime
        record['ingestedDateTime'] = datetime.now()

        return record

    # Process data in batches
    for i in range(0, len(data), batch_size):

        batch = data[i:i + batch_size]
        for record in batch:
            record = cast_types(record)
            cursor.execute(insert_query, record)
        print(f"Batch size: {i} inserted successfully.")
        conn.commit()  # Commit the transaction for the current batch

    cursor.close()
    conn.close()