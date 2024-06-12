import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://app:8000/api"

st.title("Employee Leave Visualization")

# Fetch employees
response = requests.get(f"{API_URL}/employees")
if response.status_code == 200:
    employees = response.json()
    employees_df = pd.DataFrame(employees)
    st.write("Employee Data", employees_df)
else:
    st.error("Failed to fetch employee data")

# Fetch leaves
response = requests.get(f"{API_URL}/leaves")
if response.status_code == 200:
    leaves = response.json()
    leaves_df = pd.DataFrame(leaves)
    st.write("Leave Data", leaves_df)

    # Visualization: Leave Types Distribution
    st.subheader("Leave Types Distribution")
    leave_type_counts = leaves_df['leave_type'].value_counts()
    st.bar_chart(leave_type_counts)

    # Visualization: Leaves by Department
    st.subheader("Leaves by Department")
    leaves_by_department = leaves_df.groupby(['department']).size()
    st.bar_chart(leaves_by_department)

    # Visualization: Leaves by Month
    st.subheader("Leaves by Month")
    leaves_df['start_date'] = pd.to_datetime(leaves_df['start_date'])
    leaves_df['month'] = leaves_df['start_date'].dt.month
    leaves_by_month = leaves_df['month'].value_counts().sort_index()
    st.line_chart(leaves_by_month)

    # Visualization: Leave Status Distribution
    st.subheader("Leave Status Distribution")
    leave_status_counts = leaves_df['status'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(leave_status_counts, labels=leave_status_counts.index, autopct='%1.1f%%')
    st.pyplot(fig1)
else:
    st.error("Failed to fetch leave data")

if __name__ == "__main__":
    st.run()
