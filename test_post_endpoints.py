import requests
import json

BASE_URL = "http://localhost:8000"

def test_post_endpoints():
    print("🧪 ТЕСТИРОВАНИЕ POST ЭНДПОИНТОВ")
    print("=" * 50)
    
    # Тестируем создание сотрудника
    print("1. Создание сотрудника...")
    employee_data = {
        "first_name": "Иван",
        "last_name": "Иванов",
        "role": "Оператор"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/employees", json=employee_data)
        print(f"   Статус: {response.status_code}")
        if response.status_code in [200, 201]:
            print("   ✅ Успешно создан")
        elif response.status_code == 422:
            print("   ⚠️  Ошибка валидации (возможно неправильные параметры)")
            print(f"   Детали: {response.json()}")
        else:
            print(f"   ❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"   🚫 Ошибка подключения: {e}")
    
    # Тестируем создание заказа
    print("\n2. Создание заказа...")
    order_data = {
        "product_name": "Тестовый продукт",
        "quantity": 10
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/orders", json=order_data)
        print(f"   Статус: {response.status_code}")
        if response.status_code in [200, 201]:
            print("   ✅ Успешно создан")
        elif response.status_code == 422:
            print("   ⚠️  Ошибка валидации")
        else:
            print(f"   ❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"   🚫 Ошибка подключения: {e}")
    
    # Тестируем операции
    print("\n3. Проверка эндпоинтов операций...")
    operations_endpoints = [
        ("/api/v1/operations/start", "Запуск операции"),
        ("/api/v1/operations/pause", "Пауза операции"), 
        ("/api/v1/operations/complete", "Завершение операции")
    ]
    
    for endpoint, description in operations_endpoints:
        try:
            response = requests.post(f"{BASE_URL}{endpoint}", json={"operation_id": 1})
            print(f"   {description}: {response.status_code}")
            if response.status_code in [200, 201, 422]:
                print("   ✅ Эндпоинт доступен")
            else:
                print(f"   ❌ Проблема: {response.status_code}")
        except Exception as e:
            print(f"   🚫 Ошибка: {e}")

if __name__ == "__main__":
    test_post_endpoints()
