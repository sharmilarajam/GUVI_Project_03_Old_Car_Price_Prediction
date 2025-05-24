import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ------------------- Load the Trained Model -------------------
with open("car_price_model.pkl", "rb") as f:
    model = pickle.load(f)

# ------------------- Streamlit App UI -------------------
st.title("Used Car Price Prediction")

with st.form("car_input_form"):
    transmission = st.selectbox("Transmission (0=Manual, 1=Automatic)", [0, 1])
    model_code = st.number_input("Model (numeric code)", min_value=0)
    year = st.number_input("Year of Manufacture", min_value=1900, max_value=2025, value=2015)
    city = st.selectbox("City (numeric code)", [0, 1, 2, 3, 4, 5])
    ft = st.number_input("ft (feature)", min_value=0)
    bt = st.number_input("bt (feature)", min_value=0)
    ownership = st.selectbox("Ownership (1=1st, 2=2nd, etc.)", [1, 2, 3, 4])
    kms_driven = st.number_input("Kms Driven", min_value=0)
    engine_type = st.number_input("Engine Type (numeric code)", min_value=0)

    submitted = st.form_submit_button("Submit")

# ------------------- Prediction -------------------
if submitted:
    # Build input DataFrame — column names must match training data
    input_data = pd.DataFrame([{
        "transmission": transmission,
        "model": model_code,
        "year_of_manufacture": year,
        "city": city,
        "ft": ft,
        "bt": bt,
        "ownership": ownership,
        "kms_driven": kms_driven,
        "engine_type": engine_type
    }])

    # encodeing
    with open("label_encoders.pkl", "rb") as f:
        encoders = pickle.load(f)

# Your single-row input DataFrame (already constructed as `input_data`)
    for col, le in encoders.items():
        input_data[col] = le.transform(input_data[col].astype(str))

# Convert to array for prediction
    input_array = input_data.to_numpy().reshape(1, -1)

    
    # scaling (0-1)

    # Predict log(price), then inverse transform to actual price
    pred = model.predict(input_data.values)

    # Show result
    st.success(f"Estimated Car Price: ₹ {pred}")
