import streamlit as st
import time
import asyncio
from HRfunc import get_heart_rate
from data import datastore

def main():
    # Setup workout values
    if "heart_rate_trend" not in st.session_state:
        st.session_state.heart_rate_trend = []
    if "end_workout" not in st.session_state:
        st.session_state.end_workout = False

    #Check for errors
    if not st.session_state.connected:
        st.error("No heart rate sensor connected.")
        time.sleep(2)
        st.switch_page("pages/home.py")
    elif st.session_state.workout is None:
        st.warning("No workout selected, redirecting...")
        time.sleep(2)
        st.switch_page("pages/workoutlist.py")
    else:

        # Layout containers
        static_ui = st.container()
        graph = st.empty()

        # Static Part of website
        with static_ui:
            st.title("Heart Rate Monitor Dashboard")
            st.write("Click the button below to end your workout.")
            if st.button("End Workout", key="end_workout_button"):
                st.session_state.end_workout = True

        # Dynamic Part of Website
        while not st.session_state.end_workout:
            #record current time
            oldtime = time.time()-st.session_state.start_time
            # Get new heart rate reading
            try:
                hr = asyncio.run(get_heart_rate(st.session_state.client))
                st.session_state.heart_rate_trend.append(hr)
            except Exception as e:
                st.error(f"Error reading heart rate: {e}")
                time.sleep(2)
                st.switch_page("pages/home.py")

            # Update only the graph area
            with graph.container():
                st.write(f"Your current heart rate: {int(hr)} bpm")
                st.line_chart(st.session_state.heart_rate_trend)
                elapsed = int(time.time() - st.session_state.start_time)
                st.write(f"Timer: {elapsed} seconds")

            #delay if needed so it doesn't update faster than 1/s
            while time.time()-st.session_state.start_time < (int(oldtime)+1):
                time.sleep(0.001)

        # Save data and end workout
        avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
        tottime = time.time() - st.session_state.start_time
        totalreps = 0  # Placeholder

        st.session_state.WO_list.append(
            datastore(tottime, avgHR, totalreps, st.session_state.workout)
        )
        #reset values so next workout starts fresh
        st.session_state.heart_rate_trend = []
        st.session_state.end_workout = False
        st.session_state.workout = "None"

        #switch to page with workout summaries
        st.switch_page("pages/history.py")

if __name__ == "__main__":
    main()