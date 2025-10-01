import requests
import time

BASE_URL = "http://localhost:8000"

def test_missing_endpoints():
    print("🧪 ТЕСТИРОВАНИЕ ДОБАВЛЕННЫХ ЭНДПОИНТОВ")
    print("=" * 50)
    
    # 1. Тестируем генерацию QR-кодов
    print("\n1. 📱 ТЕСТ ГЕНЕРАЦИИ QR-КОДОВ:")
    test_entities = ['order', 'employee', 'mo']
    
    for entity in test_entities:
        try:
            # Берем существующий ID для теста
            test_id = 1
            
            response = requests.get(f"{BASE_URL}/api/v1/qr/{entity}/{test_id}")
            print(f"   QR {entity}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"      ✅ Успех: {data['qr_data']}")
            else:
                print(f"      ❌ Ошибка: {response.text}")
        except Exception as e:
            print(f"   💥 Ошибка QR {entity}: {e}")
    
    # 2. Тестируем паузу операций
    print("\n2. ⏸️ ТЕСТ ПАУЗЫ ОПЕРАЦИЙ:")
    
    try:
        # Сначала создаем тестовую операцию и запускаем ее
        # Создаем MO для теста
        mo_response = requests.post(f"{BASE_URL}/api/v1/mo", params={
            "order_number": "PAUSE-TEST-001",
            "product_name": "Тест паузы операций",
            "product_code": "PAUSE-TEST",
            "quantity": 5
        })
        
        if mo_response.status_code == 200:
            mo_id = mo_response.json()['id']
            print(f"   ✅ Создано MO: {mo_id}")
            
            # Создаем операцию
            op_response = requests.post(f"{BASE_URL}/api/v1/operations", params={
                "manufacturing_order_id": mo_id,
                "operation_number": "OP-PAUSE-TEST",
                "name": "Тестовая операция для паузы",
                "description": "Операция для тестирования функции паузы"
            })
            
            if op_response.status_code == 200:
                op_id = op_response.json()['id']
                print(f"   ✅ Создана операция: {op_id}")
                
                # Запускаем операцию
                start_response = requests.post(f"{BASE_URL}/api/v1/operations/start", params={
                    "operation_id": op_id,
                    "employee_id": 1  # Используем существующего сотрудника
                })
                
                if start_response.status_code == 200:
                    print(f"   ✅ Операция запущена")
                    
                    # Тестируем паузу
                    pause_response = requests.post(f"{BASE_URL}/api/v1/operations/pause", params={
                        "operation_id": op_id
                    })
                    
                    print(f"   ⏸️ Пауза операции: {pause_response.status_code}")
                    if pause_response.status_code == 200:
                        print(f"      ✅ Успех: {pause_response.json()}")
                    else:
                        print(f"      ❌ Ошибка: {pause_response.text}")
                else:
                    print(f"   ❌ Не удалось запустить операцию: {start_response.text}")
            else:
                print(f"   ❌ Не удалось создать операцию: {op_response.text}")
        else:
            print(f"   ❌ Не удалось создать MO: {mo_response.text}")
            
    except Exception as e:
        print(f"   💥 Ошибка теста паузы: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")

if __name__ == "__main__":
    test_missing_endpoints()
