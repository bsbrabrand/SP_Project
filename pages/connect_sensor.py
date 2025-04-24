import streamlit as st
from HRfunc import connect_to_heart_rate_sensor, disconnect_from_heart_rate_sensor
from menu import menu

st.title("Bluetooth Sensor Setup")
menu()

if st.session_state.connected == False:
    st.write("No heart rate sensor connected.")
    if st.button("Press to connect to bluetooth device"):
        try:
            with st.spinner("Attempting to connect", show_time=True):
                st.session_state.client=connect_to_heart_rate_sensor()
                st.write(st.session_state.client)
                if st.session_state.client != None:
                    st.success("HR Monitor Connected!")
                    st.session_state.connected=True
        except TimeoutError:
            st.warning("Unable to connect. Timeout error")
else:
    st.write("Heart rate sensor connected")
    if st.button("Press to disconnect from bluetooth device"):
        disconnect_from_heart_rate_sensor()