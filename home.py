# import streamlit as st
# from menu import menu
# import time
# import asyncio
# from HRfunc import connect_ble_client

# ############### setup webpage #############################
# st.set_page_config(
#     page_title="Heart Rate Dashboard",
#     page_icon="♥️",
#     layout="wide",
# )
# hide_default_format = """
#     <style>
#     #MainMenu {visibility: hidden; }
#     footer {visibility: hidden;}
#     </style>
#     """
# st.markdown(hide_default_format, unsafe_allow_html=True)

# #Global variables
# st.session_state.connected = True
# st.session_state.ID = "00002a37-0000-1000-8000-00805f9b34fb"
# st.session_state.workout = None
# st.session_state.WO_list = []
# menu()
# st.title("Heart Rate Workout Monitor Home")
# st.write("This project was made by Bennett Brabrand and Riley Fry for ME 5194 at The Ohio State University. To begin, please connect a heart rate monitor from the menu.")
# st.write("To begin, connect a heart rate monitor using the button below")
# if st.button("Press to connect to bluetooth device"):
#         try:
#             with st.spinner("Attempting to connect", show_time=True):
#                 if "ble_client" not in st.session_state:
#                     st.session_state.ble_client = connect_ble_client()
#                     st.write(st.session_state.ble_client)
#             if st.session_state.ble_client != None:
#                 st.success("HR Monitor Connected!, redirecting...")
#                 st.session_state.connected=True
#             time.sleep(3)
#             st.switch_page("pages/workoutlist.py")
#         except TimeoutError:
#             st.warning("Unable to connect. Timeout error")

# import streamlit as st
# from menu import menu
# import time
# import asyncio
# from HRfunc import connect_ble_client

# ############### setup webpage #############################
# st.set_page_config(
#     page_title="Heart Rate Dashboard",
#     page_icon="♥️",
#     layout="wide",
# )
# hide_default_format = """
#     <style>
#     #MainMenu {visibility: hidden; }
#     footer {visibility: hidden;}
#     </style>
#     """
# st.markdown(hide_default_format, unsafe_allow_html=True)

# # Global variables
# st.session_state.connected = True
# st.session_state.ID = "00002a37-0000-1000-8000-00805f9b34fb"
# st.session_state.workout = None
# st.session_state.WO_list = []
# menu()
# st.title("Heart Rate Workout Monitor Home")
# st.write("This project was made by Bennett Brabrand and Riley Fry for ME 5194 at The Ohio State University. To begin, please connect a heart rate monitor from the menu.")
# st.write("To begin, connect a heart rate monitor using the button below")

# # Async wrapper for connecting to BLE device
# async def connect_to_ble():
#     if "ble_client" not in st.session_state:
#         st.session_state.ble_client = await connect_ble_client()  # Ensure you await the connection here
#     return st.session_state.ble_client

# # Button to trigger BLE connection
# if st.button("Press to connect to bluetooth device"):
#     try:
#         with st.spinner("Attempting to connect", show_time=True):
#             # Using asyncio.run() to handle async function in Streamlit
#             ble_client = asyncio.run(connect_to_ble())  # Run the async function
#             st.write(ble_client)  # Show the client object
#         if ble_client is not None:
#             st.success("HR Monitor Connected!, redirecting...")
#             st.session_state.connected = True
#         time.sleep(3)
#         st.switch_page("pages/workoutlist.py")
#     except TimeoutError:
#         st.warning("Unable to connect. Timeout error")
#     except Exception as e:
#         st.warning(f"Error occurred: {e}")


# import streamlit as st
# from menu import menu
# import time
# import asyncio
# from HRfunc import connect_ble_client

# ############### setup webpage #############################
# st.set_page_config(
#     page_title="Heart Rate Dashboard",
#     page_icon="♥️",
#     layout="wide",
# )
# hide_default_format = """
#     <style>
#     #MainMenu {visibility: hidden; }
#     footer {visibility: hidden;}
#     </style>
#     """
# st.markdown(hide_default_format, unsafe_allow_html=True)

# # Global variables
# st.session_state.connected = True
# st.session_state.ID = "00002a37-0000-1000-8000-00805f9b34fb"
# st.session_state.workout = None
# st.session_state.WO_list = []
# menu()
# st.title("Heart Rate Workout Monitor Home")
# st.write("This project was made by Bennett Brabrand and Riley Fry for ME 5194 at The Ohio State University. To begin, please connect a heart rate monitor from the menu.")
# st.write("To begin, connect a heart rate monitor using the button below")

# # Async wrapper for connecting to BLE device
# async def connect_to_ble():
#     if "ble_client" not in st.session_state:
#         st.session_state.ble_client = await connect_ble_client()  # Ensure you await the connection here
#     return st.session_state.ble_client

# # Button to trigger BLE connection
# if st.button("Press to connect to bluetooth device"):
#     try:
#         with st.spinner("Attempting to connect", show_time=True):
#             # Get the current event loop
#             try:
#                 loop = asyncio.get_event_loop()
#             except RuntimeError as e:
#                 if 'no current event loop' in str(e):
#                     # Create a new event loop if there's no current loop
#                     loop = asyncio.new_event_loop()
#                     asyncio.set_event_loop(loop)

#             # Use asyncio.create_task to run the async task
#             task = loop.create_task(connect_to_ble())  # Schedule the async task
#             ble_client = loop.run_until_complete(task)  # Await the result of the task
#             st.write(ble_client)  # Show the client object

#         if ble_client is not None:
#             st.success("HR Monitor Connected!, redirecting...")
#             st.session_state.connected = True
#         time.sleep(3)
#         st.switch_page("pages/workoutlist.py")
#     except TimeoutError:
#         st.warning("Unable to connect. Timeout error")
#     except Exception as e:
#         st.warning(f"Error occurred: {e}")


import streamlit as st
import time
import asyncio
from HRfunc import connect_ble_client

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

# Global variables
st.session_state.connected = True
st.session_state.ID = "00002a37-0000-1000-8000-00805f9b34fb"
st.session_state.workout = None
st.session_state.WO_list = []
menu()
st.title("Heart Rate Workout Monitor Home")
st.write("This project was made by Bennett Brabrand and Riley Fry for ME 5194 at The Ohio State University. To begin, please connect a heart rate monitor from the menu.")
st.write("To begin, connect a heart rate monitor using the button below")

# Async wrapper for connecting to BLE device
async def connect_to_ble():
    if "ble_client" not in st.session_state:
        st.session_state.ble_client = await connect_ble_client()  # Ensure you await the connection here
    return st.session_state.ble_client

# Button to trigger BLE connection
if st.button("Press to connect to bluetooth device"):
    try:
        with st.spinner("Attempting to connect", show_time=True):
            # Get the current event loop
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError as e:
                if 'no current event loop' in str(e):
                    # Create a new event loop if there's no current loop
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

            # Use asyncio.run to run the main task, ensuring that the task runs in the same loop
            ble_client = asyncio.run(connect_to_ble())  # Ensure the BLE client is connected on the correct event loop

            # Log the BLE client object for debugging
            st.write(ble_client)  

        if ble_client is not None:
            st.success("HR Monitor Connected!, redirecting...")
            st.session_state.connected = True
        time.sleep(3)
        st.switch_page("pages/workoutlist.py")
    except TimeoutError:
        st.warning("Unable to connect. Timeout error")
    except Exception as e:
        st.warning(f"Error occurred: {e}")
