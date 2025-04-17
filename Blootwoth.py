import asyncio
from bleak import BleakClient

# Replace with your actual device's BLE MAC address
ADDRESS = "XX:XX:XX:XX:XX:XX"

# UUID for Heart Rate Measurement (standard for BLE HRM devices)
HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

def handle_hr_data(sender, data):
    # First byte is flags, second byte is heart rate value (if no extended format)
    hr_value = data[1]
    print(f"Heart Rate: {hr_value} bpm")

async def main():
    async with BleakClient(ADDRESS) as client:
        print("Connected:", await client.is_connected())

        # Start receiving notifications from heart rate measurement characteristic
        await client.start_notify(HR_UUID, handle_hr_data)

        print("Listening for heart rate data... (press Ctrl+C to stop)")
        await asyncio.sleep(60)  # Keep listening for 60 seconds

        await client.stop_notify(HR_UUID)

asyncio.run(main())
