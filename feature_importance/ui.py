import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# MySQL DB connection details
DB_HOST = "localhost"
DB_PORT = "3306"
DB_USER = "root"
DB_PASSWORD = "123456"
DB_NAME = "car"

# Connect to MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Fetch distinct values from the database for the dropdowns
def fetch_dropdown_options():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            # Query to fetch distinct values for dropdowns
            cursor.execute("SELECT DISTINCT transmission FROM price_prediction;")
            transmissions = cursor.fetchall()

            cursor.execute("SELECT DISTINCT model FROM price_prediction;")
            models = cursor.fetchall()

            cursor.execute("SELECT DISTINCT year_of_manufacture FROM price_prediction;")
            years = cursor.fetchall()

            cursor.execute("SELECT DISTINCT City FROM price_prediction;")
            cities = cursor.fetchall()

            cursor.close()
            connection.close()

            # Return the options as lists of values
            return {
                "transmissions": [row["transmission"] for row in transmissions],
                "models": [row["model"] for row in models],
                "years": [row["year_of_manufacture"] for row in years],
                "cities": [row["City"] for row in cities]
            }
        except Error as e:
            st.error(f"Failed to fetch dropdown options: {e}")
            return None
    return None

# Insert data
def insert_car_info(data):
    query = """
    INSERT INTO price_prediction(
        transmission, model, year_of_manufacture, City, ft, bt,
        Ownership, kms_driven, engine_type
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, tuple(data.values()))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            st.error(f"Failed to insert data: {e}")
            return False
    return False

# Streamlit UI
st.title("Used Car Information Form")

# Fetch available options from the database
options = fetch_dropdown_options()

if options:
    with st.form("car_input_form"):
        # Use options fetched from the database for the selectboxes
        transmission = st.selectbox("Transmission (0=Manual, 1=Automatic)", options["transmissions"])
        model = st.selectbox("Model", options["models"])
        year = st.selectbox("Year of Manufacture", options["years"])
        city = st.selectbox("City", options["cities"])
        ft = st.number_input("ft (feature)", min_value=0)
        bt = st.number_input("bt (feature)", min_value=0)
        ownership = st.selectbox("Ownership (1=1st, 2=2nd, etc.)", [1, 2, 3, 4])
        kms_driven = st.number_input("Kms Driven", min_value=0)
        engine_type = st.number_input("Engine Type (numeric code)", min_value=0)

        submitted = st.form_submit_button("Submit")

    if submitted:
        input_data = {
            "transmission": transmission,
            "model": model,
            "year_of_manufacture": year,
            "city": city,
            "ft": ft,
            "bt": bt,
            "ownership": ownership,
            "kms_driven": kms_driven,
            "engine_type": engine_type
        }

        if insert_car_info(input_data):
            st.success("Data inserted successfully!")
            st.write("You entered:")
            st.dataframe(pd.DataFrame([input_data]))
        else:
            st.error("Failed to insert data.")
else:
    st.error("Failed to load dropdown options from the database.")
