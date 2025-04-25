import streamlit as st
from menu import menu

st.title("Workout History")
menu()
if len(st.session_state.WO_list) == 0:
    st.write("No workouts recorded")
else:
    for WO in st.session_state.WO_list:
        st.write(WO)
        st.write("\n")