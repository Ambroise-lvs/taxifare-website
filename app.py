import streamlit as st
import datetime
import requests
import pydeck as pdk
import pandas as pd

# ----------- PAGE CONFIG -----------
st.set_page_config(
    page_title="NYC Taxi Fare Predictor",
    page_icon="🚕",
    layout="centered"
)

# ----------- TITLE -----------
st.markdown(
    """
    <h1 style='text-align: center; color: #FFD700;'>
        🚕 NYC Taxi Fare Prediction
    </h1>
    <p style='text-align: center; font-size: 18px; color: #ccc;'>
        Enter your ride details to estimate the taxi fare in New York City.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

### DATE + TIME IN 2 COLUMNS
st.subheader("📅 Ride details")
col1, col2 = st.columns(2)

with col1:
    d = st.date_input("Date", datetime.date(2014, 7, 6))

with col2:
    t = st.time_input("Time", datetime.time(19, 18, 0))

ride_datetime = f"{d} {t}"


### PICKUP COORDS IN 2 COLUMNS
st.subheader("📍 Pickup coordinates")
col1, col2 = st.columns(2)

with col1:
    pickup_longitude = st.number_input("Longitude", value=-73.950655, format="%.6f")

with col2:
    pickup_latitude = st.number_input("Latitude", value=40.783282, format="%.6f")


### DROPOFF COORDS IN 2 COLUMNS
st.subheader("🎯 Dropoff coordinates")
col1, col2 = st.columns(2)

with col1:
    dropoff_longitude = st.number_input("Longitude", value=-73.984365, format="%.6f")

with col2:
    dropoff_latitude = st.number_input("Latitude", value=40.769802, format="%.6f")


### PASSENGER COUNT
st.subheader("🧍 Passengers")
passenger_count = st.number_input("Passenger count", min_value=1, max_value=8, value=1)

# ----------- MAP DISPLAY-----------
st.subheader("🗺️ Map")
map = pd.DataFrame([[pickup_latitude, pickup_longitude], [dropoff_latitude, dropoff_longitude]], columns=['lat', 'lon'])
st.map(map, zoom=12)

# ----------- API CALL -----------
url = 'https://taxifare.lewagon.ai/predict'

params = {
    "pickup_datetime": str(ride_datetime),
    "pickup_longitude": float(pickup_longitude),
    "pickup_latitude": float(pickup_latitude),
    "dropoff_longitude": float(dropoff_longitude),
    "dropoff_latitude": float(dropoff_latitude),
    "passenger_count": int(passenger_count)
}

st.markdown("---")

# ----------- ACTION BUTTON -----------
if st.button("🔮 Predict fare"):
    with st.spinner("Predicting fare..."):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            fare = response.json()["fare"]
            st.success(f"💰 **Estimated fare: ${fare:.2f}**")
        else:
            st.error("API error: Unable to retrieve prediction.")

