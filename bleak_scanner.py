import asyncio
import re
from bleak import BleakScanner

# Regex to match names that are hex-only (e.g., 'ABC123', 'deadbeef')
hex_only_pattern = re.compile(r'^[0-9A-Fa-f]+$')

async def scan():
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name is None:
            continue  # Skip devices with no name
        if hex_only_pattern.fullmatch(d.name):
            continue  # Skip hex-only names
        print(f"Name: {d.name}, Address: {d.address}, RSSI: {d.rssi}")

asyncio.run(scan())
