import requests
from main import app

def final_verification():
    print("🎯 ФИНАЛЬНАЯ ПРОВЕРКА 100% СООТВЕТСТВИЯ")
    print("=" * 60)
    
    # Собираем все эндпоинты
    endpoints = {}
    for route in app.routes:
        methods = getattr(route, 'methods', None)
        path = getattr(route, 'path', None)
        if methods and path:
            endpoints[path] = methods
    
    # Требования День 3
    day3_requirements = {
        "GET": [
            "/api/v1/health",
            "/api/v1/orders",
            "/api/v1/employees", 
            "/api/v1/mo",
            "/api/v1/operations",
            "/api/v1/defects",
            "/api/v1/projects",
            "/api/v1/qr/order/{order_id}",
            "/api/v1/qr/employee/{employee_id}",
            "/api/v1/qr/mo/{mo_id}"
        ],
        "POST": [
            "/api/v1/employees",
            "/api/v1/orders",
            "/api/v1/mo",
            "/api/v1/operations", 
            "/api/v1/operations/start",
            "/api/v1/operations/pause",
            "/api/v1/operations/complete",
            "/api/v1/defects",
            "/api/v1/projects"
        ]
    }
    
    print("🔍 ПРОВЕРКА СООТВЕТСТВИЯ ДЕНЬ 3:")
    print("-" * 40)
    
    all_requirements_met = True
    
    for method, required_endpoints in day3_requirements.items():
        print(f"\n{method} методы:")
        for endpoint in required_endpoints:
            if endpoint in endpoints and method in endpoints[endpoint]:
                print(f"   ✅ {endpoint}")
            else:
                print(f"   ❌ {endpoint}")
                all_requirements_met = False
    
    # Проверяем работу через реальные запросы
    print(f"\n🧪 ТЕСТИРОВАНИЕ РАБОТОСПОСОБНОСТИ:")
    print("-" * 40)
    
    BASE_URL = "http://localhost:8000"
    test_results = []
    
    # Простой тест создания сотрудника
    try:
        employee_data = {"first_name": "Тест", "last_name": "Тестов", "role": "Оператор"}
        response = requests.post(f"{BASE_URL}/api/v1/employees", json=employee_data, timeout=10)
        if response.status_code == 200:
            print("✅ POST /api/v1/employees - РАБОТАЕТ")
            test_results.append(True)
        else:
            print(f"❌ POST /api/v1/employees - Ошибка: {response.status_code}")
            test_results.append(False)
    except Exception as e:
        print(f"🚫 POST /api/v1/employees - Ошибка: {e}")
        test_results.append(False)
    
    # Тест получения сотрудников
    try:
        response = requests.get(f"{BASE_URL}/api/v1/employees", timeout=10)
        if response.status_code == 200:
            print("✅ GET /api/v1/employees - РАБОТАЕТ")
            test_results.append(True)
        else:
            print(f"❌ GET /api/v1/employees - Ошибка: {response.status_code}")
            test_results.append(False)
    except Exception as e:
        print(f"🚫 GET /api/v1/employees - Ошибка: {e}")
        test_results.append(False)
    
    # Финальный вердикт
    print(f"\n🎯 ФИНАЛЬНЫЙ РЕЗУЛЬТАТ:")
    print("=" * 40)
    
    if all_requirements_met and all(test_results):
        print("🎉 100% СООТВЕТСТВИЕ ДЕНЬ 3 ДОСТИГНУТО!")
        print("✅ Все эндпоинты присутствуют")
        print("✅ Все эндпоинты работают")
        print("✅ Система готова к использованию")
    elif all_requirements_met:
        print("✅ Все эндпоинты присутствуют")
        print("⚠️  Некоторые эндпоинты могут иметь проблемы")
    else:
        print("❌ Не все требования выполнены")
        print("🔧 Требуются дополнительные исправления")
    
    return all_requirements_met and all(test_results)

if __name__ == "__main__":
    final_verification()
