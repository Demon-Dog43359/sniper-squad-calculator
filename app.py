import streamlit as st
import joblib

sniperRifle = {
    "Timberwolf":{"model":"model.pkl", "poly":"poly.pkl"},
}


st.title("Squad Hold Calculator")

rifle = st.selectbox("Sniper Rifle", list(sniperRifle.keys()))
reg = joblib.load(sniperRifle[rifle]["model"])
poly = joblib.load(sniperRifle[rifle]["poly"])

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
