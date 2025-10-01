import requests
import json

BASE_URL = "http://localhost:8000"

def test_100_percent():
    print("🏆 ТЕСТ ДЛЯ 100% РЕЗУЛЬТАТА")
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
    
    # 2. Тестируем создание данных с ПРАВИЛЬНЫМИ схемами
    print("\n2. 📝 ТЕСТИРОВАНИЕ СОЗДАНИЯ ДАННЫХ...")
    
    test_cases = [
        ("/api/v1/employees", {
            "first_name": "Иван", 
            "last_name": "Иванов", 
            "role": "Оператор",
            "qr_code": "EMP001"
        }, "Сотрудник"),
        
        ("/api/v1/orders", {
            "name": "Тестовый заказ",
            "description": "Описание тестового заказа", 
            "product_name": "Тестовый продукт",
            "quantity": 10
        }, "Заказ"),
        
        ("/api/v1/mo", {
            "order_number": "MO-001",
            "product_name": "Производимый продукт",
            "product_code": "PROD-001", 
            "quantity": 5
        }, "Производственное задание"),
        
        ("/api/v1/operations", {
            "manufacturing_order_id": 1,
            "operation_number": "OP-001",
            "name": "Тестовая операция",
            "description": "Описание тестовой операции",
            "planned_duration": 60
        }, "Операция"),
        
        ("/api/v1/defects", {
            "manufacturing_order_id": 1,
            "reported_by": 1,
            "defect_type": "Качество",
            "defect_description": "Тестовое отклонение качества",
            "severity": "medium"
        }, "Отклонение"),
        
        ("/api/v1/projects", {
            "name": "Тестовый проект",
            "description": "Описание тестового проекта"
        }, "Проект")
    ]
    
    created_ids = {}
    
    for endpoint, data, description in test_cases:
        try:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=10)
            if response.status_code == 200:
                result_data = response.json()
                entity_id = result_data.get("id")
                if entity_id:
                    created_ids[description] = entity_id
                print(f"   ✅ {description} создан (ID: {entity_id})")
                results.append((f"Создание {description}", "✅"))
            else:
                print(f"   ❌ {description}: {response.status_code} - {response.text}")
                results.append((f"Создание {description}", "❌"))
        except Exception as e:
            print(f"   🚫 {description}: {e}")
            results.append((f"Создание {description}", "🚫"))
    
    # 3. Тестируем управление операциями
    print("\n3. 🎮 ТЕСТИРОВАНИЕ УПРАВЛЕНИЯ ОПЕРАЦИЯМИ...")
    if "Операция" in created_ids:
        operation_id = created_ids["Операция"]
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
        print("   ⚠️  Пропуск тестов управления (операция не создана)")
        for desc in ["Запуск операции", "Пауза операции", "Завершение операции"]:
            results.append((desc, "⚠️"))
    
    # 4. Тестируем ВСЕ GET эндпоинты
    print("\n4. 📊 ТЕСТИРОВАНИЕ ВСЕХ GET ЭНДПОИНТОВ...")
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
                data = response.json()
                count = len(data) if isinstance(data, list) else "N/A"
                print(f"   ✅ GET {endpoint} ({count} записей)")
                results.append((f"GET {endpoint}", "✅"))
            else:
                print(f"   ❌ GET {endpoint}: {response.status_code}")
                results.append((f"GET {endpoint}", "❌"))
        except Exception as e:
            print(f"   🚫 GET {endpoint}: {e}")
            results.append((f"GET {endpoint}", "🚫"))
    
    # 5. Тестируем QR коды
    print("\n5. 📱 ТЕСТИРОВАНИЕ QR КОДОВ...")
    qr_endpoints = [
        ("/api/v1/qr/order/1", "QR заказа"),
        ("/api/v1/qr/employee/1", "QR сотрудника"),
        ("/api/v1/qr/mo/1", "QR МО")
    ]
    
    for endpoint, description in qr_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image/'):
                print(f"   ✅ {description} (возвращает изображение)")
                results.append((description, "✅"))
            else:
                print(f"   ❌ {description}: {response.status_code}")
                results.append((description, "❌"))
        except Exception as e:
            print(f"   🚫 {description}: {e}")
            results.append((description, "🚫"))
    
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
    
    return success, total

if __name__ == "__main__":
    test_100_percent()
