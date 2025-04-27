# import streamlit as st
# import time
# import asyncio
# from HRfunc import get_heart_rate
# from data import datastore
# from datatransferpc import receive_data_from_pi

# async def get_reps(conn):
#     """Continuously receive the rep count from the Raspberry Pi."""
#     try:
#         while True:
#             total_reps = conn.recv(1024).decode('utf-8')
#             if total_reps:
#                 st.session_state.total_reps = total_reps
#             await asyncio.sleep(1)  # Sleep to avoid blocking other tasks
#     except Exception as e:
#         st.error(f"Error receiving data from Pi: {e}")

# def main():
#     # Setup workout values
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False

#     #Check for errors
#     if not st.session_state.connected:
#         st.error("No heart rate sensor connected.")
#         time.sleep(2)
#         st.switch_page("pages/home.py")
#     elif st.session_state.workout is None:
#         st.warning("No workout selected, redirecting...")
#         time.sleep(2)
#         st.switch_page("pages/workoutlist.py")
#     else:

#         # Layout containers
#         static_ui = st.container()
#         graph = st.empty()

#         #start socket
#         pc_ip = "192.168.1.4"  # Replace with your PC's IP address
#         pc_port = 65432  # Replace with the port number you want to use
#         conn = receive_data_from_pi(pc_ip, pc_port)

#         # Static Part of website
#         with static_ui:
#             st.title("Heart Rate Monitor Dashboard")
#             st.write("Click the button below to end your workout.")
#             if st.button("End Workout", key="end_workout_button"):
#                 st.session_state.end_workout = True

#         # Dynamic Part of Website
#         while not st.session_state.end_workout:
#             #record current time
#             oldtime = time.time()-st.session_state.start_time
#             # Get new heart rate reading
#             try:
#                 hr = asyncio.run(get_heart_rate(st.session_state.client,conn))
#                 st.session_state.heart_rate_trend.append(hr)
#             except Exception as e:
#                 st.error(f"Error reading heart rate: {e}")
#                 time.sleep(2)
#                 st.switch_page("pages/home.py")

#             # Update only the graph area
#             with graph.container():
#                 st.write(f"Your current heart rate: {int(hr)} bpm")
#                 st.line_chart(st.session_state.heart_rate_trend)
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")
#                 st.write(f"Current reps {st.session_state.total_reps}")

#             #delay if needed so it doesn't update faster than 1/s
#             while time.time()-st.session_state.start_time < (int(oldtime)+1):
#                 time.sleep(0.001)

#         # Save data and end workout
#         avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#         tottime = time.time() - st.session_state.start_time
#         totalreps = st.session_state.total_reps
#         conn.close()

#         st.session_state.WO_list.append(
#             datastore(tottime, avgHR, totalreps, st.session_state.workout)
#         )
#         #reset values so next workout starts fresh
#         st.session_state.heart_rate_trend = []
#         st.session_state.end_workout = False
#         st.session_state.workout = "None"
#         st.session_state.total_reps = 0

#         #switch to page with workout summaries
#         st.switch_page("pages/history.py")

# if __name__ == "__main__":
#     main()

### GOOD CODE, just only updates when a new rep and freezes when end workout button click
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
        tot_reps = total_reps.split(" ")[-1]
    except Exception as e:
        st.error(f"Error: {e}")
        return None, None
    return heart_rate, tot_reps

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


## bad code
# import streamlit as st
# import time
# import asyncio
# from HRfunc import get_heart_rate
# from data import datastore
# from datatransferpc import receive_data_from_pi
# import socket

# async def get_heart_rate_and_reps(client, conn):
#     """Retrieve heart rate and rep count data asynchronously."""
#     # Start heart rate data retrieval
#     try:
#         heart_rate = await get_heart_rate(client)  # Get heart rate asynchronously
#         # Receive rep count from Raspberry Pi asynchronously
#         total_reps = await asyncio.to_thread(receive_reps_from_pi, conn)
#     except Exception as e:
#         st.error(f"Error: {e}")
#         return None, None
#     return heart_rate, total_reps

# def receive_reps_from_pi(conn):
#     """Receive rep count from Raspberry Pi in a blocking manner."""
#     return conn.recv(1024).decode('utf-8')

# def main():
#     # Setup workout values
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "total_reps" not in st.session_state:
#         st.session_state.total_reps = 0
#     if "running" not in st.session_state:
#         st.session_state.running = False

#     # Check for errors
#     if not st.session_state.connected:
#         st.error("No heart rate sensor connected.")
#         time.sleep(2)
#         st.switch_page("pages/home.py")
#     elif st.session_state.workout is None:
#         st.warning("No workout selected, redirecting...")
#         time.sleep(2)
#         st.switch_page("pages/workoutlist.py")
#     else:
#         # Layout containers
#         static_ui = st.container()
#         graph = st.empty()

#         # Start socket
#         pc_ip = "192.168.1.4"  # Replace with your PC's IP address
#         pc_port = 65432  # Replace with the port number you want to use
#         conn = receive_data_from_pi(pc_ip, pc_port)

#         # Static Part of website
#         with static_ui:
#             st.title("Heart Rate Monitor Dashboard")
#             st.write("Click the button below to end your workout.")
#             if st.button("End Workout", key="end_workout_button"):
#                 st.session_state.end_workout = True
#                 st.session_state.running = False  # Stop the background task

#         # Start the background task when workout is active
#         if st.session_state.running and not st.session_state.end_workout:
#             # Record current time
#             oldtime = time.time() - st.session_state.start_time
#             # Get heart rate and rep count asynchronously
#             heart_rate, total_reps = asyncio.run(get_heart_rate_and_reps(st.session_state.client, conn))
            
#             if heart_rate is None or total_reps is None:
#                 st.session_state.running = False  # Stop if there's an error
#                 return  # Exit if an error occurs

#             # Update the heart rate trend and rep count
#             st.session_state.heart_rate_trend.append(heart_rate)
#             st.session_state.total_reps = total_reps

#             # Update only the graph area
#             with graph.container():
#                 st.write(f"Your current heart rate: {int(heart_rate)} bpm")
#                 st.line_chart(st.session_state.heart_rate_trend)
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")
#                 st.write(f"Total Reps: {st.session_state.total_reps}")  # Display the current rep count

#             # Delay if needed so it doesn't update faster than 1/s
#             #while time.time() - st.session_state.start_time < (int(oldtime) + 1):
#                 #time.sleep(0.001)

#         elif not st.session_state.running and not st.session_state.end_workout:
#             # Start the background task if not already running
#             st.session_state.running = True
#             # Start the workout loop in the background
#             asyncio.run(run_workout_loop(conn))

#         # Save data and end workout
#         if st.session_state.end_workout:
#             avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#             tottime = time.time() - st.session_state.start_time
#             totalreps = st.session_state.total_reps
#             conn.close()

#             st.session_state.WO_list.append(
#                 datastore(tottime, avgHR, totalreps, st.session_state.workout)
#             )
#             # Reset values so next workout starts fresh
#             st.session_state.heart_rate_trend = []
#             st.session_state.end_workout = False
#             st.session_state.workout = "None"
#             st.session_state.running = False  # Stop the workout

#             # Switch to page with workout summaries
#             st.switch_page("pages/history.py")

# async def run_workout_loop(conn):
#     """Run the workout loop in the background."""
#     while not st.session_state.end_workout:
#         heart_rate, total_reps = await get_heart_rate_and_reps(st.session_state.client, conn)
#         if heart_rate is None or total_reps is None:
#             break  # Exit if there's an error
#         st.session_state.heart_rate_trend.append(heart_rate)
#         st.session_state.total_reps = total_reps
#         await asyncio.sleep(1)  # Sleep to avoid blocking other tasks

# if __name__ == "__main__":
#     main()


# import streamlit as st
# import time
# import asyncio
# from HRfunc import get_heart_rate
# from data import datastore
# from datatransferpc import receive_data_from_pi
# import socket

# async def get_heart_rate_and_reps(client, conn):
#     """Retrieve heart rate and rep count data asynchronously."""
#     try:
#         heart_rate = await get_heart_rate(client)  # Get heart rate asynchronously
#         total_reps = await asyncio.to_thread(receive_reps_from_pi, conn)  # Blocking rep count retrieval
#     except Exception as e:
#         st.error(f"Error: {e}")
#         return None, None
#     return heart_rate, total_reps

# def receive_reps_from_pi(conn):
#     """Receive rep count from Raspberry Pi in a blocking manner."""
#     return conn.recv(1024).decode('utf-8')

# def main():
#     # Setup workout values
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "total_reps" not in st.session_state:
#         st.session_state.total_reps = 0
#     if "running" not in st.session_state:
#         st.session_state.running = False
#     if "graph_data" not in st.session_state:
#         st.session_state.graph_data = []

#     # Check for errors
#     if not st.session_state.connected:
#         st.error("No heart rate sensor connected.")
#         time.sleep(2)
#         st.switch_page("pages/home.py")
#     elif st.session_state.workout is None:
#         st.warning("No workout selected, redirecting...")
#         time.sleep(2)
#         st.switch_page("pages/workoutlist.py")
#     else:
#         # Layout containers
#         static_ui = st.container()
#         graph = st.empty()

#         # Start socket
#         pc_ip = "192.168.1.4"  # Replace with your PC's IP address
#         pc_port = 65432  # Replace with the port number you want to use
#         conn = receive_data_from_pi(pc_ip, pc_port)

#         # Static Part of website
#         with static_ui:
#             st.title("Heart Rate Monitor Dashboard")
#             st.write("Click the button below to end your workout.")
#             if st.button("End Workout", key="end_workout_button"):
#                 st.session_state.end_workout = True
#                 st.session_state.running = False  # Stop the background task

#         # Start the workout loop in the background if not running
#         if st.session_state.running and not st.session_state.end_workout:
#             heart_rate, total_reps = asyncio.run(get_heart_rate_and_reps(st.session_state.client, conn))

#             if heart_rate is None or total_reps is None:
#                 st.session_state.running = False  # Stop if there's an error
#                 return  # Exit if an error occurs

#             # Update the heart rate trend and rep count
#             st.session_state.heart_rate_trend.append(heart_rate)
#             st.session_state.total_reps = total_reps
#             st.session_state.graph_data.append((time.time(), heart_rate, total_reps))  # Save both HR and reps

#             # Update only the graph area
#             with graph.container():
#                 st.write(f"Your current heart rate: {int(heart_rate)} bpm")
#                 st.write(f"Total Reps: {total_reps}")  # Display the current rep count
#                 st.line_chart(st.session_state.heart_rate_trend)  # Display heart rate graph
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")

#             # Delay to avoid over-updating
#             while time.time() - st.session_state.start_time < (int(time.time()) + 1):
#                 time.sleep(0.001)

#         # Start workout loop if not running
#         if not st.session_state.running and not st.session_state.end_workout:
#             st.session_state.running = True
#             # Start the workout loop in the background
#             asyncio.run(run_workout_loop(conn))

#         # Save data and end workout
#         if st.session_state.end_workout:
#             avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#             tottime = time.time() - st.session_state.start_time
#             totalreps = st.session_state.total_reps
#             conn.close()

#             st.session_state.WO_list.append(
#                 datastore(tottime, avgHR, totalreps, st.session_state.workout)
#             )
#             # Reset values so next workout starts fresh
#             st.session_state.heart_rate_trend = []
#             st.session_state.end_workout = False
#             st.session_state.workout = "None"
#             st.session_state.running = False  # Stop the workout

#             # Switch to page with workout summaries
#             st.switch_page("pages/history.py")

# async def run_workout_loop(conn):
#     """Run the workout loop in the background."""
#     while not st.session_state.end_workout:
#         heart_rate, total_reps = await get_heart_rate_and_reps(st.session_state.client, conn)
#         if heart_rate is None or total_reps is None:
#             break  # Exit if there's an error
#         st.session_state.heart_rate_trend.append(heart_rate)
#         st.session_state.total_reps = total_reps
#         await asyncio.sleep(1)  # Sleep to avoid blocking other tasks

# if __name__ == "__main__":
#     main()


# ## needs conn to be defined
# import streamlit as st
# import time
# import asyncio
# from HRfunc import get_heart_rate
# from data import datastore
# from datatransferpc import receive_data_from_pi
# import socket

# def start_workout_loop():
#     """ Start the workout loop for heart rate and rep count updates """
#     st.session_state.running = True
#     st.session_state.end_workout = False

#     # Start socket for communication with Raspberry Pi
#     pc_ip = "192.168.1.4"  # Replace with your PC's IP address
#     pc_port = 65432  # Replace with the port number you want to use
#     conn = receive_data_from_pi(pc_ip, pc_port)

#     # Run workout in background
#     while not st.session_state.end_workout:
#         heart_rate, total_reps = asyncio.run(get_heart_rate_and_reps(st.session_state.client, conn))
        
#         if heart_rate is None or total_reps is None:
#             st.error("Error retrieving heart rate or rep count.")
#             break

#         # Update heart rate trend and rep count
#         st.session_state.heart_rate_trend.append(heart_rate)
#         st.session_state.total_reps = total_reps

#         # Update UI elements
#         st.session_state.graph_data.append((time.time(), heart_rate, total_reps))

#         # Update the graph
#         st.session_state.graph_data = st.session_state.graph_data[-100:]  # Keep the last 100 data points for smooth graph updates
#         with st.empty():
#             st.write(f"Your current heart rate: {int(heart_rate)} bpm")
#             st.write(f"Total Reps: {total_reps}")
#             st.line_chart([entry[1] for entry in st.session_state.graph_data])  # Only plot heart rate (index 1)

#         time.sleep(1)

#     # Closing connection once workout ends
#     conn.close()

# async def get_heart_rate_and_reps(client, conn):
#     """ Retrieve heart rate and rep count asynchronously """
#     try:
#         heart_rate = await get_heart_rate(client)  # Get heart rate asynchronously
#         total_reps = await asyncio.to_thread(receive_reps_from_pi, conn)  # Blocking rep count retrieval
#     except Exception as e:
#         st.error(f"Error: {e}")
#         return None, None
#     return heart_rate, total_reps

# def receive_reps_from_pi(conn):
#     """ Receive rep count from Raspberry Pi in a blocking manner """
#     return conn.recv(1024).decode('utf-8')

# def main():
#     # Setup workout values
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "total_reps" not in st.session_state:
#         st.session_state.total_reps = 0
#     if "running" not in st.session_state:
#         st.session_state.running = False
#     if "graph_data" not in st.session_state:
#         st.session_state.graph_data = []

#     # Check for errors
#     if not st.session_state.connected:
#         st.error("No heart rate sensor connected.")
#         time.sleep(2)
#         st.switch_page("pages/home.py")
#     elif st.session_state.workout is None:
#         st.warning("No workout selected, redirecting...")
#         time.sleep(2)
#         st.switch_page("pages/workoutlist.py")
#     else:
#         # Layout containers
#         static_ui = st.container()
#         graph = st.empty()

#         # Static Part of website
#         with static_ui:
#             st.title("Heart Rate Monitor Dashboard")
#             st.write("Click the button below to end your workout.")
#             if st.button("End Workout", key="end_workout_button"):
#                 st.session_state.end_workout = True
#                 st.session_state.running = False  # Stop the background task
#                 st.session_state.graph_data.clear()  # Clear the graph data

#         # Start the workout loop in the background if not running
#         if st.session_state.running and not st.session_state.end_workout:
#             heart_rate, total_reps = asyncio.run(get_heart_rate_and_reps(st.session_state.client, conn))

#             if heart_rate is None or total_reps is None:
#                 st.session_state.running = False  # Stop if there's an error
#                 return  # Exit if an error occurs

#             # Update the heart rate trend and rep count
#             st.session_state.heart_rate_trend.append(heart_rate)
#             st.session_state.total_reps = total_reps

#             # Update only the graph area
#             with graph.container():
#                 st.write(f"Your current heart rate: {int(heart_rate)} bpm")
#                 st.write(f"Total Reps: {total_reps}")  # Display the current rep count
#                 st.line_chart(st.session_state.heart_rate_trend)  # Display heart rate graph
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")

#             # Delay to avoid over-updating
#             while time.time() - st.session_state.start_time < (int(time.time()) + 1):
#                 time.sleep(0.001)

#         # Start workout loop if not running
#         if not st.session_state.running and not st.session_state.end_workout:
#             st.session_state.running = True
#             # Start the workout loop in the background
#             start_workout_loop()

#         # Save data and end workout
#         if st.session_state.end_workout:
#             avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#             tottime = time.time() - st.session_state.start_time
#             totalreps = st.session_state.total_reps

#             st.session_state.WO_list.append(
#                 datastore(tottime, avgHR, totalreps, st.session_state.workout)
#             )
#             # Reset values so next workout starts fresh
#             st.session_state.heart_rate_trend = []
#             st.session_state.end_workout = False
#             st.session_state.workout = "None"
#             st.session_state.running = False  # Stop the workout

#             # Switch to page with workout summaries
#             st.switch_page("pages/history.py")

# if __name__ == "__main__":
#     main()
