import asyncio
from bleak import BleakScanner, BleakClient


PROTECTION_LEVEL=1

async def main():
    print("Сканирование BLE-устройств (10 секунд)...\n")
    
    # Сканируем с полными advertisement-данными
    discovered = await BleakScanner.discover(timeout=15.0, return_adv=True)
    
    if not discovered:
        print("Устройства не найдены.")
        return
    
    print(f"Найдено {len(discovered)} уникальных устройств.\n")
    print("Начинаем подключение и опрос сервисов у каждого...\n")
    
    for key, (device, adv_data) in discovered.items():
        name = adv_data.local_name or device.name or "Неизвестно"
        print(f"Устройство: {device.address}")
        print(f"  Имя: {name}")
        print(f"  RSSI: {adv_data.rssi} dBm")
        
        client = BleakClient(device.address)
        try:
            print("  Подключение...", end=" ")
            await client.connect(timeout=15.0)  # Таймаут подключения
            if client.is_connected:
                print("Успешно!")
                
                res = await client.pair(protection_level=PROTECTION_LEVEL)
                print(f'--Pair: {res}')

                # Получаем сервисы
                services = client.services  # Это BleakGATTServiceCollection
                
                # Проверка на наличие сервисов — работает без len()
                if services:
                    print(f"  Найдено сервисов: {len(list(services))}")  # Если очень хочется число — преобразуем в list
                    for service in services:
                        print(f"    Сервис: {service.uuid}")
                        print(f"      Описание: {service.description or 'Нет описания'}")
                        
                        characteristics = service.characteristics
                        if characteristics:
                            print("      Характеристики:")
                            for char in characteristics:
                                props = ", ".join(char.properties) if char.properties else "нет"
                                desc = char.description or "Нет описания"
                                print(f"        {char.uuid} | Свойства: {props} | {desc}")
                        else:
                            print("      Характеристик нет")
                else:
                    print("  Сервисы не обнаружены (возможно, требуется pairing или устройство защищено)")
            else:
                print("Не удалось подключиться")
                
        except asyncio.TimeoutError:
            print("Таймаут подключения")
        except Exception as e:
            print(f"Ошибка: {e}")
        
        finally:
            if client.is_connected:
                await client.disconnect()
            print("-" * 80)

# Запуск
asyncio.run(main())
