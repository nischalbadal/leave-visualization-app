import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from config import API_URL


def main():
    st.title("Top Visualizations")

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/dashboard", headers=headers)

    if response.status_code == 200:
        data = response.json()

        dim_designations_df = pd.DataFrame(data["dim_designations"])
        dim_fiscal_periods_df = pd.DataFrame(data["dim_fiscal_periods"])
        dim_leave_types_df = pd.DataFrame(data["dim_leave_types"])
        dim_users_df = pd.DataFrame(data["dim_users"])
        dim_leave_issuer_df = pd.DataFrame(data["dim_leave_issuer"])
        fact_leave_requests_df = pd.DataFrame(data["fact_leave_requests"])

        # Pie Chart and Bar Chart
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Composition of Leave Types")
            leave_type_counts = (
                fact_leave_requests_df["leaveTypeName"].value_counts().reset_index()
            )
            leave_type_counts.columns = ["leaveTypeName", "count"]
            fig_pie = px.pie(
                leave_type_counts,
                values="count",
                names="leaveTypeName",
                title="Composition of Leave Types",
            )
            st.plotly_chart(fig_pie)

        with col2:
            st.subheader("Leave Requests per Department")
            dept_counts = (
                fact_leave_requests_df["departmentDescription"]
                .value_counts()
                .reset_index()
            )
            dept_counts.columns = ["departmentDescription", "count"]
            fig_bar = px.bar(
                dept_counts,
                x="departmentDescription",
                y="count",
                title="Leave Requests per Department",
            )
            st.plotly_chart(fig_bar)

        # Line Chart and Donut Chart
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Leave Requests Over Time")
            fact_leave_requests_df["startDate"] = pd.to_datetime(
                fact_leave_requests_df["startDate"]
            )
            time_series = (
                fact_leave_requests_df.groupby("startDate")
                .size()
                .reset_index(name="counts")
            )
            fig_line = px.line(
                time_series, x="startDate", y="counts", title="Leave Requests Over Time"
            )
            st.plotly_chart(fig_line)

        with col2:
            st.subheader("Leave Status by Department (Not Approved or Rejected)")
            status_dept = (
                fact_leave_requests_df.groupby(["departmentDescription", "status"])
                .size()
                .reset_index(name="counts")
            )
            fig_donut = px.pie(
                status_dept,
                values="counts",
                names="status",
                title="Leave Status by Department (Not Approved or Rejected)",
                color="departmentDescription",
                hole=0.4,
                hover_data=["departmentDescription"],
            )
            st.plotly_chart(fig_donut)

        # Histogram and Scatter Plot
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Distribution of Leave Days")
            fig_hist = px.histogram(
                fact_leave_requests_df,
                x="leaveDays",
                nbins=30,
                title="Distribution of Leave Days",
            )
            st.plotly_chart(fig_hist)

        with col2:
            st.subheader("Leave Requests vs. Fiscal Periods")
            fact_leave_requests_with_fiscal = fact_leave_requests_df.merge(
                dim_fiscal_periods_df, on="fiscalId", how="left"
            )
            fig_scatter = px.scatter(
                fact_leave_requests_with_fiscal,
                x="fiscalStartDate",
                y=fact_leave_requests_with_fiscal.index,
                title="Leave Requests vs. Fiscal Periods",
            )
            st.plotly_chart(fig_scatter)

        # Bubble Chart and Stacked Area Chart
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Leave Requests by Leave Type and Status")
            leave_type_status = (
                fact_leave_requests_df.groupby(["leaveTypeId", "status"])
                .size()
                .reset_index(name="counts")
            )
            fig_bubble = px.scatter(
                leave_type_status,
                x="leaveTypeId",
                y="counts",
                size="counts",
                color="status",
                title="Leave Requests by Leave Type and Status",
            )
            st.plotly_chart(fig_bubble)

        with col2:
            st.subheader("Accumulated Leave Days Over Time")
            fact_leave_requests_df["createdAt"] = pd.to_datetime(
                fact_leave_requests_df["createdAt"], errors="coerce"
            )
            if fact_leave_requests_df["createdAt"].isnull().any():
                st.warning(
                    "Some dates could not be converted. Please check the date format."
                )
            accum_leave_days = (
                fact_leave_requests_df.groupby(["createdAt", "leaveTypeId"])[
                    "leaveDays"
                ]
                .sum()
                .reset_index()
            )
            fig_stacked_area = px.area(
                accum_leave_days,
                x="createdAt",
                y="leaveDays",
                color="leaveTypeId",
                title="Accumulated Leave Days Over Time",
            )
            st.plotly_chart(fig_stacked_area)

        # Donut Chart and Box Plot
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("HR vs. Non-HR Leave Requests")
            hr_counts = (
                dim_users_df.merge(
                    fact_leave_requests_df,
                    left_on="userId",
                    right_on="userId",
                    how="left",
                )["isHr"]
                .value_counts()
                .reset_index()
            )
            hr_counts.columns = ["isHr", "count"]
            fig_donut = px.pie(
                hr_counts,
                values="count",
                names="isHr",
                hole=0.4,
                title="HR vs. Non-HR Leave Requests",
            )
            st.plotly_chart(fig_donut)

        with col2:
            st.subheader("Leave Days by Leave Type")
            fig_box = px.box(
                fact_leave_requests_df,
                x="leaveTypeId",
                y="leaveDays",
                title="Leave Days by Leave Type",
            )
            st.plotly_chart(fig_box)

        # Heatmap
        st.subheader("Leave Requests Heatmap by Leave Type and Status")
        not_approved_or_rejected = fact_leave_requests_df[
            (fact_leave_requests_df["status"] != "Approved")
            & (fact_leave_requests_df["status"] != "Rejected")
        ]
        heatmap_data = (
            fact_leave_requests_df.groupby(["leaveTypeId", "status"])
            .size()
            .reset_index(name="count")
        )

        if not heatmap_data.empty:
            heatmap_pivot = heatmap_data.pivot(
                index="leaveTypeId", columns="status", values="count"
            ).fillna(0)
            fig_heatmap = px.imshow(
                heatmap_pivot,
                labels=dict(x="Status", y="Leave Type", color="Number of Requests"),
                title="Heatmap of Leave Requests by Leave Type and Status",
                color_continuous_scale="Viridis",
            )
            st.plotly_chart(fig_heatmap)
        else:
            st.write("No data available for the heatmap.")

    else:
        st.error(f"Failed to fetch data from the server.")


if __name__ == "__main__":
    main()
