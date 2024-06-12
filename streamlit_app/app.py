import os
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv
import psycopg2

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

# Function to fetch data from a table
def fetch_data(conn, table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    return df

# Fetch data from all tables
with connect_to_db() as conn:
    dim_designations = fetch_data(conn, 'dim_designations')
    dim_fiscal_periods = fetch_data(conn, 'dim_fiscal_periods')
    dim_leave_types = fetch_data(conn, 'dim_leave_types')
    dim_users = fetch_data(conn, 'dim_users')
    dim_leave_issuer = fetch_data(conn, 'dim_leave_issuer')
    fact_leave_requests = fetch_data(conn, 'fact_leave_requests')

# Page configuration
st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")

st.title("Data Visualization Dashboard")

# Pie Chart - Composition of Leave Types
st.subheader("Composition of Leave Types")
leave_type_counts = fact_leave_requests['leaveTypeId'].value_counts().reset_index()
leave_type_counts.columns = ['leaveTypeId', 'count']
fig_pie = px.pie(leave_type_counts, values='count', names='leaveTypeId', title='Composition of Leave Types')
st.plotly_chart(fig_pie)

# Bar Chart - Leave Requests per Department
st.subheader("Leave Requests per Department")
dept_counts = fact_leave_requests['departmentDescription'].value_counts().reset_index()
dept_counts.columns = ['departmentDescription', 'count']
fig_bar = px.bar(dept_counts, x='departmentDescription', y='count', title='Leave Requests per Department')
st.plotly_chart(fig_bar)

# Line Chart - Leave Requests Over Time
st.subheader("Leave Requests Over Time")
fact_leave_requests['startDate'] = pd.to_datetime(fact_leave_requests['startDate'])
time_series = fact_leave_requests.groupby('startDate').size().reset_index(name='counts')
fig_line = px.line(time_series, x='startDate', y='counts', title='Leave Requests Over Time')
st.plotly_chart(fig_line)

# Stacked Bar Chart - Leave Status by Department
st.subheader("Leave Status by Department")
status_dept = fact_leave_requests.groupby(['departmentDescription', 'status']).size().reset_index(name='counts')
fig_stacked_bar = px.bar(status_dept, x='departmentDescription', y='counts', color='status', title='Leave Status by Department')
st.plotly_chart(fig_stacked_bar)

# Histogram - Distribution of Leave Days
st.subheader("Distribution of Leave Days")
fig_hist = px.histogram(fact_leave_requests, x='leaveDays', nbins=30, title='Distribution of Leave Days')
st.plotly_chart(fig_hist)

# Scatter Plot - Leave Requests vs. Fiscal Periods
st.subheader("Leave Requests vs. Fiscal Periods")
fact_leave_requests = fact_leave_requests.merge(dim_fiscal_periods, on='fiscalId', how='left')
fig_scatter = px.scatter(fact_leave_requests, x='fiscalStartDate', y=fact_leave_requests.index, title='Leave Requests vs. Fiscal Periods')
st.plotly_chart(fig_scatter)

# Tree Map - Hierarchical View of Leave Types and Days
st.subheader("Hierarchical View of Leave Types and Days")
fig_tree = px.treemap(dim_leave_types, path=['leaveTypeName'], values='defaultDays', title='Hierarchical View of Leave Types and Days')
st.plotly_chart(fig_tree)

# Bubble Chart - Leave Requests by Leave Type and Status
st.subheader("Leave Requests by Leave Type and Status")
leave_type_status = fact_leave_requests.groupby(['leaveTypeId', 'status']).size().reset_index(name='counts')
fig_bubble = px.scatter(leave_type_status, x='leaveTypeId', y='counts', size='counts', color='status', title='Leave Requests by Leave Type and Status')
st.plotly_chart(fig_bubble)

# Stacked Area Chart - Accumulated Leave Days Over Time
st.subheader("Accumulated Leave Days Over Time")
fact_leave_requests['createdAt'] = pd.to_datetime(fact_leave_requests['createdAt'])
accum_leave_days = fact_leave_requests.groupby(['createdAt', 'leaveTypeId'])['leaveDays'].sum().reset_index()
fig_stacked_area = px.area(accum_leave_days, x='createdAt', y='leaveDays', color='leaveTypeId', title='Accumulated Leave Days Over Time')
st.plotly_chart(fig_stacked_area)

# Donut Chart - HR vs. Non-HR Leave Requests
st.subheader("HR vs. Non-HR Leave Requests")
hr_counts = dim_users.merge(fact_leave_requests, left_on='userId', right_on='userId', how='left')['isHr'].value_counts().reset_index()
hr_counts.columns = ['isHr', 'count']
fig_donut = px.pie(hr_counts, values='count', names='isHr', hole=0.4, title='HR vs. Non-HR Leave Requests')
st.plotly_chart(fig_donut)

# Box and Whisker Plot - Leave Days by Leave Type
st.subheader("Leave Days by Leave Type")
fig_box = px.box(fact_leave_requests, x='leaveTypeId', y='leaveDays', title='Leave Days by Leave Type')
st.plotly_chart(fig_box)


