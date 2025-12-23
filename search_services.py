import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_ADDRESS='C2:F1:F7:0F:25:F5'

async def main():
        
    client = BleakClient(DEVICE_ADDRESS)
    try:
        print("  Подключение...", end=" ")
        await client.connect(timeout=15.0)  # Таймаут подключения
        if client.is_connected:
            print("Успешно!")
            
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
