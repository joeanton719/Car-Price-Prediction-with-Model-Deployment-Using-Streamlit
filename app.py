import streamlit as st
import numpy as np
import pandas as pd
import pickle

st.title("Let's Predict Used Car Prices!")

@st.cache
def get_df(filename):
    df = pd.read_csv(filename)
    return df


df = get_df("final.csv")

left_column, mid_column, right_column = st.columns(3)


brand = left_column.selectbox(
    "What is the Brand of your Car?",
     df['brand'].unique()
     )


model = mid_column.selectbox(
    "What is the Model of your Car?",
     df.query(f'brand == "{brand}"')['model'].unique()
     )


year = right_column.selectbox(
    "What is the Model of your Car?",
     df['year'].sort_values(ascending = False).unique()
     )


fuel = left_column.selectbox(
    "Fuel Type",
     df['fuel_type'].unique()
     )


transmission = mid_column.selectbox(
    "Car Transmission",
     df['transmission'].unique()
     )


seats = right_column.selectbox(
    "Seating Capacity",
     df.query(f'model == "{model}"')['seats'].sort_values().unique()
     )


owner = left_column.selectbox(
    "Are you the Original Owner (First-Hand or Second-Hand) Car?",
     df['is_first_owner'].unique()
     )


loc = mid_column.selectbox(
    "Location",
     df['location'].unique()
    )

distance = right_column.slider( 
        "Total Distance Driven in Kilometers", 
        min_value = 0, 
        max_value = 750000, 
        value = 0, 
        step = 50
    )

mileage = left_column.slider( 
        "Mileage (km/l)", 
        min_value = 0.0, 
        max_value = 50.0, 
        value = 5.0, 
        step = 0.1
    )

engine = mid_column.slider( 
        "Engine CC", 
        min_value = 600, 
        max_value = 5500, 
        value = 650, 
        step = 10
    )

power = right_column.slider( 
        "Brake Horse Power (BHP)", 
        min_value = 30.0, 
        max_value = 500.0, 
        value = 50.0, 
        step = 0.1
    )



cat_model = pickle.load(open('cat_pipe.pkl', 'rb'))


features = pd.DataFrame({
        "brand" : brand,
        "model" : model, 
        "milage_kmpl" : mileage,
        "location" : loc, 
        "year" : year, 
        "kilometers_driven" : distance,
        "fuel_type" : fuel, 
        "transmission" : transmission,
        "is_first_owner" : owner, 
        "engine" : engine, 
        "power" : power,
        "seats" : seats
    }, index=[0])


prediction = cat_model.predict(features)[0]

pressed = mid_column.button('Predict Car Price')

if pressed:
  st.subheader(f"This Car is predicted to cost around {prediction:,.0f} INR")
  st.balloons()
  