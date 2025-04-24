import streamlit as st
import pandas as pd
import random
import time
import asyncio
from bleak import BleakClient, BleakScanner
from HRfunc import parse_hr_data, get_heart_rate, connect_to_heart_rate_sensor
from menu import menu
menu()

async def main():

    ###################### finish setup #####################

    #Initialize variables
    placeholder = st.empty()
    heart_rate_trend = []

    if st.session_state.connected==False:
        st.write("No heart rate sensor connected.")
    else:
        #Website data
        for seconds in range(200):
            
            with placeholder.container():
                bluetooth_data= await get_heart_rate(st.session_state.client)
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