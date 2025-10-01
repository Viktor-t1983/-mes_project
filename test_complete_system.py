import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_complete_system():
    print("🧪 ПОЛНОЕ ТЕСТИРОВАНИЕ СИСТЕМЫ")
    print("=" * 50)
    
    test_results = []
    
    # 1. Тест создания сотрудника
    print("1. 📝 СОЗДАНИЕ СОТРУДНИКА...")
    employee_data = {
        "first_name": "Иван",
        "last_name": "Иванов",
        "role": "Оператор"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/employees", json=employee_data)
        if response.status_code == 200:
            employee_id = response.json()["id"]
            print(f"   ✅ Успешно создан (ID: {employee_id})")
            test_results.append(("Создание сотрудника", "✅"))
        else:
            print(f"   ❌ Ошибка: {response.status_code} - {response.text}")
            test_results.append(("Создание сотрудника", "❌"))
    except Exception as e:
        print(f"   🚫 Ошибка подключения: {e}")
        test_results.append(("Создание сотрудника", "🚫"))
    
    # 2. Тест создания заказа
    print("\n2. 📦 СОЗДАНИЕ ЗАКАЗА...")
    order_data = {
        "product_name": "Тестовый продукт",
        "quantity": 10
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/orders", json=order_data)
        if response.status_code == 200:
            order_id = response.json()["id"]
            print(f"   ✅ Успешно создан (ID: {order_id})")
            test_results.append(("Создание заказа", "✅"))
        else:
            print(f"   ❌ Ошибка: {response.status_code} - {response.text}")
            test_results.append(("Создание заказа", "❌"))
    except Exception as e:
        print(f"   🚫 Ошибка подключения: {e}")
        test_results.append(("Создание заказа", "🚫"))
    
    # 3. Тест создания производственного задания
    print("\n3. 🏭 СОЗДАНИЕ ПРОИЗВОДСТВЕННОГО ЗАДАНИЯ...")
    mo_data = {
        "product_name": "Производимый продукт", 
        "quantity": 5
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/mo", json=mo_data)
        if response.status_code == 200:
            mo_id = response.json()["id"]
            print(f"   ✅ Успешно создано (ID: {mo_id})")
            test_results.append(("Создание МО", "✅"))
        else:
            print(f"   ❌ Ошибка: {response.status_code} - {response.text}")
            test_results.append(("Создание МО", "❌"))
    except Exception as e:
        print(f"   🚫 Ошибка подключения: {e}")
        test_results.append(("Создание МО", "🚫"))
    
    # 4. Тест создания операции
    print("\n4. ⚙️ СОЗДАНИЕ ОПЕРАЦИИ...")
    operation_data = {
        "name": "Тестовая операция",
        "description": "Описание тестовой операции"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/operations", json=operation_data)
        if response.status_code == 200:
            operation_id = response.json()["id"]
            print(f"   ✅ Успешно создана (ID: {operation_id})")
            test_results.append(("Создание операции", "✅"))
        else:
            print(f"   ❌ Ошибка: {response.status_code} - {response.text}")
            test_results.append(("Создание операции", "❌"))
            operation_id = 1
    except Exception as e:
        print(f"   🚫 Ошибка подключения: {e}")
        test_results.append(("Создание операции", "🚫"))
        operation_id = 1
    
    # 5. Тест управления операциями
    print("\n5. 🎮 УПРАВЛЕНИЕ ОПЕРАЦИЯМИ...")
    management_endpoints = [
        ("/api/v1/operations/start", "Запуск операции"),
        ("/api/v1/operations/pause", "Пауза операции"),
        ("/api/v1/operations/complete", "Завершение операции")
    ]
    
    for endpoint, description in management_endpoints:
        try:
            response = requests.post(f"{BASE_URL}{endpoint}?operation_id={operation_id}")
            if response.status_code == 200:
                print(f"   ✅ {description} - Успешно")
                test_results.append((description, "✅"))
            else:
                print(f"   ❌ {description} - Ошибка: {response.status_code}")
                test_results.append((description, "❌"))
        except Exception as e:
            print(f"   🚫 {description} - Ошибка подключения: {e}")
            test_results.append((description, "🚫"))
    
    # 6. Тест создания отклонения
    print("\n6. ⚠️ СОЗДАНИЕ ОТКЛОНЕНИЯ...")
    defect_data = {
        "defect_type": "Качество",
        "defect_description": "Тестовое отклонение качества",
        "severity": "medium"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/defects", json=defect_data)
        if response.status_code == 200:
            print(f"   ✅ Успешно создано")
            test_results.append(("Создание отклонения", "✅"))
        else:
            print(f"   ❌ Ошибка: {response.status_code} - {response.text}")
            test_results.append(("Создание отклонения", "❌"))
    except Exception as e:
        print(f"   🚫 Ошибка подключения: {e}")
        test_results.append(("Создание отклонения", "🚫"))
    
    # 7. Тест создания проекта
    print("\n7. 📋 СОЗДАНИЕ ПРОЕКТА...")
    project_data = {
        "name": "Тестовый проект",
        "description": "Описание тестового проекта"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/v1/projects", json=project_data)
        if response.status_code == 200:
            print(f"   ✅ Успешно создан")
            test_results.append(("Создание проекта", "✅"))
        else:
            print(f"   ❌ Ошибка: {response.status_code} - {response.text}")
            test_results.append(("Создание проекта", "❌"))
    except Exception as e:
        print(f"   🚫 Ошибка подключения: {e}")
        test_results.append(("Создание проекта", "🚫"))
    
    # 8. Тест QR кодов
    print("\n8. 📱 ТЕСТ QR КОДОВ...")
    qr_endpoints = [
        ("/api/v1/qr/order/1", "QR заказа"),
        ("/api/v1/qr/employee/1", "QR сотрудника"),
        ("/api/v1/qr/mo/1", "QR МО")
    ]
    
    for endpoint, description in qr_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                print(f"   ✅ {description} - Работает")
                test_results.append((description, "✅"))
            else:
                print(f"   ❌ {description} - Ошибка: {response.status_code}")
                test_results.append((description, "❌"))
        except Exception as e:
            print(f"   🚫 {description} - Ошибка подключения: {e}")
            test_results.append((description, "🚫"))
    
    # Итоговый отчет
    print(f"\n🎯 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ:")
    print("=" * 40)
    
    success_count = sum(1 for _, status in test_results if status == "✅")
    total_count = len(test_results)
    
    for test_name, status in test_results:
        print(f"   {status} {test_name}")
    
    print(f"\n📊 РЕЗУЛЬТАТ: {success_count}/{total_count} успешных тестов")
    
    if success_count == total_count:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("✅ Система полностью соответствует День 3!")
    else:
        print("⚠️  Есть проблемы, требующие исправления")

if __name__ == "__main__":
    test_complete_system()
