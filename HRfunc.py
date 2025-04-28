import asyncio
from bleak import BleakClient, BleakScanner

# UUID for Heart rate
global HR_UUID
HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# Global variable to store the heart rate
current_heart_rate = None

def parse_hr_data(sender, data):
    global current_heart_rate
    flags = data[0]
    hr_format = flags & 0x01

    if hr_format == 0:
        current_heart_rate = data[1]
    else:
        current_heart_rate = int.from_bytes(data[1:3], byteorder='little')

async def connect_to_heart_rate_sensor():
    """Connect to the heart rate sensor and start notifications"""
    # Discover bluetooth devices
    devices = await BleakScanner.discover(timeout=10)
    hr_device = None
    for d in devices:
        if "HRM" in str(d.name): #change "HRM" here for a different HR monitor
            hr_device = d
            break

    if hr_device is None:
        raise Exception("Heart rate monitor not found.")

    # Connect to the heart rate monitor
    client = BleakClient(hr_device.address)
    await client.connect()
    
    # Start heart rate notifications
    await client.start_notify(HR_UUID, parse_hr_data)
    return client

async def get_heart_rate(client):
    """get the current heart rate value."""
    global current_heart_rate
    current_heart_rate = None  # Reset before reading
    await client.start_notify(HR_UUID, parse_hr_data)

    # Wait a bit to get the heart rate value
    for _ in range(100):  # max wait of 20 seconds
        await asyncio.sleep(0.25)
        if current_heart_rate is not None:
            break

    if current_heart_rate is None:
        raise Exception("Failed to receive heart rate data.")
    return current_heart_rate

#Just crashes whenever attempted, don't use
async def disconnect_from_heart_rate_sensor(name,ID):
    '''disconect from the HR sensor (doesn't work)'''
    await name.stop_notify(ID)
    await name.disconnect()