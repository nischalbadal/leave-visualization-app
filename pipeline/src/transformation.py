import os
import psycopg2
import json
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from utils import log_pipeline_run

def connect_to_db():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    return conn


def execute_sql_file(conn, file_path):
    cursor = conn.cursor()
    with open(file_path, "r") as sql_file:
        cursor.execute(sql_file.read())
    conn.commit()
    cursor.close()


def fetch_distinct_allocations(conn):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT DISTINCT allocations::text FROM raw_leave_data WHERE allocations IS NOT NULL"
    )
    distinct_allocations = cursor.fetchall()

    cursor.execute("TRUNCATE TABLE allocations;")

    for allocation_row in distinct_allocations:
        allocations = json.loads(allocation_row[0])
        load_allocations(conn, allocations)


def load_allocations(conn, raw_data):
    cursor = conn.cursor()
    try:
        for record in raw_data:
            user_id = record.get("userId")
            allocations_json = record.get("allocations")

            if user_id and allocations_json:
                allocations = json.loads(allocations_json)

                for allocation in allocations:
                    allocation_id = allocation.get("id")
                    name = allocation.get("name")
                    allocation_type = allocation.get("type")

                    cursor.execute(
                        """
                        INSERT INTO allocations (allocationId, userId, name, type)
                        VALUES (%s, %s, %s, %s)
                    """,
                        (allocation_id, user_id, name, allocation_type),
                    )

        conn.commit()

    except psycopg2.Error as e:
        print(f"Error loading data into 'allocations' table: {e}")
        conn.rollback()
    finally:
        cursor.close()


def main():
    conn = connect_to_db()

    print("Applying transformation and loading to different tables:")
    sql_files_directory = "sql/"
    # sql_files = [f for f in os.listdir(sql_files_directory) if f.endswith('.sql')]
    sql_files = [
        "load_designations.sql",
        "load_fiscal_years.sql",
        "load_leave_types.sql",
        "load_users.sql",
        "load_leave_requests.sql",
    ]

    try:
        for sql_file in sql_files:
            table_name = sql_file.split("load_")[1].split(".")[0]
            print(f"Loading data to {table_name} table;")
            file_path = os.path.join(sql_files_directory, sql_file)
            execute_sql_file(conn, file_path)
            print("Data Load successful.")

        print(f"Loading data to allocations table;")
        fetch_distinct_allocations(conn)
        print("Data load successful.")
        log_pipeline_run(conn, f"transformation", 'COMPLETED', 'raw_leave_data')

    except psycopg2.Error as e:
        print(f"Error loading data into 'allocations' table: {e}")
        log_pipeline_run(conn, f"transformation", 'FAILED', 'raw_leave_data')
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
