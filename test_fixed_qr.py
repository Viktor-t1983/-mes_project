import requests
import time

BASE_URL = "http://localhost:8000"

def test_fixed_qr_endpoints():
    print("🧪 ТЕСТИРОВАНИЕ ИСПРАВЛЕННЫХ QR-КОДОВ")
    print("=" * 50)
    
    # Сначала создаем тестовые данные если нужно
    print("1. 📝 ПОДГОТОВКА ТЕСТОВЫХ ДАННЫХ:")
    
    # Создаем сотрудника для теста
    try:
        employee_response = requests.post(f"{BASE_URL}/api/v1/employees", params={
            "first_name": "Тест",
            "last_name": "QR-Сотрудник", 
            "role": "Тестировщик"
        })
        
        if employee_response.status_code == 200:
            employee_id = employee_response.json()['id']
            print(f"   ✅ Создан сотрудник для теста: ID {employee_id}")
        else:
            # Используем существующего сотрудника
            employees_response = requests.get(f"{BASE_URL}/api/v1/employees")
            if employees_response.status_code == 200:
                employees = employees_response.json()
                if employees:
                    employee_id = employees[0]['id']
                    print(f"   ✅ Используем существующего сотрудника: ID {employee_id}")
                else:
                    print("   ❌ Нет сотрудников для теста")
                    return
    except Exception as e:
        print(f"   💥 Ошибка подготовки сотрудника: {e}")
        return
    
    # Создаем MO для теста
    try:
        mo_response = requests.post(f"{BASE_URL}/api/v1/mo", params={
            "order_number": "QR-TEST-001",
            "product_name": "Тест QR MO",
            "product_code": "QR-TEST",
            "quantity": 1
        })
        
        if mo_response.status_code == 200:
            mo_id = mo_response.json()['id']
            print(f"   ✅ Создано MO для теста: ID {mo_id}")
        else:
            # Используем существующее MO
            mo_list_response = requests.get(f"{BASE_URL}/api/v1/mo")
            if mo_list_response.status_code == 200:
                mo_list = mo_list_response.json()
                if mo_list:
                    mo_id = mo_list[0]['id']
                    print(f"   ✅ Используем существующее MO: ID {mo_id}")
                else:
                    print("   ❌ Нет MO для теста")
                    return
    except Exception as e:
        print(f"   💥 Ошибка подготовки MO: {e}")
        return
    
    # 2. Тестируем исправленные QR-коды
    print("\n2. 📱 ТЕСТ ИСПРАВЛЕННЫХ QR-КОДОВ:")
    
    test_cases = [
        ('order', 1, "Заказ"),
        ('employee', employee_id, "Сотрудник"),
        ('mo', mo_id, "Производственное задание")
    ]
    
    all_success = True
    
    for entity, entity_id, description in test_cases:
        try:
            response = requests.get(f"{BASE_URL}/api/v1/qr/{entity}/{entity_id}")
            print(f"   QR {description} (ID {entity_id}): {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"      ✅ Успех: {data['qr_data']}")
                print(f"      📋 Данные: {data['entity_name']}")
            else:
                print(f"      ❌ Ошибка: {response.text}")
                all_success = False
                
        except Exception as e:
            print(f"   💥 Ошибка QR {description}: {e}")
            all_success = False
    
    print("\n" + "=" * 50)
    if all_success:
        print("🎉 ВСЕ QR-КОДЫ РАБОТАЮТ КОРРЕКТНО!")
    else:
        print("⚠️  Некоторые QR-коды требуют доработки")

if __name__ == "__main__":
    test_fixed_qr_endpoints()
