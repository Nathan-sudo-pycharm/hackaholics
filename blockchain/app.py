import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Function for Aadhaar card validation (12 digits)
def is_valid_aadhaar(aadhaar_number):
    return len(aadhaar_number) == 12 and aadhaar_number.isdigit()

# Function to save login data to CSV file
def save_to_csv(name, aadhaar_number):
    data = {
        "Name": [name],
        "Aadhaar Number": [aadhaar_number]
    }
    df = pd.DataFrame(data)
    df.to_csv("login_data.csv", mode='a', header=False, index=False)

# Function to show the menu
def streamlit_menu(example=1):
    if example == 1:
        # Sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # Required
                options=["Home", "Projects", "Contact"],  # Required
                icons=["house", "book", "envelope"],  # Optional
                menu_icon="cast",  # Optional
                default_index=0,  # Optional
            )
        return selected

    if example == 2:
        # Horizontal menu without custom style
        selected = option_menu(
            menu_title=None,  # Required
            options=["Home", "What We do", "Upload the Files"],  # Required
            icons=["house", "book", "envelope"],  # Optional
            menu_icon="cast",  # Optional
            default_index=0,  # Optional
            orientation="horizontal",
        )
        return selected

    if example == 3:
        # Horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # Required
            options=["Home", "What We do", "Upload the Files"],  # Required
            icons=["house", "book", "envelope"],  # Optional
            menu_icon="cast",  # Optional
            default_index=0,  # Optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
        return selected

# Function to handle logging out
def logout():
    # Clear session state
    st.session_state.logged_in = False
    st.session_state.page = "login"

# Check if the user is logged in or not
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Page control
if "page" not in st.session_state:
    st.session_state.page = "login"

# Page navigation
if st.session_state.page == "login":
    st.title("Login to MedManager")

    # Input fields for name and Aadhaar number
    name = st.text_input("Enter your Name:")
    aadhaar_number = st.text_input("Enter your Aadhaar Card Number (12 digits):")

    # Validate Aadhaar number
    if is_valid_aadhaar(aadhaar_number):
        st.success("Aadhaar card number is valid! You can proceed to the main menu.")

        # Proceed button for navigating to the main menu
        if st.button("Login"):
            # Save login data to CSV
            save_to_csv(name, aadhaar_number)

            # Set the session state to logged in and navigate to main menu
            st.session_state.logged_in = True
            st.session_state.page = "main"

    else:
        if aadhaar_number:
            st.error("Aadhaar card number must be 12 digits long.")

    # Show name input
    if name:
        st.write(f"Hello, {name}!")

# Main menu page after login
if st.session_state.page == "main":
    selected = streamlit_menu(example=1)

    if selected == "Home":
        st.title(f"You have selected {selected}")
    elif selected == "Projects":
        st.title(f"You have selected {selected}")
    elif selected == "Contact":
        st.title(f"You have selected {selected}")

    # Add Log Out button
    if st.button("Log Out"):
        logout()
        st.session_state.page = "login"
