import asyncio
from bleak import BleakClient, BleakScanner
import time

# Replace with your actual device's BLE MAC address
ADDRESS = "F3:7C:B0:DD:7C:D0"

# UUID for Heart Rate Measurement (standard for BLE HRM devices)
HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

def parse_hr_data(event, data):
    # First byte is flags
    flags = data[0]
    hr_format = flags & 0x01

    if hr_format == 0:
        # 8-bit heart rate
        hr_value = data[1]
    else:
        # 16-bit heart rate
        hr_value = int.from_bytes(data[1:3], byteorder='little')
    
    print(f"Time: {time.time()} | Heart Rate: {hr_value} bpm")

async def read_heart_rate(client):
    data = await client.read_gatt_char(HR_UUID)
    print(data)
    parse_hr_data(data)

async def main():

    devices = await BleakScanner.discover(timeout=15)
    for d in devices:
        print(d.name)
        if "HRM" in str(d.name):
            print(f"found device with addr {d.address}")
            async with BleakClient(d.address, timeout=15) as client:
                try:
                    await client.start_notify(HR_UUID, parse_hr_data)
                    while True:
                        await asyncio.sleep(0.25)
                        pass
                    print("Listening for HR notifications for 30s...")
                except KeyboardInterrupt:
                    await client.stop_notify(HR_UUID)


asyncio.run(main())
