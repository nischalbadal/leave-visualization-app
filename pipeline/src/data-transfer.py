import os
import psycopg2
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL database connection parameters
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def connect_to_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def execute_sql_file(conn, file_path):
    cursor = conn.cursor()
    with open(file_path, 'r') as sql_file:
        cursor.execute(sql_file.read())
    conn.commit()
    cursor.close()

def main():
    # Connect to the database
    conn = connect_to_db()

    print("Applying transformation and loading to different tables:")
    # Get all SQL files in the directory
    sql_files_directory = 'sql/dw/'
    # sql_files = [f for f in os.listdir(sql_files_directory) if f.endswith('.sql')]

    sql_files = ['load_dim_designations.sql', 'load_dim_fiscal_periods.sql', 'load_dim_users.sql', 'load_dim_leave_types.sql',  'load_dim_leave_issuer.sql','load_fact_leave_requests.sql']

    try:
        # Iterate over SQL files and execute them
        for sql_file in sql_files:
            table_name = sql_file.split("load_")[1].split(".")[0]
            print(f"Loading data to {table_name} table;")
            file_path = os.path.join(sql_files_directory, sql_file)
            execute_sql_file(conn, file_path)
            print("Data Load successful.")

    except psycopg2.Error as e:
        print(f"Error loading data into 'allocations' table: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()