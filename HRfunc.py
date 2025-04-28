# import asyncio
# from bleak import BleakClient, BleakScanner

# # UUID for Heart Rate Measurement (standard for BLE HRM devices)
# global HR_UUID
# HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# # Global variable to store the heart rate
# current_heart_rate = None

# def parse_hr_data(sender, data):
#     global current_heart_rate
#     flags = data[0]
#     hr_format = flags & 0x01

#     if hr_format == 0:
#         current_heart_rate = data[1]
#     else:
#         current_heart_rate = int.from_bytes(data[1:3], byteorder='little')

# async def connect_to_heart_rate_sensor():
#     """Connect to the BLE heart rate sensor and start receiving notifications."""
#     # Discover devices
#     devices = await BleakScanner.discover(timeout=10)
#     hr_device = None
#     for d in devices:
#         if "HRM" in str(d.name):
#             hr_device = d
#             break

#     if hr_device is None:
#         raise Exception("Heart rate monitor not found.")

#     # Connect to the heart rate sensor
#     client = BleakClient(hr_device.address)
#     await client.connect()
    
#     # Start receiving heart rate notifications
#     await client.start_notify(HR_UUID, parse_hr_data)
#     return client



# async def _get_heart_rate(client):
#     """Retrieve the current heart rate value."""
#     global current_heart_rate
#     current_heart_rate = None  # Reset before reading
#     await client.start_notify(HR_UUID, parse_hr_data)

#     # Wait for a short period to receive the heart rate value
#     for _ in range(100):  # max wait ~5 seconds
#         await asyncio.sleep(0.25)
#         if current_heart_rate is not None:
#             break

#     if current_heart_rate is None:
#         raise Exception("Failed to receive heart rate data.")
    
#     return current_heart_rate

# def get_heart_rate(client):
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         # No loop in this thread → create one manually
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)

#     return loop.run_until_complete(_get_heart_rate(client))

# async def disconnect_from_heart_rate_sensor(name,ID):
#     await name.stop_notify(ID)
#     await name.disconnect()

# # Example usage
# async def main():
#     try:
#         # Step 1: Connect to the sensor
#         client = await connect_to_heart_rate_sensor()

#         # Step 2: Get the current heart rate
#         heart_rate = await get_heart_rate(client)
#         print(f"Current heart rate: {heart_rate} bpm")

#         # Stop notifications and disconnect
#         await disconnect_from_heart_rate_sensor(client,HR_UUID)

#     except Exception as e:
#         print(f"Error: {e}")

# # Run the example
# if __name__ == "__main__":
#     asyncio.run(main())


# import asyncio
# from bleak import BleakClient, BleakScanner

# HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# def parse_hr_data(sender, data):
#     flags = data[0]
#     hr_format = flags & 0x01
#     if hr_format == 0:
#         return data[1]
#     else:
#         return int.from_bytes(data[1:3], byteorder='little')

# async def _get_heart_rate():
#     heart_rate = None

#     def handle_hr(sender, data):
#         nonlocal heart_rate
#         heart_rate = parse_hr_data(sender, data)

#     devices = await BleakScanner.discover(timeout=10)
#     hr_device = next((d for d in devices if "HRM" in str(d.name)), None)

#     if not hr_device:
#         raise Exception("Heart rate monitor not found.")

#     async with BleakClient(hr_device) as client:
#         await client.start_notify(HR_UUID, handle_hr)

#         # Wait up to 5 seconds for a heart rate reading
#         for _ in range(20):
#             await asyncio.sleep(0.25)
#             if heart_rate is not None:
#                 break

#         await client.stop_notify(HR_UUID)

#     if heart_rate is None:
#         raise Exception("Failed to receive heart rate data.")

#     return heart_rate

# def get_heart_rate():
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)

#     return loop.run_until_complete(_get_heart_rate())

# def connect_to_heart_rate_sensor():
#     async def _connect():
#         devices = await BleakScanner.discover(timeout=10)
#         hr_device = next((d for d in devices if "HRM" in str(d.name)), None)
#         if not hr_device:
#             raise Exception("HRM not found")
#         client = BleakClient(hr_device)
#         await client.connect()
#         return client

#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#     return loop.run_until_complete(_connect())


# HRfunc.py
# import asyncio
# from bleak import BleakClient, BleakScanner

# HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# def parse_hr_data(sender, data):
#     flags = data[0]
#     hr_format = flags & 0x01
#     if hr_format == 0:
#         return data[1]
#     else:
#         return int.from_bytes(data[1:3], byteorder='little')

# def connect_ble_client():
#     async def _connect():
#         devices = await BleakScanner.discover(timeout=10)
#         hr_device = next((d for d in devices if "HRM" in str(d.name)), None)
#         if not hr_device:
#             raise Exception("Heart rate monitor not found.")
#         client = BleakClient(hr_device)
#         await client.connect()
#         return client

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(_connect())

# def start_heart_rate_notifications(client, update_func):
#     async def _start():
#         await client.start_notify(HR_UUID, update_func)

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(_start())

# def stop_ble_client(client):
#     async def _stop():
#         try:
#             await client.stop_notify(HR_UUID)
#         except:
#             pass
#         await client.disconnect()

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(_stop())


# HRfunc.py
# import asyncio
# from bleak import BleakClient, BleakScanner

# HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# def parse_hr_data(sender, data):
#     flags = data[0]
#     hr_format = flags & 0x01
#     print(data)
#     print("test")
#     if hr_format == 0:
#         return data[1]
#     else:
#         return int.from_bytes(data[1:3], byteorder='little')

# def connect_ble_client():
#     async def _connect():
#         devices = await BleakScanner.discover(timeout=10)
#         hr_device = next((d for d in devices if "HRM" in str(d.name)), None)
#         if not hr_device:
#             raise Exception("Heart rate monitor not found.")
#         client = BleakClient(hr_device)
#         await client.connect()
#         print("✅ BLE connected to:", hr_device.name)
#         return client

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(_connect())

# def start_heart_rate_notifications(client, update_func):
#     async def _start():
#         await client.start_notify(HR_UUID, update_func)
#         print("✅ Started heart rate notifications.")

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(_start())

# def stop_ble_client(client):
#     async def _stop():
#         try:
#             await client.stop_notify(HR_UUID)
#             print("🔌 Stopped notifications.")
#         except Exception as e:
#             print("⚠️ Error stopping notify:", e)
#         await client.disconnect()
#         print("🛑 BLE client disconnected.")

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(_stop())

# import asyncio
# from bleak import BleakClient, BleakScanner
# import threading

# HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# def parse_hr_data(sender, data):
#     flags = data[0]
#     hr_format = flags & 0x01
#     if hr_format == 0:
#         return data[1]
#     else:
#         return int.from_bytes(data[1:3], byteorder='little')

# def connect_ble_client():
#     async def _connect():
#         devices = await BleakScanner.discover(timeout=10)
#         print("Discovered devices:", [d.name for d in devices])  # Optional debug
#         hr_device = next((d for d in devices if "HRM" in str(d.name)), None)
#         if not hr_device:
#             raise Exception("Heart rate monitor not found.")
#         client = BleakClient(hr_device)
#         await client.connect()
#         print("✅ BLE connected to:", hr_device.name)
#         return client

#     # 💡 Always use a fresh event loop
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(_connect())

# # def start_heart_rate_notifications(client, update_func):
# #     async def _start():
# #         await client.start_notify(HR_UUID, update_func)
# #         print("✅ Started heart rate notifications.")

# #     loop = asyncio.new_event_loop()
# #     asyncio.set_event_loop(loop)
# #     loop.run_until_complete(_start())

# def start_heart_rate_notifications(client, update_func):
#     def run():
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)

#         async def _start():
#             await client.start_notify(HR_UUID, update_func)
#             print("✅ Started heart rate notifications.")

#         loop.run_until_complete(_start())
#         loop.run_forever()  # Keeps the loop alive for BLE notifications

#     thread = threading.Thread(target=run, daemon=True)
#     thread.start()

# def stop_ble_client(client):
#     async def _stop():
#         try:
#             await client.stop_notify(HR_UUID)
#             print("🔌 Stopped notifications.")
#         except Exception as e:
#             print("⚠️ Error stopping notify:", e)
#         await client.disconnect()
#         print("🛑 BLE client disconnected.")

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(_stop())


# import asyncio
# import threading
# from bleak import BleakClient, BleakScanner

# HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# def parse_hr_data(sender, data):
#     flags = data[0]
#     hr_format = flags & 0x01
#     if hr_format == 0:
#         return data[1]
#     else:
#         return int.from_bytes(data[1:3], byteorder='little')

# def connect_ble_client():
#     async def _connect():
#         devices = await BleakScanner.discover(timeout=10)
#         print("Discovered devices:", [d.name for d in devices])
#         hr_device = next((d for d in devices if "HRM" in str(d.name)), None)
#         if not hr_device:
#             raise Exception("Heart rate monitor not found.")
#         client = BleakClient(hr_device)
#         await client.connect()
#         print("✅ BLE connected to:", hr_device.name)
#         return client

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(_connect())

# def start_heart_rate_notifications(client, thread_safe_callback):
#     def run():
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)

#         async def _start():
#             async def bleak_callback(sender, data):
#                 hr = parse_hr_data(sender, data)
#                 print(f"📥 HR notify received: {hr}")
#                 thread_safe_callback(hr)

#             await client.start_notify(HR_UUID, bleak_callback)
#             print("✅ Started heart rate notifications.")
#             # Keep loop running for notifications
#             while True:
#                 await asyncio.sleep(1)

#         loop.run_until_complete(_start())

#     thread = threading.Thread(target=run, daemon=True)
#     thread.start()

# def stop_ble_client(client):
#     async def _stop():
#         try:
#             await client.stop_notify(HR_UUID)
#             print("🔌 Stopped notifications.")
#         except Exception as e:
#             print("⚠️ Error stopping notify:", e)
#         await client.disconnect()
#         print("🛑 BLE client disconnected.")

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(_stop())

# import asyncio
# import threading
# from bleak import BleakClient, BleakScanner

# HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# def parse_hr_data(sender, data):
#     flags = data[0]
#     hr_format = flags & 0x01
#     if hr_format == 0:
#         return data[1]
#     else:
#         return int.from_bytes(data[1:3], byteorder='little')

# def connect_ble_client():
#     async def _connect():
#         devices = await BleakScanner.discover(timeout=10)
#         hr_device = next((d for d in devices if "HRM" in str(d.name)), None)
#         if not hr_device:
#             raise Exception("Heart rate monitor not found.")
#         client = BleakClient(hr_device)
#         await client.connect()
#         print("✅ BLE connected to:", hr_device.name)
#         return client

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(_connect())

# def start_heart_rate_notifications(client, update_func):
#     async def _start():
#         await client.start_notify(HR_UUID, update_func)
#         print("✅ Started heart rate notifications.")

#     loop = asyncio.new_event_loop()  # New event loop per thread to avoid asyncio error
#     threading.Thread(target=run_async, args=(loop, _start)).start()

# def run_async(loop, coro):
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(coro())

# def stop_ble_client(client):
#     async def _stop():
#         try:
#             await client.stop_notify(HR_UUID)
#             print("🔌 Stopped notifications.")
#         except Exception as e:
#             print("⚠️ Error stopping notify:", e)
#         await client.disconnect()
#         print("🛑 BLE client disconnected.")

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(_stop())

# import asyncio
# import threading
# from bleak import BleakClient, BleakScanner

# HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# def parse_hr_data(sender, data):
#     flags = data[0]
#     hr_format = flags & 0x01
#     if hr_format == 0:
#         return data[1]
#     else:
#         return int.from_bytes(data[1:3], byteorder='little')

# def connect_ble_client():
#     async def _connect():
#         devices = await BleakScanner.discover(timeout=10)
#         hr_device = next((d for d in devices if "HRM" in str(d.name)), None)
#         if not hr_device:
#             raise Exception("Heart rate monitor not found.")
#         client = BleakClient(hr_device)
#         await client.connect()
#         print("✅ BLE connected to:", hr_device.name)
#         return client

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(_connect())

# def start_heart_rate_notifications(client, update_func):
#     async def _start():
#         await client.start_notify(HR_UUID, update_func)
#         print("✅ Started heart rate notifications.")

#     loop = asyncio.new_event_loop()
#     threading.Thread(target=run_async, args=(loop, _start)).start()

# def run_async(loop, coro):
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(coro())

# def stop_ble_client(client):
#     async def _stop():
#         try:
#             await client.stop_notify(HR_UUID)
#             print("🔌 Stopped notifications.")
#         except Exception as e:
#             print("⚠️ Error stopping notify:", e)
#         await client.disconnect()
#         print("🛑 BLE client disconnected.")

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(_stop())

# import asyncio
# from bleak import BleakClient, BleakScanner

# HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# def parse_hr_data(sender, data):
#     flags = data[0]
#     hr_format = flags & 0x01
#     print(data)
#     if hr_format == 0:
#         return data[1]
#     else:
#         return int.from_bytes(data[1:3], byteorder='little')

# async def connect_ble_client():
#     devices = await BleakScanner.discover(timeout=10)
#     hr_device = next((d for d in devices if "HRM" in str(d.name)), None)
#     if not hr_device:
#         raise Exception("Heart rate monitor not found.")
#     client = BleakClient(hr_device)
#     await client.connect()
#     print("✅ BLE connected to:", hr_device.name)
#     return client

# async def start_heart_rate_notifications(client, update_func):
#     await client.start_notify(HR_UUID, update_func)
#     print("✅ Started heart rate notifications.")

# async def stop_ble_client(client):
#     try:
#         await client.stop_notify(HR_UUID)
#         print("🔌 Stopped notifications.")
#     except Exception as e:
#         print("⚠️ Error stopping notify:", e)
#     await client.disconnect()
#     print("🛑 BLE client disconnected.")


import asyncio
from bleak import BleakClient, BleakScanner

HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

def parse_hr_data(sender, data):
    flags = data[0]
    hr_format = flags & 0x01
    if hr_format == 0:
        return data[1]
    else:
        return int.from_bytes(data[1:3], byteorder='little')

async def connect_ble_client():
    devices = await BleakScanner.discover(timeout=10)
    hr_device = next((d for d in devices if "HRM" in str(d.name)), None)
    if not hr_device:
        raise Exception("Heart rate monitor not found.")
    client = BleakClient(hr_device)
    await client.connect()
    print("✅ BLE connected to:", hr_device.name)
    return client

async def start_heart_rate_notifications(client, update_func):
    await client.start_notify(HR_UUID, update_func)
    print("✅ Started heart rate notifications.")

async def stop_ble_client(client):
    try:
        await client.stop_notify(HR_UUID)
        print("🔌 Stopped notifications.")
    except Exception as e:
        print("⚠️ Error stopping notify:", e)
    await client.disconnect()
    print("🛑 BLE client disconnected.")
