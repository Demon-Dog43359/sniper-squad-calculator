import streamlit as st
import joblib

database = {
       "Western Private Military Contractors":{
              kits = {
                     "Sniper Rifles" : { 
                         "Timberwolf":{"model":"Models + Polynomials/timberwolf_model.pkl", "poly":"Models + Polynomials/timberwolf_poly.pkl"}, 
                     },
                      "HAT" : {
                          "RPG-1" : {"model":"Models + Polynomials/timberwolf_model.pkl", "poly":"Models + Polynomials/timberwolf_poly.pkl"},
                      },
              }, 
       },
       "People's Liberation Army": {
              kits = {
                     "Sniper Rifles":{
                            "Sniper 1": {"model": "Models + Polynomials/timberwolf_model.pkl", "poly":"Models + Polynomials/timberwolf_poly.pkl"},
                     }, 
                     "HAT":{
                            "RPG-1":{"model": "Models + Polynomials/timberwolf_model.pkl", "poly":"Models + Polynomials/timberwolf_poly.pkl"},
                     }
              }
       }
}

st.title("Squad Hold Calculator")
faction = st.selectbox("Faction", list(factions.keys()))
kit = st.selectbox("Kit", list(kits.keys()))
weapon = st.selectbox("Weapon", list(kits[kit].keys()))
reg = joblib.load(database[faction][kit][weapon]["model"])
poly = joblib.load(database[faction][kit][weapon]["poly"])

if kit != "Sniper Rifles":
    st.warning("Error: Data Available only for Sniper Rifles now")

distance = st.number_input(
    "Distance (m)",
    min_value=100,
    max_value=1000,
    step=10,
    value=300
)

if distance > 500:
        st.warning("Model currently supports 100–500 m only.")

movement_options = {
    "Slow Crouch": 0,
    "Fast Crouch": 1,
    "Jog": 2,
    "Full Sprint": 3
}

choice = st.selectbox("Target Movement", movement_options.keys())
movement = movement_options[choice]

if st.button("Calculate"):
    
    X = poly.transform([[distance, movement]])

    mil = reg.predict(X)[0]

    st.metric(
    label="Hold",
        value=f"{mil:.2f} mil"
    )
