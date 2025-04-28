import time
import asyncio
import streamlit as st
from HRfunc import connect_ble_client, start_heart_rate_notifications, stop_ble_client, parse_hr_data
from data import datastore
from datatransferpc import receive_data_from_pi

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

async def get_heart_rate_and_reps(client, conn):
    """Get values for both heart rate and number of reps"""
    try:
        heart_rate = await get_heart_rate(client)
        total_reps = await asyncio.to_thread(receive_reps_from_pi, conn)
        #Since multiple reps values can be sent in the time it takes to read a heart rate, take the most recent value only
        tot_reps = total_reps.split(" ")[-2] # format is "# # " so second to last element is the number
    except Exception as e:
        st.error(f"Error: {e}")
        return None, None
    return heart_rate, tot_reps

def receive_reps_from_pi(conn):
    """Read in the value of reps from the Raspeberry Pi"""
    return conn.recv(1024).decode('utf-8')

def main():
    # Setup workout default values
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
        st.switch_page("home.py")
    elif st.session_state.workout is None:
        st.warning("No workout selected, redirecting...")
        time.sleep(2)
        st.switch_page("pages/workoutlist.py")
    else:
        # Layout containers
        static_ui = st.container()
        graph = st.empty()

        # Start socket
        pc_ip = "192.168.1.4"  #PC's IP address
        pc_port = 65432  # random port number that worked when we tested with it
        if not st.session_state.end_workout:
            with st.spinner("Connecting to Raspberry Pi"):
                conn = receive_data_from_pi(pc_ip, pc_port) #set up connection
            
        # Static Part of website
        with static_ui:
            st.title("Heart Rate Monitor Dashboard")
            st.write("Click the button below to end your workout.")
            if st.button("End Workout", key="end_workout_button"): #if button is clicked
                st.session_state.end_workout = True

        # Dynamic Part of Website
        while not st.session_state.end_workout:
            # Record current time
            #oldtime = time.time() - st.session_state.start_time
            # Get heart rate and rep count using asyncio
            heart_rate, total_reps = asyncio.run(get_heart_rate_and_reps(st.session_state.client, conn))
            
            if heart_rate is None or total_reps is None:
                break  # exit the loop if no data

            # update the heart rate trend list and rep count value
            st.session_state.heart_rate_trend.append(heart_rate)
            st.session_state.total_reps = total_reps

            # Update only the graph area of the website here
            with graph.container():
                st.write(f"Your current heart rate: {int(heart_rate)} bpm")
                st.line_chart(st.session_state.heart_rate_trend)
                elapsed = int(time.time() - st.session_state.start_time)
                st.write(f"Timer: {elapsed} seconds")
                if st.session_state.workout == "Basic":
                    st.write(f"Total Reps: {st.session_state.total_reps}/10")
                    if int(st.session_state.total_reps)==10:
                        st.session_state.end_workout=True
                elif st.session_state.workout == "Advanced":
                    st.write(f"Total Reps: {st.session_state.total_reps}/50")
                    if int(st.session_state.total_reps)==50:
                        st.session_state.end_workout=True
                else:
                    st.write(f"Total Reps: {st.session_state.total_reps}")

                # Delay if needed so it doesn't update faster than 1/s
               # while time.time() - st.session_state.start_time < (int(oldtime) + 1):
                   # time.sleep(0.001)

        # Save data and end workout
        avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
        tottime = time.time() - st.session_state.start_time
        totalreps = st.session_state.total_reps
        #conn.close()

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