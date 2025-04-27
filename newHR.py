import streamlit as st
import time
import asyncio
from HRfunc import get_heart_rate
from data import datastore
from datatransferpc import receive_data_from_pi
import socket

async def get_heart_rate_and_reps(client, conn):
    """Retrieve heart rate and rep count data simultaneously."""
    # Start heart rate data retrieval
    try:
        heart_rate = await get_heart_rate(client)  # Get heart rate asynchronously
        # Receive rep count from Raspberry Pi asynchronously
        total_reps = await asyncio.to_thread(receive_reps_from_pi, conn)
    except Exception as e:
        st.error(f"Error: {e}")
        return None, None
    return heart_rate, total_reps

def receive_reps_from_pi(conn):
    """Receive rep count from Raspberry Pi in a blocking manner."""
    return conn.recv(1024).decode('utf-8')

def main():
    # Setup workout values
    if "heart_rate_trend" not in st.session_state:
        st.session_state.heart_rate_trend = []
    if "end_workout" not in st.session_state:
        st.session_state.end_workout = False
    if "total_reps" not in st.session_state:
        st.session_state.total_reps = 0

    # Check for errors
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

        # Start socket
        pc_ip = "192.168.1.4"  # Replace with your PC's IP address
        pc_port = 65432  # Replace with the port number you want to use
        conn = receive_data_from_pi(pc_ip, pc_port)

        # Static Part of website
        with static_ui:
            st.title("Heart Rate Monitor Dashboard")
            st.write("Click the button below to end your workout.")
            if st.button("End Workout", key="end_workout_button"):
                st.session_state.end_workout = True

        # Dynamic Part of Website
        while not st.session_state.end_workout:
            # Record current time
            oldtime = time.time() - st.session_state.start_time
            # Get heart rate and rep count asynchronously
            heart_rate, total_reps = asyncio.run(get_heart_rate_and_reps(st.session_state.client, conn))
            
            if heart_rate is None or total_reps is None:
                break  # Handle any errors or termination of the loop

            # Update the heart rate trend and rep count
            st.session_state.heart_rate_trend.append(heart_rate)
            st.session_state.total_reps = total_reps

            # Update only the graph area
            with graph.container():
                st.write(f"Your current heart rate: {int(heart_rate)} bpm")
                st.line_chart(st.session_state.heart_rate_trend)
                elapsed = int(time.time() - st.session_state.start_time)
                st.write(f"Timer: {elapsed} seconds")
                st.write(f"Total Reps: {st.session_state.total_reps}")  # Display the current rep count

            # Delay if needed so it doesn't update faster than 1/s
            while time.time() - st.session_state.start_time < (int(oldtime) + 1):
                time.sleep(0.001)

        # Save data and end workout
        avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
        tottime = time.time() - st.session_state.start_time
        totalreps = st.session_state.total_reps
        conn.close()

        st.session_state.WO_list.append(
            datastore(tottime, avgHR, totalreps, st.session_state.workout)
        )
        # Reset values so next workout starts fresh
        st.session_state.heart_rate_trend = []
        st.session_state.end_workout = False
        st.session_state.workout = "None"

        # Switch to page with workout summaries
        st.switch_page("pages/history.py")

if __name__ == "__main__":
    main()
