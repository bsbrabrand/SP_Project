import streamlit as st
from menu import menu
import time
import asyncio
from HRfunc import connect_to_heart_rate_sensor

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
st.session_state.WO_list = []

st.title("Heart Rate Workout Monitor Home")
st.write("This project was made by Bennett Brabrand and Riley Fry for ME 5194 at The Ohio State University. To begin, please connect a heart rate monitor from the menu.")
st.write("To begin, connect a heart rate monitor using the button below")
if st.button("Press to connect to bluetooth device"):
        try:
            with st.spinner("Attempting to connect", show_time=True):
                st.session_state.client=asyncio.run(connect_to_heart_rate_sensor())
                st.write(st.session_state.client)
            if st.session_state.client != None:
                st.success("HR Monitor Connected!, redirecting...")
                st.session_state.connected=True
            time.sleep(3)
            st.switch_page("pages/workoutlist.py")
        except TimeoutError:
            st.warning("Unable to connect. Timeout error")