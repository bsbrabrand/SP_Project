import streamlit as st
import pandas as pd
import random
import time
import asyncio
from bleak import BleakClient, BleakScanner
from HRfunc import parse_hr_data, get_heart_rate, connect_to_heart_rate_sensor
#from blueTooth import monitor

# UUID for Heart Rate Measurement (standard for BLE HRM devices)
HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# Global variable to store the heart rate
current_heart_rate = None

async def main():
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

    ###################### finish setup #####################

    #Initialize variables
    placeholder = st.empty()
    heart_rate_trend = []

    #Initialize sensor
    client = await connect_to_heart_rate_sensor()


    #Website data
    for seconds in range(200):
        
        with placeholder.container():
            bluetooth_data= await get_heart_rate(client)
            heart_rate_trend.append(bluetooth_data)
            #For rolling window
            #if len(heart_rate_trend)>30:
            #    heart_rate_trend.pop(0)


            st.title("Heart rate monitor dashboard")
            st.write(f"your current heart rate is: {int(bluetooth_data)} bpm")

            st.line_chart(heart_rate_trend)
            time.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())