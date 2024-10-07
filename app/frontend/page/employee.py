import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from config import API_URL

def main():
    def get_jwt_token():
        return st.session_state.get("token")

    jwt_token = get_jwt_token()
    if not jwt_token:
        st.warning("Please log in to access this page.")
        st.stop()

    response = requests.get(
        f"{API_URL}/employee/names", headers={"Authorization": f"Bearer {jwt_token}"}
    )

    if response.status_code == 200:
        employee_names = response.json()
    else:
        st.error("Failed to fetch employee names.")
        st.stop()

    selected_employee = st.selectbox(
        "Select Employee:", [f"{emp['fullName']}" for emp in employee_names]
    )

    if st.button("Get Employee Data"):
        user_id = next(
            (
                emp["userId"]
                for emp in employee_names
                if emp["fullName"] == selected_employee
            ),
            None,
        )

        if user_id:
            response = requests.get(
                f"{API_URL}/employee/{user_id}",
                headers={"Authorization": f"Bearer {jwt_token}"},
            )

            if response.status_code == 200:
                data = response.json()

                employee_details = data["employee_details"]
                employee_leaves = pd.DataFrame(data["employee_leaves"])

                # Display employee details in cards
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "Employee Name",
                        f"{employee_details['firstName']} {employee_details['lastName']}",
                    )
                with col2:
                    st.metric("Email", f"{employee_details['email']}")
                with col3:
                    st.metric("Designation", f"{employee_details['designationName']}")

                if not employee_leaves.empty:
                    # Date filtering
                    employee_leaves["startDate"] = pd.to_datetime(
                        employee_leaves["startDate"]
                    )
                    employee_leaves["endDate"] = pd.to_datetime(
                        employee_leaves["endDate"]
                    )

                    # Date filtering
                    start_date = st.date_input(
                        "Start Date", value=employee_leaves["startDate"].min().date()
                    )  # Use .date() to get date type
                    end_date = st.date_input(
                        "End Date", value=employee_leaves["endDate"].max().date()
                    )  # Use .date() to get date type

                    # Filter employee leaves based on dates
                    filtered_leaves = employee_leaves[
                        (employee_leaves["startDate"] >= pd.to_datetime(start_date))
                        & (employee_leaves["endDate"] <= pd.to_datetime(end_date))
                    ]

                    st.subheader("Leave Records")
                    st.dataframe(
                        filtered_leaves[
                            [
                                "leaveTypeName",
                                "status",
                                "startDate",
                                "endDate",
                                "leaveDays",
                            ]
                        ],
                        use_container_width=True,
                    )

                    if not filtered_leaves.empty:
                        col1, col2 = st.columns(2)

                        with col1:
                            leave_by_type = (
                                filtered_leaves.groupby("leaveTypeName")["leaveDays"]
                                .sum()
                                .reset_index()
                            )
                            leave_by_type_chart = px.bar(
                                leave_by_type,
                                x="leaveTypeName",
                                y="leaveDays",
                                title="Leave Days by Type",
                            )
                            st.plotly_chart(leave_by_type_chart)

                        with col2:
                            leave_status_counts = (
                                filtered_leaves["status"].value_counts().reset_index()
                            )
                            leave_status_counts.columns = ["status", "count"]
                            leave_status_chart = px.pie(
                                leave_status_counts,
                                values="count",
                                names="status",
                                title="Leave Status Distribution",
                            )
                            st.plotly_chart(leave_status_chart)

                        leave_days_over_time = (
                            filtered_leaves.groupby("startDate")["leaveDays"]
                            .sum()
                            .reset_index()
                        )
                        leave_days_chart = px.line(
                            leave_days_over_time,
                            x="startDate",
                            y="leaveDays",
                            title="Leave Days Over Time",
                        )
                        st.plotly_chart(leave_days_chart)

                    else:
                        st.write("No leave records found for the selected date range.")
                else:
                    st.write("No leave records found for this employee.")
            else:
                st.error("Employee not found.")
        else:
            st.error("Could not find user ID for the selected employee.")


if __name__ == "__main__":
    main()
