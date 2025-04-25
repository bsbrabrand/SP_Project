import streamlit as st

def menu():
    st.sidebar.page_link("pages/connect_sensor.py", label="Connect HR Monitor")
    st.sidebar.page_link("pages/workoutlist.py", label="Workout Library")
    st.sidebar.page_link("pages/history.py", label="Workout History")
    # st.sidebar.page_link(
    #     "pages/workout.py",
    #     label="Start a Workout",
    #     disabled=st.session_state.connected != True,
    # )