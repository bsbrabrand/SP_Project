import streamlit as st
import pandas as pd
import random
import time
import asyncio
from bleak import BleakClient, BleakScanner
from HRfunc import parse_hr_data, get_heart_rate, connect_to_heart_rate_sensor
from menu import menu
menu()

def main():

    ###################### finish setup #####################

    #Initialize variables
    placeholder = st.empty()
    heart_rate_trend = []

    if st.session_state.connected==False:
        st.write("No heart rate sensor connected.")
    elif st.session_state.workout == None:
        st.write("No workout selected, redirecting")
        time.sleep(2)
        st.switch_page("pages/workoutlist.py")
    else:
        #Website data
        st.session_state.start_time=time.time()
        for _ in range(200):
            with placeholder.container():
                oldtime = time.time()-st.session_state.start_time
                bluetooth_data= asyncio.run(get_heart_rate(st.session_state.client))
                heart_rate_trend.append(bluetooth_data)
                #For rolling window
                #if len(heart_rate_trend)>30:
                #    heart_rate_trend.pop(0)
                st.title("Heart rate monitor dashboard")
                st.write(f"your current heart rate is: {int(bluetooth_data)} bpm")

                st.line_chart(heart_rate_trend)
                #time.sleep(1)
                currenttime = time.time()-st.session_state.start_time
                while currenttime < (int(oldtime)+1):
                    time.sleep(0.001)
                    currenttime = time.time()-st.session_state.start_time

                st.write(f"Timer: {int(currenttime)} seconds")

if __name__ == "__main__":
    main()

########break############



# import streamlit as st
# import time
# import asyncio
# from HRfunc import get_heart_rate, connect_to_heart_rate_sensor
# from menu import menu
# from streamlit_autorefresh import st_autorefresh

# menu()

# def main():
#     placeholder = st.empty()

#     # Set up session state
#     if "start_time" not in st.session_state:
#         st.session_state.start_time = time.time()

#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []

#     if "client" not in st.session_state:
#         st.session_state.client = asyncio.run(connect_to_heart_rate_sensor())

#     # UI logic
#     if not st.session_state.connected:
#         st.write("No heart rate sensor connected.")
#     elif st.session_state.workout is None:
#         st.write("No workout selected, redirecting...")
#         time.sleep(2)
#         st.switch_page("pages/workoutlist.py")
#     else:
#         # Fetch HR data
#         try:
#             bluetooth_data = asyncio.run(get_heart_rate(st.session_state.client))
#             st.session_state.heart_rate_trend.append(bluetooth_data)

#             # Rolling window (optional)
#             if len(st.session_state.heart_rate_trend) > 30:
#                 st.session_state.heart_rate_trend.pop(0)

#             # UI update
#             with placeholder.container():
#                 st.title("Heart rate monitor dashboard")
#                 st.write(f"Your current heart rate is: {int(bluetooth_data)} bpm")
#                 st.line_chart(st.session_state.heart_rate_trend)

#                 elapsed = int(time.time() - st.session_state.start_time)
#                 st.write(f"Timer: {elapsed} seconds")

#         except Exception as e:
#             st.error(f"Error reading heart rate: {e}")

#         # Auto-refresh the page every second
#         st_autorefresh(interval=1000, key="heartbeat_refresh")


# if __name__ == "__main__":
#     main()

# import streamlit as st
# import time
# import asyncio
# from HRfunc import get_heart_rate, connect_to_heart_rate_sensor
# from menu import menu

# menu()

# def get_event_loop():
#     """Helper to get or create an event loop."""
#     try:
#         return asyncio.get_event_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         return loop

# def main():
#     placeholder = st.empty()

#     # Init session state
#     if "start_time" not in st.session_state:
#         st.session_state.start_time = time.time()
#     if "heart_rate_trend" not in st.session_state:
#         st.session_state.heart_rate_trend = []
#     if "client" not in st.session_state:
#         st.session_state.client = get_event_loop().run_until_complete(connect_to_heart_rate_sensor())

#     if not st.session_state.connected:
#         st.write("No heart rate sensor connected.")
#         return

#     if st.session_state.workout is None:
#         st.write("No workout selected, redirecting...")
#         time.sleep(2)
#         st.switch_page("pages/workoutlist.py")
#         return

#     # Data update loop — runs once per rerun (not full page refresh)
#     for _ in range(1):  # run once per render, allows us to rerun cleanly
#         client = st.session_state.client
#         try:
#             bluetooth_data = get_event_loop().run_until_complete(get_heart_rate(client))
#             st.session_state.heart_rate_trend.append(bluetooth_data)

#             if len(st.session_state.heart_rate_trend) > 30:
#                 st.session_state.heart_rate_trend.pop(0)

#         except Exception as e:
#             st.error(f"Error reading heart rate: {e}")
#             return

#         # UI update
#         with placeholder.container():
#             st.title("Heart rate monitor dashboard")
#             st.write(f"Your current heart rate is: {int(bluetooth_data)} bpm")
#             st.line_chart(st.session_state.heart_rate_trend)
#             current_time = int(time.time() - st.session_state.start_time)
#             st.write(f"Timer: {current_time} seconds")

#         time.sleep(1)
#         st.rerun()  # light refresh, only re-triggers Streamlit without full reload

# if __name__ == "__main__":
#     main()
