import streamlit as st
import joblib


# ----------------------------------------------------------------------------------------------------
# Database of all the weapons and movement options
database = {
       "Western Private Military Contractors":{

            "Sniper Rifles" : { 
                "Timberwolf":{
                    "vertical_model":None,
                    "vertical_poly":None,

                     "horizontal_model":"Models + Polynomials/timberwolf_horizontal_model.pkl", 
                     "horizontal_poly":"Models + Polynomials/timberwolf_horizontal_poly.pkl"
                     }, 
            },

            "HAT" : {
                "RPG-1" : {
                    "vertical_model":None,
                    "vertical_poly":None,
                    
                    "horizontal_model":None, 
                    "horizontal_poly":None,
                    },
            }, 
       },


       "People's Liberation Army": {

            "Sniper Rifles":{
                "Sniper 1": {
                    "vertical_model":None,
                    "vertical_poly":None,
                
                    "horizontal_model":None, 
                    "horizontal_poly":None,
                },
            }, 

            "HAT":{
                "RPG-1":{
                    "vertical_model":None,
                    "vertical_poly":None,
                
                    "horizontal_model":None, 
                    "horizontal_poly":None,
                },
            },
       },
}

movement_options = {
    "Slow Crouch": 0,
    "Fast Crouch": 1,
    "Jog": 2,
    "Full Sprint": 3
}

# ----------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------
# Website Display and Weapon Selection
st.title("Squad Hold Calculator")
faction = st.selectbox("Faction", list(database.keys()))
kit = st.selectbox("Kit", list(database[faction].keys()))
weapon = st.selectbox("Weapon", list(database[faction][kit].keys()))
selected_weapon = database[faction][kit][weapon]

if selected_weapon["horizontal_model"] is None:
    st.warning(f"Error: {weapon} is not supported currently")
    st.stop()


distance = st.number_input(
    "Distance (m)",
    min_value=100,
    max_value=1000,
    step=5,
    value=300
)

if distance > 500:
        st.warning("Model currently supports 100–500 m only.")
# -----------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------
# Model Loading
horizontal_reg = joblib.load(selected_weapon["horizontal_model"])
horizontal_poly = joblib.load(selected_weapon["horizontal_poly"])


choice = st.selectbox("Target Movement", movement_options.keys())
movement = movement_options[choice]
# -----------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------
# Prediction
if st.button("Calculate"):

    vertical_hold=0

    X = horizontal_poly.transform([[distance, movement]])

    horizontal_hold = horizontal_reg.predict(X)[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
             label="Vertical Hold",
             value = f"{vertical_hold:.2f} mil"
        )

    with col2:
        st.metric(
             label="Horizontal Hold",
             value = f"{horizontal_hold:.2f} mil"
        )
# ------------------------------------------------------------------------------------------------------------
