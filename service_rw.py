import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_ADDRESS='C2:F1:F7:0F:25:F5'
#SR_UUID='0000180d-0000-1000-8000-00805f9b34fb'
#CH_UUID='00002a39-0000-1000-8000-00805f9b34fb'
CH_UUID='00002a25-0000-1000-8000-00805f9b34fb' # serial number

async def main():
        
    client = BleakClient(DEVICE_ADDRESS)
    try:
        print("  Подключение...", end=" ")
        await client.connect(timeout=15.0)  # Таймаут подключения
        if client.is_connected:
            print("Успешно!")
            
            try:
                res = await client.pair(protection_level=1)
                print(f'--Pair: {res}')
                                
                # Самый простой вариант — указываем UUID характеристики напрямую
                value = await client.read_gatt_char(CH_UUID)
                print(f"Значение характеристики {CH_UUID}:")
                print(f"  Bytes: {value}      Hex:   {value.hex()}")
                # Если данные текстовые:
                #try:
                #    print(f"  Text:  {value.decode('utf-8')}")
                #except UnicodeDecodeError:
                #    print("  (не текст в utf-8)")
                    
            except Exception as e:
                print(f"Ошибка чтения характеристики: {e}")

        
        
        else:
            print("Не удалось подключиться")
            
    except asyncio.TimeoutError:
        print("Таймаут подключения")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    finally:
        if client.is_connected:
            print("  Отключение")
            await client.disconnect()
        print("===== Done =====")

# Запуск
asyncio.run(main())

