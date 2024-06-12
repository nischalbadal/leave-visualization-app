import os
import psycopg2
from flask import Flask, render_template, redirect
from dotenv import load_dotenv
import subprocess
from urllib.parse import urljoin

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# PostgreSQL database connection parameters
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


# Function to connect to the PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn


# Function to fetch employee details from dim_users table
def fetch_employee_details(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT "userId", "empId", "teamManagerId", "firstName", "middleName",
                   "lastName", "email", "isHr", "isSupervisor", "designationId"
            FROM dim_users
        """)
        employee_details = cursor.fetchall()
        return employee_details if employee_details else []  # Return empty list if no data found
        
    except psycopg2.Error as e:
        print(f"Error fetching employee details: {e}")
        return []  # Return empty list on error
    finally:
        cursor.close()

@app.route('/')
def streamlit_dashboard():
    try:
        # Run Streamlit app using subprocess
        subprocess.Popen(["streamlit", "run", "streamlit_app.py"])

        # Redirect to Streamlit app URL
        streamlit_url = "http://localhost:8502/"
        return redirect(streamlit_url)

    except Exception as e:
        print(f"Error running Streamlit app: {e}")
        return "Error running Streamlit app."

# Route to display employee details
@app.route('/api/employee/all')
def dashboard():
    try:
        conn = connect_to_db()
        employee_details = fetch_employee_details(conn)
        conn.close()

        if employee_details is None:
            employee_details = []  # Ensure employee_details is a list

        return render_template('dashboard.html', employee_details=employee_details)

    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return "Error fetching data from database"


if __name__ == '__main__':
    app.run(debug=True)
