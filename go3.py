import asyncio
import binascii

from bleak import BleakClient, BleakGATTCharacteristic

SCALE_MAC = "A0:E6:F8:C6:43:56"
WEIGHT_CHARACTERISTIC_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"

def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    print(f"{characteristic.description}: {binascii.hexlify(data)}")

async def main():
    
    print(f"Connecting... {SCALE_MAC}")
    
    client = BleakClient(SCALE_MAC)
    try:
        await client.connect(timeout=10.0)
        if not client.is_connected:
            print("  Не удалось подключиться")
        else:
            print("  Успешно подключено!")
            
        await client.pair(protection_level=2)
            
            
        services = client.services
        
        if services:  # Это работает всегда
            # Если нужно точное число — преобразуем
            print(f"  Найдено сервисов: {len(list(services))}")
            for service in services:
                print(f"    Сервис: {service.uuid} — {service.description or 'Нет описания'}")
                for char in service.characteristics:
                    props = ", ".join(char.properties)
                    print(f"      ├─ {char.uuid} ({props}) — {char.description or ''}")
        else:
            print("  Сервисы не обнаружены или доступ запрещён")
                
    except Exception as e:
        print(f"  Ошибка: {e}")
        
    finally:
        if client.is_connected:
            await client.disconnect()
        print("-" * 80)

asyncio.run(main())