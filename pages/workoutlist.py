import streamlit as st

from menu import menu
def set_workout():
    st.session_state.workout=st.session_state._work

menu()
st.title("Workout Library")
st.selectbox(
    "Select your workout:",
    ["None", "Basic", "Advanced", "Open"],
    key="_work",
    on_change=set_workout,
)
if st.button("start"):
    if st.session_state.workout != "None" and st.session_state.workout != None:
        st.switch_page("pages/workout.py")
    else:
        st.warning("Please select a workout")


tab1, tab2, tab3 = st.tabs(["Basic Workout", "Advanced Workout", "Open Workout"])

with tab1:
    st.header("Basic Workout")
    st.markdown("""
- Warm up
  - 10 bicup curls
  - 10 second rest
- Main set
  - 20 bicup curls
  - 1 minute rest
""")
with tab2:
    st.header("Advanced Workout")
    st.markdown("""
- Warm up
  - 50 bicup curls
  - 10 second rest
- Main set
  - 100 bicup curls
  - 1 minute rest
""")
with tab3:
    st.header("Open Workout")
    st.markdown("""
For this workout, the timer will count up and track how many bicup curls are done.
""")