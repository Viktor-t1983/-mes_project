import requests
import json

BASE_URL = "http://localhost:8000"

def test_crud_operations():
    print("🧪 ТЕСТИРОВАНИЕ CRUD ОПЕРАЦИЙ")
    print("=" * 50)
    
    # 1. Создание сотрудника
    employee_data = {
        "name": "Иванов Иван Иванович",
        "position": "Оператор станка",
        "department": "Производство"
    }
    
    print("1. Создание сотрудника...")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/employees", json=employee_data)
        if response.status_code in [200, 201]:
            print("✅ Сотрудник создан")
            employee_id = response.json().get('id', 1)
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(f"Детали: {response.text}")
            employee_id = 1  # fallback для тестов
    except Exception as e:
        print(f"🚫 Ошибка создания сотрудника: {e}")
        employee_id = 1

    # 2. Создание заказа
    order_data = {
        "name": "Тестовый заказ 001",
        "description": "Заказ для тестирования системы",
        "status": "новый"
    }
    
    print("\n2. Создание заказа...")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/orders", json=order_data)
        if response.status_code in [200, 201]:
            print("✅ Заказ создан")
            order_id = response.json().get('id', 1)
        else:
            print(f"❌ Ошибка: {response.status_code}")
            order_id = 1
    except Exception as e:
        print(f"🚫 Ошибка создания заказа: {e}")
        order_id = 1

    # 3. Создание производственного задания (MO)
    mo_data = {
        "order_id": order_id,
        "name": "Производственное задание 001",
        "status": "активно"
    }
    
    print("\n3. Создание производственного задания...")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/mo", json=mo_data)
        if response.status_code in [200, 201]:
            print("✅ Производственное задание создано")
            mo_id = response.json().get('id', 1)
        else:
            print(f"❌ Ошибка: {response.status_code}")
            mo_id = 1
    except Exception as e:
        print(f"🚫 Ошибка создания MO: {e}")
        mo_id = 1

    # 4. Запуск операции
    operation_start_data = {
        "manufacturing_order_id": mo_id,
        "employee_id": employee_id,
        "operation_type": "основная операция"
    }
    
    print("\n4. Запуск операции...")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/operations/start", json=operation_start_data)
        if response.status_code in [200, 201]:
            print("✅ Операция запущена")
            operation_id = response.json().get('id', 1)
        else:
            print(f"❌ Ошибка: {response.status_code}")
            operation_id = 1
    except Exception as e:
        print(f"🚫 Ошибка запуска операции: {e}")
        operation_id = 1

    # 5. Пауза операции
    operation_pause_data = {
        "operation_id": operation_id,
        "reason": "технический перерыв"
    }
    
    print("\n5. Пауза операции...")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/operations/pause", json=operation_pause_data)
        if response.status_code in [200, 201]:
            print("✅ Операция поставлена на паузу")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"🚫 Ошибка паузы операции: {e}")

    # 6. Завершение операции
    operation_complete_data = {
        "operation_id": operation_id,
        "result": "успешно завершено"
    }
    
    print("\n6. Завершение операции...")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/operations/complete", json=operation_complete_data)
        if response.status_code in [200, 201]:
            print("✅ Операция завершена")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"🚫 Ошибка завершения операции: {e}")

    # 7. Создание отклонения
    defect_data = {
        "manufacturing_order_id": mo_id,
        "operation_id": operation_id,
        "defect_type": "брак материала",
        "description": "обнаружен дефект поверхности",
        "severity": "средний"
    }
    
    print("\n7. Создание отклонения...")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/defects", json=defect_data)
        if response.status_code in [200, 201]:
            print("✅ Отклонение создано")
        else:
            print(f"❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"🚫 Ошибка создания отклонения: {e}")

    # 8. Проверка QR кодов
    print("\n8. Проверка генерации QR кодов...")
    qr_endpoints = [
        f"/api/v1/qr/order/{order_id}",
        f"/api/v1/qr/employee/{employee_id}", 
        f"/api/v1/qr/mo/{mo_id}"
    ]
    
    for endpoint in qr_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint} - работает")
            else:
                print(f"❌ {endpoint} - ошибка {response.status_code}")
        except Exception as e:
            print(f"🚫 {endpoint} - ошибка: {e}")

    print("\n🎯 ИТОГ ТЕСТИРОВАНИЯ CRUD:")
    print("Если большинство операций завершились успешно - система соответствует День 3")

if __name__ == "__main__":
    test_crud_operations()
