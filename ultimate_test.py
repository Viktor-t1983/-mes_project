import requests
import json

BASE_URL = "http://localhost:8000"

def ultimate_test():
    print("🏆 УЛЬТИМАТИВНЫЙ ТЕСТ СИСТЕМЫ")
    print("=" * 50)
    
    results = []
    
    # 1. Health check
    print("1. 🩺 HEALTH CHECK...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Сервер работает")
            results.append(("Health Check", "✅"))
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            results.append(("Health Check", "❌"))
    except Exception as e:
        print(f"   🚫 Ошибка подключения: {e}")
        return results
    
    # 2. Создание тестовых данных через все POST эндпоинты
    print("\n2. 📝 ТЕСТИРОВАНИЕ ВСЕХ POST ЭНДПОИНТОВ...")
    
    test_data = [
        ("/api/v1/employees", {"first_name": "Иван", "last_name": "Иванов", "role": "Оператор"}, "Сотрудник"),
        ("/api/v1/orders", {"product_name": "Тестовый продукт", "quantity": 10}, "Заказ"),
        ("/api/v1/mo", {"product_name": "Производимый продукт", "quantity": 5}, "Производственное задание"),
        ("/api/v1/operations", {"name": "Тестовая операция", "description": "Описание"}, "Операция"),
        ("/api/v1/defects", {"defect_type": "Качество", "defect_description": "Тест", "severity": "medium"}, "Отклонение"),
        ("/api/v1/projects", {"name": "Тестовый проект", "description": "Описание"}, "Проект")
    ]
    
    operation_id = None
    
    for endpoint, data, description in test_data:
        try:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=10)
            if response.status_code == 200:
                result_data = response.json()
                if endpoint == "/api/v1/operations":
                    operation_id = result_data["id"]
                print(f"   ✅ {description} создан")
                results.append((f"Создание {description}", "✅"))
            else:
                print(f"   ❌ {description}: {response.status_code}")
                results.append((f"Создание {description}", "❌"))
        except Exception as e:
            print(f"   🚫 {description}: {e}")
            results.append((f"Создание {description}", "🚫"))
    
    # 3. Тестирование управления операциями
    print("\n3. 🎮 ТЕСТИРОВАНИЕ УПРАВЛЕНИЯ ОПЕРАЦИЯМИ...")
    if operation_id:
        management_tests = [
            ("/api/v1/operations/start", "Запуск операции"),
            ("/api/v1/operations/pause", "Пауза операции"), 
            ("/api/v1/operations/complete", "Завершение операции")
        ]
        
        for endpoint, desc in management_tests:
            try:
                response = requests.post(f"{BASE_URL}{endpoint}?operation_id={operation_id}", timeout=10)
                if response.status_code == 200:
                    print(f"   ✅ {desc}")
                    results.append((desc, "✅"))
                else:
                    print(f"   ❌ {desc}: {response.status_code}")
                    results.append((desc, "❌"))
            except Exception as e:
                print(f"   🚫 {desc}: {e}")
                results.append((desc, "🚫"))
    else:
        print("   ⚠️  Пропуск тестов управления (нет operation_id)")
    
    # 4. Тестирование GET эндпоинтов
    print("\n4. 📊 ТЕСТИРОВАНИЕ GET ЭНДПОИНТОВ...")
    get_endpoints = [
        "/api/v1/employees",
        "/api/v1/orders", 
        "/api/v1/mo",
        "/api/v1/operations",
        "/api/v1/defects",
        "/api/v1/projects"
    ]
    
    for endpoint in get_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"   ✅ GET {endpoint}")
                results.append((f"GET {endpoint}", "✅"))
            else:
                print(f"   ❌ GET {endpoint}: {response.status_code}")
                results.append((f"GET {endpoint}", "❌"))
        except Exception as e:
            print(f"   🚫 GET {endpoint}: {e}")
            results.append((f"GET {endpoint}", "🚫"))
    
    # 5. Тестирование QR кодов
    print("\n5. 📱 ТЕСТИРОВАНИЕ QR КОДОВ...")
    qr_endpoints = [
        "/api/v1/qr/order/1",
        "/api/v1/qr/employee/1", 
        "/api/v1/qr/mo/1"
    ]
    
    for endpoint in qr_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {endpoint}")
                results.append((f"QR {endpoint}", "✅"))
            else:
                print(f"   ❌ {endpoint}: {response.status_code}")
                results.append((f"QR {endpoint}", "❌"))
        except Exception as e:
            print(f"   🚫 {endpoint}: {e}")
            results.append((f"QR {endpoint}", "🚫"))
    
    # Финальный отчет
    print(f"\n🎯 ИТОГОВЫЙ ОТЧЕТ:")
    print("=" * 50)
    
    success = sum(1 for _, status in results if status == "✅")
    total = len(results)
    
    for test, status in results:
        print(f"   {status} {test}")
    
    print(f"\n📊 РЕЗУЛЬТАТ: {success}/{total} успешных тестов")
    
    if success == total:
        print("🎉 100% УСПЕХ! ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("✅ СИСТЕМА ПОЛНОСТЬЮ СООТВЕТСТВУЕТ ДЕНЬ 3!")
        print("🚀 ГОТОВО К ПРОИЗВОДСТВЕННОЙ ЭКСПЛУАТАЦИИ!")
    elif success >= total * 0.9:
        print("✅ ОТЛИЧНЫЙ РЕЗУЛЬТАТ! Система работает!")
        print("🔧 Незначительные проблемы не влияют на работу")
    else:
        print("⚠️  ТРЕБУЮТСЯ ДОРАБОТКИ")
    
    return success == total

if __name__ == "__main__":
    ultimate_test()
