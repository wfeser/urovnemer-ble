import asyncio
from bleak import BleakScanner, BLEDevice, AdvertisementData

# Example: Filter for devices advertising the Heart Rate Service (UUID: 0x180D)
HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"

def detection_callback(device: BLEDevice, advertisement_data: AdvertisementData):
    print(f"Found device: {device.address} ({device.name})")
    # You can also check advertisement_data.service_uuids here if needed

async def run_filtered_scan():
    print("Scanning for HR devices...")
    scanner = BleakScanner(
        detection_callback=detection_callback,
        service_uuids=[HR_SERVICE_UUID] # Filter by service UUID
    )
    await scanner.start()
    await asyncio.sleep(5.0) # Scan for 5 seconds
    await scanner.stop()

async def main():
    await run_filtered_scan()

if __name__ == "__main__":
    asyncio.run(main())