import streamlit as st
from menu import menu

############### setup webpage #############################
st.set_page_config(
    page_title="Heart Rate Dashboard",
    page_icon="♥️",
    layout="wide",
)
hide_default_format = """
    <style>
    #MainMenu {visibility: hidden; }
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_default_format, unsafe_allow_html=True)

#Global variables
st.session_state.connected = False
st.session_state.ID = "00002a37-0000-1000-8000-00805f9b34fb"
st.session_state.workout = None

menu()

st.title("Heart Rate Workout Monitor Home")
st.write("This project was made by Bennett Brabrand and Riley Fry for ME 5194 at The Ohio State University. To begin, please connect a heart rate monitor from the menu.")