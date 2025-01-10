import streamlit as st
import sqlite3

# Connect to the SQLite database or create it if it doesn't exist
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create a table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL
    )
''')
conn.commit()

# Streamlit App Interface
st.title("Simple Database App")

st.subheader("Enter User Details")

# Input fields for number and name
number = st.text_input("Enter a 12-digit number")
name = st.text_input("Enter your name")

# Submit button to save data to the database
if st.button("Submit"):
    if len(number) == 12 and number.isdigit() and name:
        try:
            c.execute("INSERT INTO user_data (number, name) VALUES (?, ?)", (number, name))
            conn.commit()
            st.success("Data added successfully!")
        except sqlite3.IntegrityError:
            st.error("Number already exists in the database.")
    else:
        st.error("Please enter a valid 12-digit number and name.")

# Display the data from the database
st.subheader("Stored Data")
c.execute("SELECT * FROM user_data")
rows = c.fetchall()
for row in rows:
    st.write(f"ID: {row[0]}, Number: {row[1]}, Name: {row[2]}")
