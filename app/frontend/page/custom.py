import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import requests
from config import API_URL

def main():
    def get_jwt_token():
        return st.session_state.get("token")

    jwt_token = get_jwt_token()

    if not jwt_token:
        st.warning("Please log in to access this page.")
        st.stop()

    def load_available_tables():
        headers = {"Authorization": f"Bearer {jwt_token}"}  # Add JWT token to headers
        response = requests.get(f"{API_URL}/tables", headers=headers)
        if response.status_code == 200:
            return response.json().get("tables", [])
        else:
            st.error("Failed to load tables")
            return []

    def load_table_data(table_name):
        headers = {"Authorization": f"Bearer {jwt_token}"}  # Add JWT token to headers
        response = requests.get(f"{API_URL}/table/{table_name}", headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()  # Try to parse JSON
                if data:
                    return pd.DataFrame(data)  # Return as DataFrame
                else:
                    st.error(f"No data found for table: {table_name}")
                    return pd.DataFrame()
            except ValueError:
                st.error("Response is not valid JSON.")
                st.text(response.text)  # Display raw response for debugging
                return pd.DataFrame()
        else:
            # Log the error response
            st.error(f"Failed to load data for table: {table_name}")
            st.text(response.text)  # Display raw response for debugging
            return pd.DataFrame()

    # Load available tables
    tables = load_available_tables()

    # Table selection
    fact_table, selected_table = st.columns(2)
    with fact_table:
        fact_table =st.write("Fact Table:", "fact_leave_request")
    with selected_table:
        selected_table = st.selectbox("Choose a Dimensions table:", tables)

    # Load selected table data
    if selected_table:
        df = load_table_data(selected_table)

        if df.empty:
            st.error("No data available to visualize.")
            return

        st.subheader(f"Data from table: fact_leave_request join with **{selected_table}**")
        st.dataframe(df, use_container_width=True)

        # Dynamic column loading for x and y axis
        col1, col2, col3 = st.columns(3)
        with col1:
            x_axis = st.selectbox("Select X-axis column:", df.columns)

        with col2:
            y_axis = st.selectbox("Select Y-axis column:", df.columns)

        with col3:
            # Chart type selection (added new chart types)
            chart_type = st.selectbox("Select Chart Type:", [
                "Pie Chart", "Line Graph", "Scatter Plot", "Histogram", "Area Chart"
            ])

        fil_col, fil_val = st.columns(2)

        with fil_col:
            filter_column = st.selectbox("Select a column to filter:", df.columns)

        with fil_val:
            filter_value = st.text_input(f"Filter {filter_column} value:")

        if filter_value:
            df = df[df[filter_column].astype(str).str.contains(filter_value, case=False)]

        # Container to display multiple charts
        st.subheader("Visualization")
        chart_container = st.container()

        # Create chart based on selections
        if chart_type == "Line Graph":
            fig = px.line(df, x=x_axis, y=y_axis, title=f"{chart_type} of {y_axis} vs {x_axis}", markers=True)
            fig.update_layout(height=400)  # Set height for smaller chart
            chart_container.plotly_chart(fig)

        elif chart_type == "Pie Chart":
            fig = px.pie(df, names=x_axis, values=y_axis, title=f"{chart_type} of {y_axis}")
            fig.update_layout(height=400)  # Set height for smaller chart
            chart_container.plotly_chart(fig)

        elif chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{chart_type} of {y_axis} vs {x_axis}")
            fig.update_layout(height=400)
            chart_container.plotly_chart(fig)

        elif chart_type == "Histogram":
            fig = px.histogram(df, x=x_axis, title=f"{chart_type} of {x_axis}")
            fig.update_layout(height=400)
            chart_container.plotly_chart(fig)

        elif chart_type == "Area Chart":
            fig = px.area(df, x=x_axis, y=y_axis, title=f"{chart_type} of {y_axis} over {x_axis}")
            fig.update_layout(height=400)
            chart_container.plotly_chart(fig)

    # Footer
    st.markdown("### Filters")
    st.markdown("Adjust the filters and selections to customize your data visualization.")
    st.info("Select the table and visualize the data interactively!")

if __name__ == "__main__":
    main()
