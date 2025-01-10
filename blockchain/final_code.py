import streamlit as st
import os
import re  # For email validation


# Function to handle file upload and save it locally with customer name in their own folder
def save_image(uploaded_file, aadhaar_first_4_digits, customer_name):
    # Define the base directory to save the uploaded files
    save_dir = f"uploaded_images/{aadhaar_first_4_digits}"

    # Check if the directory exists, create if it doesn't
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Extract file extension from the uploaded file
    file_extension = uploaded_file.name.split('.')[-1]

    # Create the custom file name with the customer's name
    file_name = f"{customer_name}.{file_extension}"

    # Define the file path to save the uploaded image
    file_path = os.path.join(save_dir, file_name)

    # Write the file to the local system
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


# Function to display images in the Admin section
def display_uploaded_images(aadhaar_first_4_digits):
    # Define the directory for the specific user's Aadhaar folder
    save_dir = f"uploaded_images/{aadhaar_first_4_digits}"

    # Check if the directory exists
    if os.path.exists(save_dir):
        # List all files in the directory
        uploaded_files = os.listdir(save_dir)

        if uploaded_files:
            st.subheader("Uploaded Images")
            for file_name in uploaded_files:
                # Define the path of each image
                file_path = os.path.join(save_dir, file_name)

                # Display each uploaded image with a fixed size (e.g., 300px width)
                st.image(file_path, caption=f"Image: {file_name}", use_column_width=False, width=300)

                # Provide a download button for each image
                with open(file_path, "rb") as file:
                    btn = st.download_button(
                        label=f"Download {file_name}",
                        data=file,
                        file_name=file_name,
                        mime="image/jpeg" if file_name.endswith(('.jpg', '.jpeg')) else "image/png"
                    )

        else:
            st.warning("No images uploaded yet.")
    else:
        st.warning("No images directory found.")


# Function to validate phone number
def is_valid_phone(phone_number):
    return len(phone_number) == 12 and phone_number.isdigit()


# Main Streamlit application
def main():
    # Create a session state variable for login status
    if 'login_successful' not in st.session_state:
        st.session_state.login_successful = False

    if 'name' not in st.session_state:
        st.session_state.name = ""

    if 'aadhaar_first_4_digits' not in st.session_state:
        st.session_state.aadhaar_first_4_digits = ""

    st.title("Image Upload and Preview")

    # Sidebar menu with options for Login, Upload Image, and Admin
    with st.sidebar:
        selected = st.radio("Select Section", ["Login", "Upload Image", "Admin"])

    if selected == "Login":
        st.subheader("Login Section")
        # Collect user input for login
        name = st.text_input("Enter your Name:")
        phone_number = st.text_input("Enter your Adhaar Card Number:", type="password")
        aadhaar_first_4_digits = st.text_input("Enter the first 4 digits of your Aadhaar card:", type="password")

        if st.button("Login"):
            if name and is_valid_phone(phone_number) and len(aadhaar_first_4_digits) == 4 and aadhaar_first_4_digits.isdigit():
                # Save name, Aadhaar first 4 digits, and phone to session state
                st.session_state.name = name
                st.session_state.aadhaar_first_4_digits = aadhaar_first_4_digits
                st.session_state.login_successful = True  # Mark login as successful
                st.success("Login Successful!")

            else:
                if not name:
                    st.error("Name is required.")
                if not is_valid_phone(phone_number):
                    st.error("Invalid Adhaar Card Number. It must be 12 digits.")
                if len(aadhaar_first_4_digits) != 4 or not aadhaar_first_4_digits.isdigit():
                    st.error("Invalid first 4 digits of Aadhaar. It must be 4 digits.")

    elif selected == "Upload Image":
        if not st.session_state.login_successful:
            st.warning("Please log in first to continue.")
        else:
            st.subheader("Upload an Image")
            # Upload an image
            uploaded_file = st.file_uploader("Choose an image to upload", type=["jpg", "jpeg", "png"])

            if uploaded_file is not None:
                # Show a preview of the uploaded image
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

                # Save the image when the submit button is clicked
                if st.button("Submit"):
                    # Save the uploaded image to the local system with the customer's Aadhaar first 4 digits
                    file_path = save_image(uploaded_file, st.session_state.aadhaar_first_4_digits, st.session_state.name)
                    st.success(f"Image saved successfully at {file_path}")

    elif selected == "Admin":
        # Check if the user is logged in before accessing the Admin section
        if not st.session_state.login_successful:
            st.warning("You need to log in first to access the Admin page.")
        else:
            # Ask for the Aadhaar first 4 digits when accessing Admin section
            aadhaar_first_4_digits = st.text_input("Enter the first 4 digits of your Aadhaar card to access your images:", type="password")

            if aadhaar_first_4_digits:
                # Check if the entered first 4 digits are correct
                if aadhaar_first_4_digits == st.session_state.aadhaar_first_4_digits:
                    st.subheader("Admin Section")
                    # Display the images uploaded in the user's specific folder
                    display_uploaded_images(aadhaar_first_4_digits)
                else:
                    st.error("Invalid Aadhaar first 4 digits. Please try again.")
            else:
                st.warning("Please enter the first 4 digits of your Aadhaar card to access the Admin page.")


if __name__ == "__main__":
    main()


# natha ivor sequeira 1234