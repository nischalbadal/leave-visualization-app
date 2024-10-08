import streamlit as st
import requests
from page import employee, top_visualization, custom
from config import API_URL

def main():
    st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")

    # Initialize session state
    if "token" not in st.session_state:
        st.session_state.token = None
    if "page" not in st.session_state:
        st.session_state.page = "auth"

    # Check if the user is already logged in
    if st.session_state.token:
        st.session_state.page = "dashboard"

    # Render the appropriate page based on the session state
    if st.session_state.page == "dashboard":
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

    with st.form(key="login_form"):
        email = st.text_input("Email or Username", placeholder="Enter your email or username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            response = requests.post(
                f"{API_URL}/login", json={"email": email, "password": password}
            )

            if response.status_code == 200:
                st.session_state.token = response.json().get("access_token")
                st.session_state.page = "dashboard"
                st.success("Login successful! You can now access the dashboard.")
                st.experimental_set_query_params(page="dashboard")
            else:
                st.error("Login failed! Please check your email and password.")

def logout():
    st.session_state.token = None
    st.session_state.page = "auth"  # Redirect to auth options after logout
    st.success("You have been logged out.")

def show_register():
    st.subheader("Register")

    with st.form(key="register_form"):
        email = st.text_input("Email or Username", placeholder="Enter your email or username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        submit_button = st.form_submit_button("Register")

        if submit_button:
            if password != confirm_password:
                st.error("Passwords do not match!")
                return

            response = requests.post(
                f"{API_URL}/register", json={"email": email, "password": password}
            )

            if response.status_code == 201:
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Registration failed! Please try again.")

def show_dashboard():
    st.title("Data Visualization Dashboard ")

    top_visualizations, custom_visualizations, employee_profile, log_out = st.tabs(
        ["Top Visualizations", "Custom Visualizations", "Employee Profile", "Log Out"]
    )

    with top_visualizations:
        top_visualization.main()
    with custom_visualizations:
        custom.main()
    with employee_profile:
        employee.main()
    with log_out:
        if st.button("Logout"):
            logout()  # Call logout when the button is clicked

if __name__ == "__main__":
    main()
