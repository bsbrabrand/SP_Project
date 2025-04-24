import streamlit as st
from HRfunc import connect_to_heart_rate_sensor, disconnect_from_heart_rate_sensor
from menu import menu
import asyncio
import time

st.title("Bluetooth Sensor Setup")
menu()

if st.session_state.connected == False:
    st.write("No heart rate sensor connected.")
    if st.button("Press to connect to bluetooth device"):
        try:
            with st.spinner("Attempting to connect", show_time=True):
                st.session_state.client=asyncio.run(connect_to_heart_rate_sensor())
                st.write(st.session_state.client)
            if st.session_state.client != None:
                st.success("HR Monitor Connected!")
                st.session_state.connected=True
            time.sleep(3)
            st.rerun()
        except TimeoutError:
            st.warning("Unable to connect. Timeout error")
else:
    st.write("Heart rate sensor connected")
    if st.button("Press to disconnect from bluetooth device"):
        with st.spinner("Disconnecting", show_time=True):
            asyncio.run(disconnect_from_heart_rate_sensor(st.session_state.client,st.session_state.ID))
            st.success("HR Monitor Disconnected")
            st.session_state.connected=False
        time.sleep(3)
        st.rerun()