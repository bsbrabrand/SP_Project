# SP_Project
Final project for ME 5194


The webpage for information display is made using the streamlit library:

the home page is defined in home.py, and the rest of the pages are defined in the pages folder
streamlit also uses menu.py for a menu function for navigation

HRfunc.py contains the functions used for connecting and retriving heart rate values from the HR monitor.

data.py provides the class to store workout information for use in the workout history page.

datatransferpi.py and datatransferpc.py include functions to initialize a TCP connection between a pc and the raspberry pi

BicepCurlCountCode.py runs on the pi to count bicep curls and send the amount to the pc
