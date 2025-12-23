import asyncio
import time
from bleak import BleakScanner
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice
from collections import defaultdict


last_seen = defaultdict(float)      # Последнее время обнаружения
seen_count = defaultdict(int)       # Сколько раз видели


def detection_callback(device: BLEDevice, adv: AdvertisementData):
    addr = device.address
    now = time.time()
    
    # Обновляем только раз в 3 секунды для одного устройства
    if now - last_seen[addr] > 300.0:
        last_seen[addr] = now
        seen_count[addr] += 1
        
        name = device.name or "[без имени]"
        rssi = adv.rssi
        manufacturer = adv.manufacturer_data
        
        print(f"{time.strftime('%H:%M:%S')}  "
              f"{name:<32}  {addr}  RSSI:{rssi:4}dBm  "
              f"seen:{seen_count[addr]:3d}  ", end="")
        
        if manufacturer:
            print("Mfr data:", list(manufacturer.keys()))
        else:
            print()


async def main():
    scanner = BleakScanner(detection_callback=detection_callback, return_adv=True)
    
    print("Непрерывное сканирование BLE (обновление каждые ~3 сек)...\n")
    
    await scanner.start()
    
    try:
        await asyncio.sleep(3600 * 24)  # 24 часа или замените на float('inf')
    except KeyboardInterrupt:
        print("\nОстановка...")
    finally:
        await scanner.stop()


if __name__ == "__main__":
    asyncio.run(main())