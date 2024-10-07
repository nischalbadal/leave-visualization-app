import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000")

def main():
    st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")

    # Initialize session state for token and page if they don't exist
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'page' not in st.session_state:
        st.session_state.page = 'auth'  # Default to authentication page

    # Check the current page state
    if st.session_state.page == 'dashboard' and st.session_state.token:
        show_dashboard()
    else:
        show_auth_options()

def show_auth_options():
    st.title("Welcome")
    option = st.selectbox("Choose an option", ["Login", "Register"])

    if option == "Login":
        show_login()
    else:
        show_register()

def show_login():
    st.subheader("Login")

    with st.form(key='login_form'):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            # Authenticate the user
            response = requests.post(f"{API_URL}/login", json={"email": email, "password": password})

            if response.status_code == 200:
                st.session_state.token = response.json().get("access_token")
                st.session_state.page = 'dashboard'  # Set the page to dashboard
                st.success("Login successful! You can now access the dashboard.")
                st.experimental_set_query_params(page='dashboard')  # Set the query parameter to indicate the dashboard page
            else:
                st.error("Login failed! Please check your email and password.")

def show_register():
    st.subheader("Register")

    with st.form(key='register_form'):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        submit_button = st.form_submit_button("Register")

        if submit_button:
            if password != confirm_password:
                st.error("Passwords do not match!")
                return

            # Register the user
            response = requests.post(f"{API_URL}/register", json={"email": email, "password": password})

            if response.status_code == 201:
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Registration failed! Please try again.")

def show_dashboard():
    st.title("Data Visualization Dashboard ")

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/dashboard", headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Convert to DataFrames
        dim_designations_df = pd.DataFrame(data["dim_designations"])
        dim_fiscal_periods_df = pd.DataFrame(data["dim_fiscal_periods"])
        dim_leave_types_df = pd.DataFrame(data["dim_leave_types"])
        dim_users_df = pd.DataFrame(data["dim_users"])
        dim_leave_issuer_df = pd.DataFrame(data["dim_leave_issuer"])
        fact_leave_requests_df = pd.DataFrame(data["fact_leave_requests"])

        # Pie Chart - Composition of Leave Types
        st.subheader("Composition of Leave Types")
        leave_type_counts = fact_leave_requests_df['leaveTypeName'].value_counts().reset_index()
        leave_type_counts.columns = ['leaveTypeName', 'count']
        fig_pie = px.pie(leave_type_counts, values='count', names='leaveTypeName', title='Composition of Leave Types')
        st.plotly_chart(fig_pie)

        # Bar Chart - Leave Requests per Department
        st.subheader("Leave Requests per Department")
        dept_counts = fact_leave_requests_df['departmentDescription'].value_counts().reset_index()
        dept_counts.columns = ['departmentDescription', 'count']
        fig_bar = px.bar(dept_counts, x='departmentDescription', y='count', title='Leave Requests per Department')
        st.plotly_chart(fig_bar)

        # Line Chart - Leave Requests Over Time
        st.subheader("Leave Requests Over Time")
        fact_leave_requests_df['startDate'] = pd.to_datetime(fact_leave_requests_df['startDate'])
        time_series = fact_leave_requests_df.groupby('startDate').size().reset_index(name='counts')
        fig_line = px.line(time_series, x='startDate', y='counts', title='Leave Requests Over Time')
        st.plotly_chart(fig_line)

        status_dept = fact_leave_requests_df.groupby(['departmentDescription', 'status']).size().reset_index(name='counts')
        # Donut Chart - Leave Status by Department (Not Approved or Rejected)
        st.subheader("Leave Status by Department (Not Approved or Rejected)")
        fig_donut = px.pie(status_dept, values='counts', names='status', title='Leave Status by Department (Not Approved or Rejected)', 
                        color='departmentDescription', 
                        hole=0.4, 
                        hover_data=['departmentDescription'])

        st.plotly_chart(fig_donut)

        # Histogram - Distribution of Leave Days
        st.subheader("Distribution of Leave Days")
        fig_hist = px.histogram(fact_leave_requests_df, x='leaveDays', nbins=30, title='Distribution of Leave Days')
        st.plotly_chart(fig_hist)

        # Scatter Plot - Leave Requests vs. Fiscal Periods
        st.subheader("Leave Requests vs. Fiscal Periods")
        fact_leave_requests_with_fiscal = fact_leave_requests_df.merge(dim_fiscal_periods_df, on='fiscalId', how='left')
        fig_scatter = px.scatter(fact_leave_requests_with_fiscal, x='fiscalStartDate', y=fact_leave_requests_with_fiscal.index, title='Leave Requests vs. Fiscal Periods')
        st.plotly_chart(fig_scatter)

        # Bubble Chart - Leave Requests by Leave Type and Status
        st.subheader("Leave Requests by Leave Type and Status")
        leave_type_status = fact_leave_requests_df.groupby(['leaveTypeId', 'status']).size().reset_index(name='counts')
        fig_bubble = px.scatter(leave_type_status, x='leaveTypeId', y='counts', size='counts', color='status', title='Leave Requests by Leave Type and Status')
        st.plotly_chart(fig_bubble)

        # Stacked Area Chart - Accumulated Leave Days Over Time
        st.subheader("Accumulated Leave Days Over Time")
        # Convert 'createdAt' to datetime, specifying the format
        fact_leave_requests_df['createdAt'] = pd.to_datetime(fact_leave_requests_df['createdAt'], errors='coerce')
        # Check for any rows that couldn't be converted
        if fact_leave_requests_df['createdAt'].isnull().any():
            st.warning("Some dates could not be converted. Please check the date format.")
        # Group by 'createdAt' and 'leaveTypeId', summing the leave days
        accum_leave_days = fact_leave_requests_df.groupby(['createdAt', 'leaveTypeId'])['leaveDays'].sum().reset_index()

        # Create the stacked area chart
        fig_stacked_area = px.area(accum_leave_days, x='createdAt', y='leaveDays', color='leaveTypeId', title='Accumulated Leave Days Over Time')
        st.plotly_chart(fig_stacked_area)

        # Donut Chart - HR vs. Non-HR Leave Requests
        st.subheader("HR vs. Non-HR Leave Requests")
        hr_counts = dim_users_df.merge(fact_leave_requests_df, left_on='userId', right_on='userId', how='left')['isHr'].value_counts().reset_index()
        hr_counts.columns = ['isHr', 'count']
        fig_donut = px.pie(hr_counts, values='count', names='isHr', hole=0.4, title='HR vs. Non-HR Leave Requests')
        st.plotly_chart(fig_donut)

        # Box and Whisker Plot - Leave Days by Leave Type
        st.subheader("Leave Days by Leave Type")
        fig_box = px.box(fact_leave_requests_df, x='leaveTypeId', y='leaveDays', title='Leave Days by Leave Type')
        st.plotly_chart(fig_box)       
        
        # Filter leave requests that are not approved or rejected
        not_approved_or_rejected = fact_leave_requests_df[
            (fact_leave_requests_df['status'] != 'Approved') & 
            (fact_leave_requests_df['status'] != 'Rejected')
        ]

        # Count the occurrences of each status
        leave_status_counts = not_approved_or_rejected['status'].value_counts().reset_index()
        leave_status_counts.columns = ['status', 'count']

        # Create a pivot table to count the leave requests by leave type and status
        heatmap_data = fact_leave_requests_df.groupby(['leaveTypeId', 'status']).size().unstack(fill_value=0)

        # Reset index to convert the pivot table back to a DataFrame for Plotly
        heatmap_data = heatmap_data.reset_index()

        # Create a DataFrame with leave request counts grouped by leave type and status
        heatmap_data = (fact_leave_requests_df
                        .groupby(['leaveTypeId', 'status'])
                        .size()
                        .reset_index(name='count'))

        # Check if heatmap_data has records
        if not heatmap_data.empty:
            # Create a pivot table to get leave requests by leave type and status
            heatmap_pivot = heatmap_data.pivot(index='leaveTypeId', columns='status', values='count').fillna(0)

            # Create a heatmap
            st.subheader("Leave Requests Heatmap by Leave Type and Status")
            fig_heatmap = px.imshow(heatmap_pivot,
                                    labels=dict(x='Status', y='Leave Type', color='Number of Requests'),
                                    title='Heatmap of Leave Requests by Leave Type and Status',
                                    color_continuous_scale='Viridis')

            st.plotly_chart(fig_heatmap)
        else:
            st.write("No data available for the heatmap.")

    else:
        st.error(f"Failed to fetch data from the server.")


if __name__ == '__main__':
    main()
