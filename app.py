import streamlit as st
import requests
from datetime import datetime
import pandas as pd

st.title("TaxiFareModel front")

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions.
''')

st.markdown('''
## Ride Parameters
''')

pickup_date = st.date_input("Pickup date")
pickup_time = st.time_input("Pickup time")
pickup_datetime = datetime.combine(pickup_date, pickup_time)

pickup_longitude = st.number_input("Pickup longitude", value=-50.26)
pickup_latitude = st.number_input("Pickup latitude", value=20.2)
dropoff_longitude = st.number_input("Dropoff longitude", value=-50.26)
dropoff_latitude = st.number_input("Dropoff latitude", value=20.2)
passenger_count = st.number_input("Passenger count", min_value=1, max_value=20, value=1)

mapp = pd.DataFrame(
    {
    'lat': [pickup_latitude, dropoff_latitude],
    'lon': [pickup_longitude, dropoff_longitude]
}
    )
st.markdown("### Pickup & Dropoff Map")
st.map(mapp)



st.markdown('''
## let's call our API in order to retrieve a prediction.
''')

url = 'https://taxifare.lewagon.ai/predict'

if st.button("Predict fare"):
    params = {
        "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        prediction = response.json().get("fare", "No predict")
        st.success(f"Predicted fare: ${prediction:.2f}")
    else:
        st.error("Failed to get a predict. check your inputs again .")
