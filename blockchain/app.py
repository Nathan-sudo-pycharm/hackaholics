import streamlit as st
import pandas as pd
import os
from streamlit_option_menu import option_menu


# Function for Aadhaar card validation (12 digits)
def is_valid_aadhaar(aadhaar_number):
    return len(aadhaar_number) == 12 and aadhaar_number.isdigit()


# Function to save login data to CSV file
def save_to_csv(name, aadhaar_number, file_path="login_data.csv"):
    data = {"Name": [name], "Aadhaar": [aadhaar_number]}
    df = pd.DataFrame(data)

    try:
        df_existing = pd.read_csv(file_path)
        df_combined = pd.concat([df_existing, df])
        df_combined.drop_duplicates(subset=["Aadhaar"], inplace=True)
        df_combined.to_csv(file_path, index=False)
    except FileNotFoundError:
        df.to_csv(file_path, index=False)


# Function to handle file upload
def handle_file_upload(file, aadhaar_number, user_name):
    # Define the directory to save the uploaded file using the user's name
    upload_dir = os.path.join("uploads", user_name)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Save the file to the directory
    file_path = os.path.join(upload_dir, f"{aadhaar_number}_{file.name}")

    # Ensure the file is saved properly by writing the file buffer
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())  # Write the uploaded file buffer

    return file_path


# Function to list all uploaded files
def list_uploaded_files():
    uploaded_files_info = []
    upload_dir = "uploads"

    if os.path.exists(upload_dir):
        user_folders = os.listdir(upload_dir)  # List of user folders

        for user_folder in user_folders:
            user_folder_path = os.path.join(upload_dir, user_folder)
            if os.path.isdir(user_folder_path):  # Make sure it's a directory
                user_files = os.listdir(user_folder_path)
                for file in user_files:
                    uploaded_files_info.append({
                        "User Folder": user_folder,
                        "File Name": file,
                        "File Path": os.path.join(user_folder_path, file)
                    })

    return uploaded_files_info


# Main application logic
def main():
    st.title("User Aadhaar Login Portal")

    # Sidebar menu
    with st.sidebar:
        selected = option_menu(
            "Main Menu",
            ["Home", "Login", "Admin"],
            icons=["house", "key", "gear"],
            menu_icon="cast",
            default_index=0,
            key="main_menu"
        )

    if selected == "Home":
        st.subheader("Welcome to the Aadhaar Validation Portal")
        st.write("Please navigate through the menu to Login or access Admin settings.")

    elif selected == "Login":
        st.subheader("Login Section")
        name = st.text_input("Enter your Name:")
        aadhaar_number = st.text_input("Enter your Aadhaar Number (12 digits):", type="password")

        if st.button("Submit", key="login_button"):
            if is_valid_aadhaar(aadhaar_number):
                # Save user data to CSV
                save_to_csv(name, aadhaar_number)

                # Handle file upload
                uploaded_file = st.file_uploader("Upload Image or PDF", type=["jpg", "jpeg", "png", "pdf"])

                if uploaded_file is not None:
                    # Save uploaded file to disk and display the saved file path
                    file_path = handle_file_upload(uploaded_file, aadhaar_number, name)
                    st.success(f"File uploaded successfully! Saved at: {file_path}")
                else:
                    st.warning("No file uploaded.")

                st.success(f"Welcome, {name}! Your login data has been saved.")
            else:
                st.error("Invalid Aadhaar Number. Please enter a 12-digit number.")

    elif selected == "Admin":
        st.subheader("Admin Section")
        st.write("View registered user data and uploaded files below.")

        file_path = "login_data.csv"
        try:
            df_data = pd.read_csv(file_path)
            st.dataframe(df_data)

            # List uploaded files
            st.subheader("Uploaded Files")
            uploaded_files_info = list_uploaded_files()

            if uploaded_files_info:
                for file_info in uploaded_files_info:
                    st.write(f"User Folder: {file_info['User Folder']}")
                    st.write(f"File: {file_info['File Name']}")
                    file_url = file_info['File Path']
                    st.download_button("Download File", file_url)

            else:
                st.warning("No files uploaded yet.")
        except FileNotFoundError:
            st.warning("No data available yet.")


if __name__ == "__main__":
    main()
