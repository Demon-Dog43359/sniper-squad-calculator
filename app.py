import streamlit as st
import joblib

# Load the model
reg = joblib.load("model.pkl")
poly = joblib.load("poly.pkl")

st.title("Squad Timberwolf Hold Calculator")

distance = st.number_input(
    "Distance (m)",
    min_value=100,
    max_value=2000,
    step=20,
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
