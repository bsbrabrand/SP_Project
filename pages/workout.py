# import streamlit as st
# import time
# import asyncio
# from HRfunc import get_heart_rate
# from data import datastore
# from picamera2 import Picamera2
# import cv2
# import mediapipe as mp
# import numpy as np

# def initialize_camera():
#     """Initialize the camera and handle errors gracefully."""
#     try:
#         picam2 = Picamera2()
#         picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
#         picam2.start()
#         return picam2
#     except RuntimeError as e:
#         st.error(f"Failed to initialize camera: {e}")
#         return None


# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)

#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)

#     if angle > 180.0:
#         angle = 360 - angle

#     return angle

# def main():
#     # Setup workout values
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "counter" not in st.session_state:
#         st.session_state.counter = 0

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
#         mp_drawing = mp.solutions.drawing_utils
#         mp_pose = mp.solutions.pose

#         pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


#         #Initialize camera once
#         if "picam2" not in st.session_state:
#             st.session_state.picam2 = initialize_camera()

#         # Exit if camera is not initialized properly
#         if not st.session_state.picam2:
#             st.stop()  # Stop execution if the camera failed to initialize

#         picam2 = st.session_state.picam2
#         stage = None

#         # Layout containers
#         static_ui = st.container()
#         graph = st.empty()

#         # Static Part of website
#         with static_ui:
#             st.title("Heart Rate Monitor Dashboard")
#             st.write("Click the button below to end your workout.")
#             if st.button("End Workout", key="end_workout_button"):
#                 st.session_state.end_workout = True

#         st.write("test cam next")
#         # Dynamic Part of Website
#         while not st.session_state.end_workout:
#             #record current time
#             oldtime = time.time()-st.session_state.start_time

#             #cam
#             frame = picam2.capture_array()

#             # Convert to RGB for MediaPipe
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False
#             results = pose.process(image)
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             # Draw pose landmarks
#             if results.pose_landmarks:
#                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#                 # Extract landmarks for left arm
#                 landmarks = results.pose_landmarks.landmark
#                 left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
#                 left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
#                 left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

#                 # Get coordinates and calculate angle
#                 shoulder_coords = [left_shoulder.x, left_shoulder.y]
#                 elbow_coords = [left_elbow.x, left_elbow.y]
#                 wrist_coords = [left_wrist.x, left_wrist.y]
#                 angle = calculate_angle(shoulder_coords, elbow_coords, wrist_coords)

#                 # Bicep curl counter logic
#                 if angle > 160:
#                     stage = "Down"
#                 if angle < 30 and stage == "Down":
#                     stage = "Up"
#                     st.session_state.counter += 1

#             st.write("camera done")
#             time.sleep(5)        
#             # Get new heart rate reading
#             try:
#                 hr = asyncio.run(get_heart_rate(st.session_state.client))
#                 st.session_state.heart_rate_trend.append(hr)
#             except Exception as e:
#                 st.error(f"Error reading heart rate: {e}")
#                 time.sleep(2)
#                 st.switch_page("home.py")

#             # Update only the graph area
#             with graph.container():
#                 st.write(f"Your current heart rate: {int(hr)} bpm")
#                 st.line_chart(st.session_state.heart_rate_trend)
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")
#                 st.write(f"{st.session_state.counter} reps")

#             #delay if needed so it doesn't update faster than 1/s
#             while time.time()-st.session_state.start_time < (int(oldtime)+1):
#                 time.sleep(0.001)

#         # Save data and end workout
#         avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#         tottime = time.time() - st.session_state.start_time
#         totalreps = 0  # Placeholder

#         st.session_state.WO_list.append(
#             datastore(tottime, avgHR, totalreps, st.session_state.workout)
#         )
#         #reset values so next workout starts fresh
#         st.session_state.heart_rate_trend = []
#         st.session_state.end_workout = False
#         st.session_state.workout = "None"
#         st.session_state.counter = 0

#         #switch to page with workout summaries
#         st.switch_page("pages/history.py")

# if __name__ == "__main__":
#     main()


# import streamlit as st
# import time
# import asyncio
# from HRfunc import get_heart_rate
# from data import datastore

# def main():
#     # Setup workout values
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False

#     #Check for errors
#     if not st.session_state.connected:
#         st.error("No heart rate sensor connected.")
#         time.sleep(10)
#         st.switch_page("home.py")
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

#         # Dynamic Part of Website
#         while not st.session_state.end_workout:
#             #record current time
#             oldtime = time.time()-st.session_state.start_time
#             # Get new heart rate reading
#             try:
#                 hr = get_heart_rate()#st.session_state.client)
#                 st.session_state.heart_rate_trend.append(hr)
#             except Exception as e:
#                 st.error(f"Error reading heart rate: {e}")
#                 time.sleep(10)
#                 st.switch_page("home.py")

#             # Update only the graph area
#             with graph.container():
#                 st.write(f"Your current heart rate: {int(hr)} bpm")
#                 st.line_chart(st.session_state.heart_rate_trend)
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")

#             #delay if needed so it doesn't update faster than 1/s
#             while time.time()-st.session_state.start_time < (int(oldtime)+1):
#                 time.sleep(0.001)

#         # Save data and end workout
#         avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#         tottime = time.time() - st.session_state.start_time
#         totalreps = 0  # Placeholder

#         st.session_state.WO_list.append(
#             datastore(tottime, avgHR, totalreps, st.session_state.workout)
#         )
#         #reset values so next workout starts fresh
#         st.session_state.heart_rate_trend = []
#         st.session_state.end_workout = False
#         st.session_state.workout = "None"

#         #switch to page with workout summaries
#         st.switch_page("pages/history.py")

# if __name__ == "__main__":
#     main()

# streamlit_app.py
# import streamlit as st
# import time
# import threading
# from HRfunc import connect_ble_client, start_heart_rate_notifications, stop_ble_client, parse_hr_data
# from data import datastore

# # Global thread-safe store
# latest_hr_lock = threading.Lock()
# latest_hr_value = {"value": None}

# def handle_hr(sender, data):
#     hr = parse_hr_data(sender, data)
#     print(f"🔄 handle_hr() called: sender={sender}, raw={list(data)}, parsed={hr}")
#     with latest_hr_lock:
#         latest_hr_value["value"] = hr

# def main():
#     # Setup session state
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "start_time" not in st.session_state:
#         st.session_state.start_time = time.time()

#     # BLE Setup
#     if not st.session_state.get("ble_client"):
#         try:
#             st.session_state.ble_client = connect_ble_client()
#         except Exception as e:
#             st.error(f"Connection failed: {e}")
#             time.sleep(2)
#             st.switch_page("home.py")

#     try:
#         start_heart_rate_notifications(st.session_state.ble_client, handle_hr)
#     except Exception as e:
#         st.error(f"Notification setup failed: {e}")
#         time.sleep(2)
#         st.switch_page("home.py")

#     # Layout
#     static_ui = st.container()
#     graph = st.empty()

#     with static_ui:
#         st.title("Heart Rate Monitor Dashboard")
#         st.write("Click the button below to end your workout.")
#         if st.button("End Workout", key="end_workout_button"):
#             st.session_state.end_workout = True

#     # Workout loop
#     while not st.session_state.end_workout:
#         oldtime = time.time() - st.session_state.start_time

#         # Safely get heart rate
#         with latest_hr_lock:
#             hr = latest_hr_value["value"]

#         if hr:
#             st.session_state.heart_rate_trend.append(hr)

#         with graph.container():
#             st.write(f"Your current heart rate: {hr if hr else 'Waiting...'} bpm")
#             if st.session_state.heart_rate_trend:
#                 st.line_chart(st.session_state.heart_rate_trend)
#             elapsed = int(time.time() - st.session_state.start_time)
#             st.write(f"Timer: {elapsed} seconds")

#         # Wait ~1s before next reading
#         while time.time() - st.session_state.start_time < int(oldtime) + 1:
#             time.sleep(0.01)

#     # Cleanup
#     try:
#         stop_ble_client(st.session_state.ble_client)
#     except:
#         pass

#     avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#     tottime = time.time() - st.session_state.start_time
#     totalreps = 0  # You can adjust this as needed

#     st.session_state.WO_list.append(
#         datastore(tottime, avgHR, totalreps, st.session_state.workout)
#     )

#     # Reset session for next workout
#     for key in ["heart_rate_trend", "ble_client", "end_workout", "workout", "start_time"]:
#         if key in st.session_state:
#             del st.session_state[key]

#     st.switch_page("pages/history.py")

# if __name__ == "__main__":
#     main()

# import streamlit as st
# import time
# import threading
# from HRfunc import connect_ble_client, start_heart_rate_notifications, stop_ble_client
# from data import datastore

# # Shared, thread-safe HR store
# latest_hr_lock = threading.Lock()
# latest_hr_value = {"value": None}

# def thread_safe_callback(hr):
#     with latest_hr_lock:
#         latest_hr_value["value"] = hr

# def main():
#     # Session state setup
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "start_time" not in st.session_state:
#         st.session_state.start_time = time.time()

#     # Connect BLE device
#     if not st.session_state.get("ble_client"):
#         try:
#             st.session_state.ble_client = connect_ble_client()
#         except Exception as e:
#             st.error(f"Connection failed: {e}")
#             time.sleep(2)
#             st.switch_page("home.py")

#     try:
#         start_heart_rate_notifications(st.session_state.ble_client, thread_safe_callback)
#     except Exception as e:
#         st.error(f"Notification setup failed: {e}")
#         time.sleep(2)
#         st.switch_page("home.py")

#     # UI setup
#     static_ui = st.container()
#     graph = st.empty()

#     with static_ui:
#         st.title("Heart Rate Monitor Dashboard")
#         st.write("Click the button below to end your workout.")
#         if st.button("End Workout", key="end_workout_button"):
#             st.session_state.end_workout = True

#     # Main loop
#     while not st.session_state.end_workout:
#         oldtime = time.time() - st.session_state.start_time

#         with latest_hr_lock:
#             hr = latest_hr_value["value"]

#         if hr:
#             st.session_state.latest_hr = hr
#             st.session_state.heart_rate_trend.append(hr)

#         with graph.container():
#             st.write(f"Your current heart rate: {hr if hr else 'Waiting...'} bpm")
#             if st.session_state.heart_rate_trend:
#                 st.line_chart(st.session_state.heart_rate_trend)
#             elapsed = int(time.time() - st.session_state.start_time)
#             st.write(f"Timer: {elapsed} seconds")

#         while time.time() - st.session_state.start_time < int(oldtime) + 1:
#             time.sleep(0.01)

#     # Cleanup
#     try:
#         stop_ble_client(st.session_state.ble_client)
#     except:
#         pass

#     avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#     tottime = time.time() - st.session_state.start_time
#     totalreps = 0  # Customize as needed

#     st.session_state.WO_list.append(
#         datastore(tottime, avgHR, totalreps, st.session_state.workout)
#     )

#     # Reset state
#     for key in ["heart_rate_trend", "latest_hr", "ble_client", "end_workout", "workout", "start_time"]:
#         if key in st.session_state:
#             del st.session_state[key]

#     st.switch_page("pages/history.py")

# if __name__ == "__main__":
#     main()

# import streamlit as st
# import time
# from HRfunc import connect_ble_client, start_heart_rate_notifications, stop_ble_client, parse_hr_data
# from data import datastore

# def main():
#     # Setup session state
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "start_time" not in st.session_state:
#         st.session_state.start_time = time.time()

#     # BLE Setup
#     if not st.session_state.get("ble_client"):
#         try:
#             st.session_state.ble_client = connect_ble_client()
#         except Exception as e:
#             st.error(f"Connection failed: {e}")
#             time.sleep(2)
#             st.switch_page("home.py")

#     if "latest_hr" not in st.session_state:
#         st.session_state.latest_hr = None
#         def handle_hr(sender, data):
#             st.session_state.latest_hr = parse_hr_data(sender, data)

#         try:
#             start_heart_rate_notifications(st.session_state.ble_client, handle_hr)
#         except Exception as e:
#             st.error(f"Notification setup failed: {e}")
#             time.sleep(2)
#             st.switch_page("home.py")

#     # Layout
#     static_ui = st.container()
#     graph = st.empty()

#     with static_ui:
#         st.title("Heart Rate Monitor Dashboard")
#         st.write("Click the button below to end your workout.")
#         if st.button("End Workout", key="end_workout_button"):
#             st.session_state.end_workout = True

#     # Workout loop
#     while not st.session_state.end_workout:
#         oldtime = time.time() - st.session_state.start_time

#         hr = st.session_state.latest_hr
#         if hr:
#             st.session_state.heart_rate_trend.append(hr)

#         with graph.container():
#             st.write(f"Your current heart rate: {hr if hr else 'Waiting...'} bpm")
#             if st.session_state.heart_rate_trend:
#                 st.line_chart(st.session_state.heart_rate_trend)
#             elapsed = int(time.time() - st.session_state.start_time)
#             st.write(f"Timer: {elapsed} seconds")

#         while time.time() - st.session_state.start_time < int(oldtime) + 1:
#             time.sleep(0.01)

#     # Cleanup
#     try:
#         stop_ble_client(st.session_state.ble_client)
#     except:
#         pass

#     avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#     tottime = time.time() - st.session_state.start_time
#     totalreps = 0  # You can adjust this as needed

#     st.session_state.WO_list.append(
#         datastore(tottime, avgHR, totalreps, st.session_state.workout)
#     )

#     # Reset session for next workout
#     for key in ["heart_rate_trend", "latest_hr", "ble_client", "end_workout", "workout", "start_time"]:
#         if key in st.session_state:
#             del st.session_state[key]

#     st.switch_page("pages/history.py")

# if __name__ == "__main__":
#     main()

# import streamlit as st
# import time
# from HRfunc import connect_ble_client, start_heart_rate_notifications, stop_ble_client, parse_hr_data
# from data import datastore

# def main():
#     # Setup session state
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "start_time" not in st.session_state:
#         st.session_state.start_time = time.time()

#     # BLE Setup
#     if not st.session_state.get("ble_client"):
#         try:
#             st.session_state.ble_client = connect_ble_client()
#         except Exception as e:
#             st.error(f"Connection failed: {e}")
#             time.sleep(2)
#             st.switch_page("home.py")

#     if "latest_hr" not in st.session_state:
#         st.session_state.latest_hr = None
#         def handle_hr(sender, data):
#             st.session_state.latest_hr = parse_hr_data(sender, data)

#         try:
#             start_heart_rate_notifications(st.session_state.ble_client, handle_hr)
#         except Exception as e:
#             st.error(f"Notification setup failed: {e}")
#             time.sleep(2)
#             st.switch_page("home.py")

#     # Layout
#     static_ui = st.container()
#     graph = st.empty()

#     with static_ui:
#         st.title("Heart Rate Monitor Dashboard")
#         st.write("Click the button below to end your workout.")
#         if st.button("End Workout", key="end_workout_button"):
#             st.session_state.end_workout = True

#     # Workout loop
#     while not st.session_state.end_workout:
#         oldtime = time.time() - st.session_state.start_time

#         hr = st.session_state.latest_hr
#         if hr:
#             st.session_state.heart_rate_trend.append(hr)

#         with graph.container():
#             st.write(f"Your current heart rate: {hr if hr else 'Waiting...'} bpm")
#             if st.session_state.heart_rate_trend:
#                 st.line_chart(st.session_state.heart_rate_trend)
#             elapsed = int(time.time() - st.session_state.start_time)
#             st.write(f"Timer: {elapsed} seconds")

#         while time.time() - st.session_state.start_time < int(oldtime) + 1:
#             time.sleep(0.01)

#     # Cleanup
#     try:
#         stop_ble_client(st.session_state.ble_client)
#     except:
#         pass

#     avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#     tottime = time.time() - st.session_state.start_time
#     totalreps = 0  # You can adjust this as needed

#     st.session_state.WO_list.append(
#         datastore(tottime, avgHR, totalreps, st.session_state.workout)
#     )

#     # Reset session for next workout
#     for key in ["heart_rate_trend", "latest_hr", "ble_client", "end_workout", "workout", "start_time"]:
#         if key in st.session_state:
#             del st.session_state[key]

#     st.switch_page("pages/history.py")

# if __name__ == "__main__":
#     main()

# import time
# import streamlit as st
# from HRfunc import connect_ble_client, start_heart_rate_notifications, stop_ble_client, parse_hr_data
# from data import datastore
# import asyncio

# def main():
#     # Setup session state
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "start_time" not in st.session_state:
#         st.session_state.start_time = time.time()

#     # BLE Setup
#     if not st.session_state.get("ble_client"):
#         try:
#             st.session_state.ble_client = asyncio.run(connect_ble_client())  # Use asyncio.run() to run async function
#             print(st.session_state.ble_client)
#             print("test\n")
#         except Exception as e:
#             st.error(f"Connection failed: {e}")
#             time.sleep(2)
#             st.switch_page("home.py")

#     if "latest_hr" not in st.session_state:
#         st.session_state.latest_hr = None

#         def handle_hr(sender, data):
#             st.session_state.latest_hr = parse_hr_data(sender, data)

#         try:
#             asyncio.run(start_heart_rate_notifications(st.session_state.ble_client, handle_hr))  # Run notification handler on main loop
#         except Exception as e:
#             st.error(f"Notification setup failed: {e}")
#             time.sleep(2)
#             st.switch_page("home.py")

#     # Layout
#     static_ui = st.container()
#     graph = st.empty()

#     with static_ui:
#         st.title("Heart Rate Monitor Dashboard")
#         st.write("Click the button below to end your workout.")
#         if st.button("End Workout", key="end_workout_button"):
#             st.session_state.end_workout = True

#     # Workout loop
#     while not st.session_state.end_workout:
#         oldtime = time.time() - st.session_state.start_time

#         hr = st.session_state.latest_hr
#         if hr:
#             st.session_state.heart_rate_trend.append(hr)

#         with graph.container():
#             st.write(f"Your current heart rate: {hr if hr else 'Waiting...'} bpm")
#             if st.session_state.heart_rate_trend:
#                 st.line_chart(st.session_state.heart_rate_trend)
#             elapsed = int(time.time() - st.session_state.start_time)
#             st.write(f"Timer: {elapsed} seconds")

#         while time.time() - st.session_state.start_time < int(oldtime) + 1:
#             time.sleep(0.01)

#     # Cleanup
#     try:
#         asyncio.run(stop_ble_client(st.session_state.ble_client))  # Ensure stop notification is called in main loop
#     except:
#         pass

#     avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#     tottime = time.time() - st.session_state.start_time
#     totalreps = 0  # Adjust based on your rep counting logic

#     st.session_state.WO_list.append(
#         datastore(tottime, avgHR, totalreps, st.session_state.workout)
#     )

#     # Reset session for next workout
#     for key in ["heart_rate_trend", "latest_hr", "ble_client", "end_workout", "workout", "start_time"]:
#         if key in st.session_state:
#             del st.session_state[key]

#     st.switch_page("pages/history.py")

# if __name__ == "__main__":
#     main()

import time
import asyncio
import streamlit as st
from HRfunc import connect_ble_client, start_heart_rate_notifications, stop_ble_client, parse_hr_data
from data import datastore

async def main():
    # Setup session state
    if "heart_rate_trend" not in st.session_state:
        st.session_state.heart_rate_trend = []
    if "end_workout" not in st.session_state:
        st.session_state.end_workout = False
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    # BLE Setup
    if "ble_client" not in st.session_state:
        try:
            st.session_state.ble_client = await connect_ble_client()  # Use await to get the client
        except Exception as e:
            st.error(f"Connection failed: {e}")
            time.sleep(2)
            st.switch_page("home.py")

    if "latest_hr" not in st.session_state:
        st.session_state.latest_hr = None

        # Define HR update callback
        def handle_hr(sender, data):
            st.session_state.latest_hr = parse_hr_data(sender, data)

        try:
            await start_heart_rate_notifications(st.session_state.ble_client, handle_hr)  # Run notification setup here
        except Exception as e:
            st.error(f"Notification setup failed: {e}")
            time.sleep(2)
            st.switch_page("home.py")

    # Layout
    static_ui = st.container()
    graph = st.empty()

    with static_ui:
        st.title("Heart Rate Monitor Dashboard")
        st.write("Click the button below to end your workout.")
        if st.button("End Workout", key="end_workout_button"):
            st.session_state.end_workout = True

    # Workout loop
    while not st.session_state.end_workout:
        oldtime = time.time() - st.session_state.start_time

        hr = st.session_state.latest_hr
        if hr:
            st.session_state.heart_rate_trend.append(hr)

        with graph.container():
            st.write(f"Your current heart rate: {hr if hr else 'Waiting...'} bpm")
            if st.session_state.heart_rate_trend:
                st.line_chart(st.session_state.heart_rate_trend)
            elapsed = int(time.time() - st.session_state.start_time)
            st.write(f"Timer: {elapsed} seconds")

        while time.time() - st.session_state.start_time < int(oldtime) + 1:
            time.sleep(0.01)

    # Cleanup
    try:
        await stop_ble_client(st.session_state.ble_client)  # Stop notification properly
    except:
        pass

    avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
    tottime = time.time() - st.session_state.start_time
    totalreps = 0  # Adjust based on your rep counting logic

    st.session_state.WO_list.append(
        datastore(tottime, avgHR, totalreps, st.session_state.workout)
    )

    # Reset session for next workout
    for key in ["heart_rate_trend", "latest_hr", "ble_client", "end_workout", "workout", "start_time"]:
        if key in st.session_state:
            del st.session_state[key]

    st.switch_page("pages/history.py")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())


# import streamlit as st
# import time
# from HRfunc import connect_ble_client, start_heart_rate_notifications, stop_ble_client, parse_hr_data
# from data import datastore

# def main():
#     # Setup session state
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "start_time" not in st.session_state:
#         st.session_state.start_time = time.time()

#     # BLE Setup
#     if not st.session_state.get("ble_client"):
#         try:
#             st.session_state.ble_client = connect_ble_client()
#         except Exception as e:
#             st.error(f"Connection failed: {e}")
#             time.sleep(2)
#             st.switch_page("home.py")

#     if "latest_hr" not in st.session_state:
#         st.session_state.latest_hr = None
#         def handle_hr(sender, data):
#             st.session_state.latest_hr = parse_hr_data(sender, data)

#         try:
#             start_heart_rate_notifications(st.session_state.ble_client, handle_hr)
#         except Exception as e:
#             st.error(f"Notification setup failed: {e}")
#             time.sleep(2)
#             st.switch_page("home.py")

#     # Layout
#     static_ui = st.container()
#     graph = st.empty()

#     with static_ui:
#         st.title("Heart Rate Monitor Dashboard")
#         st.write("Click the button below to end your workout.")
#         if st.button("End Workout", key="end_workout_button"):
#             st.session_state.end_workout = True

#     # Workout loop
#     while not st.session_state.end_workout:
#         oldtime = time.time() - st.session_state.start_time

#         hr = st.session_state.latest_hr
#         if hr:
#             st.session_state.heart_rate_trend.append(hr)

#         with graph.container():
#             st.write(f"Your current heart rate: {hr if hr else 'Waiting...'} bpm")
#             if st.session_state.heart_rate_trend:
#                 st.line_chart(st.session_state.heart_rate_trend)
#             elapsed = int(time.time() - st.session_state.start_time)
#             st.write(f"Timer: {elapsed} seconds")

#         while time.time() - st.session_state.start_time < int(oldtime) + 1:
#             time.sleep(0.01)

#     # Cleanup
#     try:
#         stop_ble_client(st.session_state.ble_client)
#     except:
#         pass

#     avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#     tottime = time.time() - st.session_state.start_time
#     totalreps = 0  # You can adjust this as needed

#     st.session_state.WO_list.append(
#         datastore(tottime, avgHR, totalreps, st.session_state.workout)
#     )

#     # Reset session for next workout
#     for key in ["heart_rate_trend", "latest_hr", "ble_client", "end_workout", "workout", "start_time"]:
#         if key in st.session_state:
#             del st.session_state[key]

#     st.switch_page("pages/history.py")

# if __name__ == "__main__":
#     main()


# import streamlit as st
# import time
# import asyncio
# from HRfunc import get_heart_rate
# from data import datastore
# from picamera2 import Picamera2
# import cv2
# import mediapipe as mp
# import numpy as np


# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)

#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)

#     if angle > 180.0:
#         angle = 360 - angle

#     return angle


# def initialize_camera():
#     """Initialize the camera and handle errors gracefully."""
#     try:
#         picam2 = Picamera2()
#         picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
#         picam2.start()
#         return picam2
#     except RuntimeError as e:
#         st.error(f"Failed to initialize camera: {e}")
#         return None


# async def fetch_heart_rate():
#     """Fetch the heart rate asynchronously."""
#     try:
#         hr = await get_heart_rate(st.session_state.client)  # Assuming get_heart_rate is an async function
#         return hr
#     except Exception as e:
#         st.error(f"Error reading heart rate: {e}")
#         return None


# def main():
#     # Setup workout values
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "counter" not in st.session_state:
#         st.session_state.counter = 0

#     # Check for errors
#     if not st.session_state.connected:
#         st.error("No heart rate sensor connected.")
#         time.sleep(10)
#         st.switch_page("pages/home.py")
#     elif st.session_state.workout is None:
#         st.warning("No workout selected, redirecting...")
#         time.sleep(10)
#         st.switch_page("pages/workoutlist.py")
#     else:
#         mp_drawing = mp.solutions.drawing_utils
#         mp_pose = mp.solutions.pose

#         pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

#         # Initialize camera once
#         if "picam2" not in st.session_state:
#             st.session_state.picam2 = initialize_camera()

#         # Exit if camera is not initialized properly
#         if not st.session_state.picam2:
#             st.stop()  # Stop execution if the camera failed to initialize

#         picam2 = st.session_state.picam2
#         stage = None

#         # Layout containers
#         static_ui = st.container()
#         graph = st.empty()

#         # Static Part of website
#         with static_ui:
#             st.title("Heart Rate Monitor Dashboard")
#             st.write("Click the button below to end your workout.")
#             if st.button("End Workout", key="end_workout_button"):
#                 st.session_state.end_workout = True

#         # Dynamic Part of Website
#         while not st.session_state.end_workout:
#             # Record current time
#             oldtime = time.time() - st.session_state.start_time

#             # Capture frame from camera
#             frame = picam2.capture_array()

#             # Convert to RGB for MediaPipe
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False
#             results = pose.process(image)
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             # Draw pose landmarks
#             if results.pose_landmarks:
#                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#                 # Extract landmarks for left arm
#                 landmarks = results.pose_landmarks.landmark
#                 left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
#                 left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
#                 left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

#                 # Get coordinates and calculate angle
#                 shoulder_coords = [left_shoulder.x, left_shoulder.y]
#                 elbow_coords = [left_elbow.x, left_elbow.y]
#                 wrist_coords = [left_wrist.x, left_wrist.y]
#                 angle = calculate_angle(shoulder_coords, elbow_coords, wrist_coords)

#                 # Bicep curl counter logic
#                 if angle > 160:
#                     stage = "Down"
#                 if angle < 30 and stage == "Down":
#                     stage = "Up"
#                     st.session_state.counter += 1

#             # Get new heart rate reading asynchronously
#             hr = None
#             task = asyncio.create_task(fetch_heart_rate())  # Create the async task
#             hr = asyncio.run(task)  # Run the task and wait for the result

#             if hr is not None:
#                 st.session_state.heart_rate_trend.append(hr)

#             # Update only the graph area
#             with graph.container():
#                 st.write(f"Your current heart rate: {int(hr)} bpm" if hr else "Unable to fetch heart rate")
#                 st.line_chart(st.session_state.heart_rate_trend)
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")
#                 st.write(f"{st.session_state.counter} reps")

#             # Delay to update every 1 second
#             while time.time() - st.session_state.start_time < (int(oldtime) + 1):
#                 time.sleep(0.001)

#         # Save data and end workout
#         avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#         tottime = time.time() - st.session_state.start_time
#         totalreps = 0  # Placeholder

#         st.session_state.WO_list.append(
#             datastore(tottime, avgHR, totalreps, st.session_state.workout)
#         )

#         # Reset values so next workout starts fresh
#         st.session_state.heart_rate_trend = []
#         st.session_state.end_workout = False
#         st.session_state.workout = "None"
#         st.session_state.counter = 0

#         # Switch to page with workout summaries
#         st.switch_page("pages/history.py")


# if __name__ == "__main__":
#     main()


# import streamlit as st
# import time
# import asyncio
# import threading
# from HRfunc import get_heart_rate
# from data import datastore
# from picamera2 import Picamera2
# import cv2
# import mediapipe as mp
# import numpy as np


# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)

#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)

#     if angle > 180.0:
#         angle = 360 - angle

#     return angle


# def initialize_camera():
#     """Initialize the camera and handle errors gracefully."""
#     try:
#         picam2 = Picamera2()
#         picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
#         picam2.start()
#         return picam2
#     except RuntimeError as e:
#         st.error(f"Failed to initialize camera: {e}")
#         return None


# def fetch_heart_rate_async():
#     """Fetch heart rate in a separate thread."""
#     async def fetch_heart_rate():
#         try:
#             hr = await get_heart_rate(st.session_state.client)
#             st.write(f"Heart rate fetched: {hr}")  # Debugging
#             return hr
#         except Exception as e:
#             st.error(f"Error reading heart rate: {e}")
#             return None

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(fetch_heart_rate())


# def main():
#     # Setup workout values
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "counter" not in st.session_state:
#         st.session_state.counter = 0

#     # Check for errors
#     if not st.session_state.connected:
#         st.error("No heart rate sensor connected.")
#         time.sleep(10)
#         st.switch_page("pages/home.py")
#     elif st.session_state.workout is None:
#         st.warning("No workout selected, redirecting...")
#         time.sleep(10)
#         st.switch_page("pages/workoutlist.py")
#     else:
#         mp_drawing = mp.solutions.drawing_utils
#         mp_pose = mp.solutions.pose

#         pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

#         # Initialize camera once
#         if "picam2" not in st.session_state:
#             st.session_state.picam2 = initialize_camera()

#         # Exit if camera is not initialized properly
#         if not st.session_state.picam2:
#             st.stop()  # Stop execution if the camera failed to initialize

#         picam2 = st.session_state.picam2
#         stage = None

#         # Layout containers
#         static_ui = st.container()
#         graph = st.empty()

#         # Static Part of website
#         with static_ui:
#             st.title("Heart Rate Monitor Dashboard")
#             st.write("Click the button below to end your workout.")
#             if st.button("End Workout", key="end_workout_button"):
#                 st.session_state.end_workout = True

#         # Start the asynchronous heart rate fetching in a new thread
#         heart_rate_thread = threading.Thread(target=fetch_heart_rate_async)
#         heart_rate_thread.daemon = True  # Daemon thread will close when the main thread ends
#         heart_rate_thread.start()

#         # Initialize hr to a default value to avoid referencing before assignment
#         hr = None

#         # Dynamic Part of Website
#         while not st.session_state.end_workout:
#             # Record current time
#             oldtime = time.time() - st.session_state.start_time

#             # Capture frame from camera
#             frame = picam2.capture_array()

#             # Convert to RGB for MediaPipe
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False
#             results = pose.process(image)
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             # Draw pose landmarks
#             if results.pose_landmarks:
#                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#                 # Extract landmarks for left arm
#                 landmarks = results.pose_landmarks.landmark
#                 left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
#                 left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
#                 left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

#                 # Get coordinates and calculate angle
#                 shoulder_coords = [left_shoulder.x, left_shoulder.y]
#                 elbow_coords = [left_elbow.x, left_elbow.y]
#                 wrist_coords = [left_wrist.x, left_wrist.y]
#                 angle = calculate_angle(shoulder_coords, elbow_coords, wrist_coords)

#                 # Bicep curl counter logic
#                 if angle > 160:
#                     stage = "Down"
#                 if angle < 30 and stage == "Down":
#                     stage = "Up"
#                     st.session_state.counter += 1

#             # Update heart rate graph periodically
#             if heart_rate_thread.is_alive():
#                 hr = fetch_heart_rate_async()  # Fetch heart rate synchronously within the main thread
#                 if hr is None:
#                     hr = "Unable to fetch heart rate"

#             # Debugging: log the heart rate fetched
#             st.write(f"Heart rate fetched: {hr}")

#             # Update only the graph area
#             with graph.container():
#                 st.write(f"Your current heart rate: {int(hr)} bpm" if isinstance(hr, int) else hr)
#                 st.line_chart(st.session_state.heart_rate_trend)
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")
#                 st.write(f"{st.session_state.counter} reps")

#             # Delay to update every 1 second
#             while time.time() - st.session_state.start_time < (int(oldtime) + 1):
#                 time.sleep(0.001)

#         # Save data and end workout
#         avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#         tottime = time.time() - st.session_state.start_time
#         totalreps = 0  # Placeholder

#         st.session_state.WO_list.append(
#             datastore(tottime, avgHR, totalreps, st.session_state.workout)
#         )

#         # Reset values so next workout starts fresh
#         st.session_state.heart_rate_trend = []
#         st.session_state.end_workout = False
#         st.session_state.workout = "None"
#         st.session_state.counter = 0

#         # Switch to page with workout summaries
#         st.switch_page("pages/history.py")


# if __name__ == "__main__":
#     main()


# import streamlit as st
# import time
# import asyncio
# from HRfunc import get_heart_rate
# from data import datastore
# from picamera2 import Picamera2
# import cv2
# import mediapipe as mp
# import numpy as np


# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)

#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)

#     if angle > 180.0:
#         angle = 360 - angle

#     return angle


# async def fetch_heart_rate():
#     try:
#         hr = await get_heart_rate(st.session_state.client)
#         return hr
#     except Exception as e:
#         st.error(f"Error reading heart rate: {e}")
#         return None


# def initialize_camera():
#     """Initialize the camera and handle errors gracefully."""
#     try:
#         picam2 = Picamera2()
#         picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
#         picam2.start()
#         return picam2
#     except RuntimeError as e:
#         st.error(f"Failed to initialize camera: {e}")
#         return None


# def main():
#     # Setup workout values
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "counter" not in st.session_state:
#         st.session_state.counter = 0

#     # Check for errors
#     if not st.session_state.connected:
#         st.error("No heart rate sensor connected.")
#         time.sleep(10)
#         st.switch_page("pages/home.py")
#     elif st.session_state.workout is None:
#         st.warning("No workout selected, redirecting...")
#         time.sleep(10)
#         st.switch_page("pages/workoutlist.py")
#     else:
#         mp_drawing = mp.solutions.drawing_utils
#         mp_pose = mp.solutions.pose

#         pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

#         # Initialize camera once
#         if "picam2" not in st.session_state:
#             st.session_state.picam2 = initialize_camera()

#         # Exit if camera is not initialized properly
#         if not st.session_state.picam2:
#             st.stop()  # Stop execution if the camera failed to initialize

#         picam2 = st.session_state.picam2
#         stage = None

#         # Layout containers
#         static_ui = st.container()
#         graph = st.empty()

#         # Static Part of website
#         with static_ui:
#             st.title("Heart Rate Monitor Dashboard")
#             st.write("Click the button below to end your workout.")
#             if st.button("End Workout", key="end_workout_button"):
#                 st.session_state.end_workout = True

#         # Fetch heart rate asynchronously
#         hr = None
#         if st.session_state.client:  # Check if client is initialized
#             hr = asyncio.run(fetch_heart_rate())  # Call async function to fetch heart rate
#             st.write(f"Heart rate fetched: {hr}" if hr else "Unable to fetch heart rate")

#         # Dynamic Part of Website
#         while not st.session_state.end_workout:
#             # Record current time
#             oldtime = time.time() - st.session_state.start_time

#             # Capture frame from camera
#             frame = picam2.capture_array()

#             # Convert to RGB for MediaPipe
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False
#             results = pose.process(image)
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             # Draw pose landmarks
#             if results.pose_landmarks:
#                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#                 # Extract landmarks for left arm
#                 landmarks = results.pose_landmarks.landmark
#                 left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
#                 left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
#                 left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

#                 # Get coordinates and calculate angle
#                 shoulder_coords = [left_shoulder.x, left_shoulder.y]
#                 elbow_coords = [left_elbow.x, left_elbow.y]
#                 wrist_coords = [left_wrist.x, left_wrist.y]
#                 angle = calculate_angle(shoulder_coords, elbow_coords, wrist_coords)

#                 # Bicep curl counter logic
#                 if angle > 160:
#                     stage = "Down"
#                 if angle < 30 and stage == "Down":
#                     stage = "Up"
#                     st.session_state.counter += 1

#             # Update heart rate graph periodically
#             if hr is None:
#                 hr = "Unable to fetch heart rate"
#             st.session_state.heart_rate_trend.append(hr)

#             # Update only the graph area
#             with graph.container():
#                 st.write(f"Your current heart rate: {int(hr)} bpm" if isinstance(hr, int) else hr)
#                 st.line_chart(st.session_state.heart_rate_trend)
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")
#                 st.write(f"{st.session_state.counter} reps")

#             # Delay to update every 1 second
#             while time.time() - st.session_state.start_time < (int(oldtime) + 1):
#                 time.sleep(0.001)

#         # Save data and end workout
#         avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#         tottime = time.time() - st.session_state.start_time
#         totalreps = 0  # Placeholder

#         st.session_state.WO_list.append(
#             datastore(tottime, avgHR, totalreps, st.session_state.workout)
#         )

#         # Reset values so next workout starts fresh
#         st.session_state.heart_rate_trend = []
#         st.session_state.end_workout = False
#         st.session_state.workout = "None"
#         st.session_state.counter = 0

#         # Switch to page with workout summaries
#         st.switch_page("pages/history.py")


# if __name__ == "__main__":
#     main()

# import streamlit as st
# import time
# import numpy as np
# import cv2
# import mediapipe as mp
# from picamera2 import Picamera2
# from HRfunc import get_heart_rate
# from data import datastore

# # Function to calculate angle
# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)
#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)
#     if angle > 180.0:
#         angle = 360 - angle
#     return angle

# # Camera initialization
# def initialize_camera():
#     try:
#         picam2 = Picamera2()
#         picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
#         picam2.start()
#         return picam2
#     except RuntimeError as e:
#         st.error(f"Failed to initialize camera: {e}")
#         return None

# # Fetch heart rate
# def fetch_heart_rate():
#     try:
#         hr = get_heart_rate(st.session_state.client)  # Assume this is synchronous for now
#         return hr
#     except Exception as e:
#         st.error(f"Error reading heart rate: {e}")
#         return None

# # Main function
# def main():
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "counter" not in st.session_state:
#         st.session_state.counter = 0

#     # Ensure client is connected
#     if not st.session_state.connected:
#         st.error("No heart rate sensor connected.")
#         time.sleep(10)
#         st.switch_page("pages/home.py")
#     elif st.session_state.workout is None:
#         st.warning("No workout selected, redirecting...")
#         time.sleep(10)
#         st.switch_page("pages/workoutlist.py")
#     else:
#         mp_drawing = mp.solutions.drawing_utils
#         mp_pose = mp.solutions.pose
#         pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

#         # Initialize camera once
#         if "picam2" not in st.session_state:
#             st.session_state.picam2 = initialize_camera()

#         if not st.session_state.picam2:
#             st.stop()  # Stop execution if the camera failed to initialize

#         picam2 = st.session_state.picam2
#         stage = None

#         # Layout containers
#         static_ui = st.container()
#         graph = st.empty()

#         # Static Part of website
#         with static_ui:
#             st.title("Heart Rate Monitor Dashboard")
#             st.write("Click the button below to end your workout.")
#             if st.button("End Workout", key="end_workout_button"):
#                 st.session_state.end_workout = True

#         # Periodically fetch and update heart rate
#         hr = fetch_heart_rate()
#         if hr is not None:
#             st.session_state.heart_rate_trend.append(hr)

#         # Dynamic Part of Website
#         while not st.session_state.end_workout:
#             oldtime = time.time() - st.session_state.start_time
#             frame = picam2.capture_array()

#             # Convert to RGB for MediaPipe
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False
#             results = pose.process(image)
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             # Draw pose landmarks
#             if results.pose_landmarks:
#                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#                 # Extract landmarks for left arm
#                 landmarks = results.pose_landmarks.landmark
#                 left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
#                 left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
#                 left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

#                 # Get coordinates and calculate angle
#                 shoulder_coords = [left_shoulder.x, left_shoulder.y]
#                 elbow_coords = [left_elbow.x, left_elbow.y]
#                 wrist_coords = [left_wrist.x, left_wrist.y]
#                 angle = calculate_angle(shoulder_coords, elbow_coords, wrist_coords)

#                 # Bicep curl counter logic
#                 if angle > 160:
#                     stage = "Down"
#                 if angle < 30 and stage == "Down":
#                     stage = "Up"
#                     st.session_state.counter += 1

#             # Update heart rate graph periodically
#             st.session_state.heart_rate_trend.append(hr if hr is not None else 0)

#             # Update only the graph area
#             with graph.container():
#                 st.write(f"Your current heart rate: {hr if hr is not None else 'Unable to fetch'} bpm")
#                 st.line_chart(st.session_state.heart_rate_trend)
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")
#                 st.write(f"{st.session_state.counter} reps")

#             # Delay to update every 1 second
#             while time.time() - st.session_state.start_time < (int(oldtime) + 1):
#                 time.sleep(0.001)

#         # Save data and end workout
#         avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#         tottime = time.time() - st.session_state.start_time
#         totalreps = 0  # Placeholder

#         st.session_state.WO_list.append(
#             datastore(tottime, avgHR, totalreps, st.session_state.workout)
#         )

#         # Reset values so next workout starts fresh
#         st.session_state.heart_rate_trend = []
#         st.session_state.end_workout = False
#         st.session_state.workout = "None"
#         st.session_state.counter = 0

#         # Switch to page with workout summaries
#         st.switch_page("pages/history.py")


# if __name__ == "__main__":
#     main()

# import streamlit as st
# import time
# import numpy as np
# import cv2
# import mediapipe as mp
# from picamera2 import Picamera2
# import asyncio
# from HRfunc import get_heart_rate
# from data import datastore

# # Function to calculate angle
# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)
#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)
#     if angle > 180.0:
#         angle = 360 - angle
#     return angle

# # Camera initialization
# def initialize_camera():
#     try:
#         picam2 = Picamera2()
#         picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
#         picam2.start()
#         return picam2
#     except RuntimeError as e:
#         st.error(f"Failed to initialize camera: {e}")
#         return None

# # Fetch heart rate asynchronously
# async def fetch_heart_rate():
#     try:
#         hr = await get_heart_rate(st.session_state.client)  # Fetch heart rate asynchronously
#         return hr
#     except Exception as e:
#         st.error(f"Error reading heart rate: {e}")
#         return None

# # Main function
# def main():
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "counter" not in st.session_state:
#         st.session_state.counter = 0

#     # Ensure client is connected
#     if not st.session_state.connected:
#         st.error("No heart rate sensor connected.")
#         time.sleep(10)
#         st.switch_page("pages/home.py")
#     elif st.session_state.workout is None:
#         st.warning("No workout selected, redirecting...")
#         time.sleep(10)
#         st.switch_page("pages/workoutlist.py")
#     else:
#         mp_drawing = mp.solutions.drawing_utils
#         mp_pose = mp.solutions.pose
#         pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

#         # Initialize camera once
#         if "picam2" not in st.session_state:
#             st.session_state.picam2 = initialize_camera()

#         if not st.session_state.picam2:
#             st.stop()  # Stop execution if the camera failed to initialize

#         picam2 = st.session_state.picam2
#         stage = None

#         # Layout containers
#         static_ui = st.container()
#         graph = st.empty()

#         # Static Part of website
#         with static_ui:
#             st.title("Heart Rate Monitor Dashboard")
#             st.write("Click the button below to end your workout.")
#             if st.button("End Workout", key="end_workout_button"):
#                 st.session_state.end_workout = True

#         # Periodically fetch and update heart rate
#         async def update_heart_rate():
#             # Await heart rate fetch and update trend
#             hr = await fetch_heart_rate()
#             if hr is not None:
#                 st.session_state.heart_rate_trend.append(hr)

#         # Run heart rate update task
#         asyncio.run(update_heart_rate())

#         # Dynamic Part of Website
#         while not st.session_state.end_workout:
#             oldtime = time.time() - st.session_state.start_time
#             frame = picam2.capture_array()

#             # Convert to RGB for MediaPipe
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False
#             results = pose.process(image)
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             # Draw pose landmarks
#             if results.pose_landmarks:
#                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#                 # Extract landmarks for left arm
#                 landmarks = results.pose_landmarks.landmark
#                 left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
#                 left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
#                 left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

#                 # Get coordinates and calculate angle
#                 shoulder_coords = [left_shoulder.x, left_shoulder.y]
#                 elbow_coords = [left_elbow.x, left_elbow.y]
#                 wrist_coords = [left_wrist.x, left_wrist.y]
#                 angle = calculate_angle(shoulder_coords, elbow_coords, wrist_coords)

#                 # Bicep curl counter logic
#                 if angle > 160:
#                     stage = "Down"
#                 if angle < 30 and stage == "Down":
#                     stage = "Up"
#                     st.session_state.counter += 1

#             # Update heart rate graph periodically
#             async def update_graph():
#                 hr = await fetch_heart_rate()  # Fetch updated heart rate
#                 st.session_state.heart_rate_trend.append(hr if hr is not None else 0)

#             asyncio.run(update_graph())

#             # Update only the graph area
#             with graph.container():
#                 #st.write(f"Your current heart rate: {st.session_state.heart_rate_trend(-1) if st.session_state.heart_rate_trend(-1) is not None else 'Unable to fetch'} bpm")
#                 st.line_chart(st.session_state.heart_rate_trend)
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")
#                 st.write(f"{st.session_state.counter} reps")

#             # Delay to update every 1 second
#             while time.time() - st.session_state.start_time < (int(oldtime) + 1):
#                 time.sleep(0.001)

#         # Save data and end workout
#         avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#         tottime = time.time() - st.session_state.start_time
#         totalreps = 0  # Placeholder

#         st.session_state.WO_list.append(
#             datastore(tottime, avgHR, totalreps, st.session_state.workout)
#         )

#         # Reset values so next workout starts fresh
#         st.session_state.heart_rate_trend = []
#         st.session_state.end_workout = False
#         st.session_state.workout = "None"
#         st.session_state.counter = 0

#         # Switch to page with workout summaries
#         st.switch_page("pages/history.py")


# if __name__ == "__main__":
#     main()


# import streamlit as st
# import time
# import numpy as np
# import cv2
# import mediapipe as mp
# from picamera2 import Picamera2
# import asyncio
# from HRfunc import get_heart_rate
# from data import datastore

# # Function to calculate angle
# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)
#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)
#     if angle > 180.0:
#         angle = 360 - angle
#     return angle

# # Camera initialization
# def initialize_camera():
#     try:
#         picam2 = Picamera2()
#         picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
#         picam2.start()
#         return picam2
#     except RuntimeError as e:
#         st.error(f"Failed to initialize camera: {e}")
#         return None

# # Fetch heart rate asynchronously
# async def fetch_heart_rate():
#     try:
#         hr = await get_heart_rate(st.session_state.client)  # Fetch heart rate asynchronously
#         return hr
#     except Exception as e:
#         st.error(f"Error reading heart rate: {e}")
#         return None

# # Main function
# def main():
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "end_workout" not in st.session_state:
#         st.session_state.end_workout = False
#     if "counter" not in st.session_state:
#         st.session_state.counter = 0

#     # Ensure client is connected
#     if not st.session_state.connected:
#         st.error("No heart rate sensor connected.")
#         time.sleep(10)
#         st.switch_page("pages/home.py")
#     elif st.session_state.workout is None:
#         st.warning("No workout selected, redirecting...")
#         time.sleep(10)
#         st.switch_page("pages/workoutlist.py")
#     else:
#         mp_drawing = mp.solutions.drawing_utils
#         mp_pose = mp.solutions.pose
#         pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

#         # Initialize camera once
#         if "picam2" not in st.session_state:
#             st.session_state.picam2 = initialize_camera()

#         if not st.session_state.picam2:
#             st.stop()  # Stop execution if the camera failed to initialize

#         picam2 = st.session_state.picam2
#         stage = None

#         # Layout containers
#         static_ui = st.container()
#         graph = st.empty()

#         # Static Part of website
#         with static_ui:
#             st.title("Heart Rate Monitor Dashboard")
#             st.write("Click the button below to end your workout.")
#             if st.button("End Workout", key="end_workout_button"):
#                 st.session_state.end_workout = True

#         # Periodically fetch and update heart rate using Streamlit's event loop
#         async def update_heart_rate():
#             # Await heart rate fetch and update trend
#             hr = await fetch_heart_rate()
#             if hr is not None:
#                 st.session_state.heart_rate_trend.append(hr)
#             st.experimental_rerun()  # Rerun the Streamlit script to update UI

#         if st.session_state.get('heart_rate_task') is None:
#             st.session_state.heart_rate_task = asyncio.create_task(update_heart_rate())

#         # Dynamic Part of Website
#         while not st.session_state.end_workout:
#             oldtime = time.time() - st.session_state.start_time
#             frame = picam2.capture_array()

#             # Convert to RGB for MediaPipe
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image.flags.writeable = False
#             results = pose.process(image)
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             # Draw pose landmarks
#             if results.pose_landmarks:
#                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#                 # Extract landmarks for left arm
#                 landmarks = results.pose_landmarks.landmark
#                 left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
#                 left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
#                 left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

#                 # Get coordinates and calculate angle
#                 shoulder_coords = [left_shoulder.x, left_shoulder.y]
#                 elbow_coords = [left_elbow.x, left_elbow.y]
#                 wrist_coords = [left_wrist.x, left_wrist.y]
#                 angle = calculate_angle(shoulder_coords, elbow_coords, wrist_coords)

#                 # Bicep curl counter logic
#                 if angle > 160:
#                     stage = "Down"
#                 if angle < 30 and stage == "Down":
#                     stage = "Up"
#                     st.session_state.counter += 1

#             # Update heart rate graph periodically
#             if len(st.session_state.heart_rate_trend) > 0:
#                 hr = st.session_state.heart_rate_trend[-1]
#             else:
#                 hr = "Unable to fetch"

#             # Update only the graph area
#             with graph.container():
#                 st.write(f"Your current heart rate: {hr} bpm")
#                 st.line_chart(st.session_state.heart_rate_trend)
#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")
#                 st.write(f"{st.session_state.counter} reps")

#             # Delay to update every 1 second
#             while time.time() - st.session_state.start_time < (int(oldtime) + 1):
#                 time.sleep(0.001)

#         # Save data and end workout
#         avgHR = sum(st.session_state.heart_rate_trend) / len(st.session_state.heart_rate_trend)
#         tottime = time.time() - st.session_state.start_time
#         totalreps = 0  # Placeholder

#         st.session_state.WO_list.append(
#             datastore(tottime, avgHR, totalreps, st.session_state.workout)
#         )

#         # Reset values so next workout starts fresh
#         st.session_state.heart_rate_trend = []
#         st.session_state.end_workout = False
#         st.session_state.workout = "None"
#         st.session_state.counter = 0

#         # Switch to page with workout summaries
#         st.switch_page("pages/history.py")


# if __name__ == "__main__":
#     main()
