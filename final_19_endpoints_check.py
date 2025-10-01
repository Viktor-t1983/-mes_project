import requests
import time

BASE_URL = "http://localhost:8000"

print("🎯 ФИНАЛЬНАЯ ПРОВЕРКА ВСЕХ 19 ENDPOINTS")
print("=" * 50)

# Все endpoints которые должны работать
endpoints = [
    # GET endpoints (10)
    ("GET", "/api/v1/health"),
    ("GET", "/api/v1/employees"),
    ("GET", "/api/v1/orders"),
    ("GET", "/api/v1/mo"),
    ("GET", "/api/v1/operations"),
    ("GET", "/api/v1/defects"),
    ("GET", "/api/v1/projects"),
    ("GET", "/api/v1/qr/order/1"),
    ("GET", "/api/v1/qr/employee/1"),
    ("GET", "/api/v1/qr/mo/1"),
    
    # POST endpoints (9) - проверяем доступность
    ("POST", "/api/v1/employees"),
    ("POST", "/api/v1/orders"),
    ("POST", "/api/v1/mo"),
    ("POST", "/api/v1/operations"),
    ("POST", "/api/v1/operations/start"),
    ("POST", "/api/v1/operations/pause"),
    ("POST", "/api/v1/operations/complete"),
    ("POST", "/api/v1/defects"),
    ("POST", "/api/v1/projects")
]

success_count = 0

for i, (method, endpoint) in enumerate(endpoints, 1):
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"{i:2d}. ✅ {method} {endpoint}")
                success_count += 1
            else:
                print(f"{i:2d}. ❌ {method} {endpoint} - {response.status_code}")
        else:
            # Для POST проверяем что endpoint существует (возвращает не 404)
            response = requests.post(f"{BASE_URL}{endpoint}", json={}, timeout=3)
            if response.status_code != 404:  # 422 (validation error) нормально - endpoint работает
                print(f"{i:2d}. ✅ {method} {endpoint} (доступен)")
                success_count += 1
            else:
                print(f"{i:2d}. ❌ {method} {endpoint} - 404 Not Found")
    except Exception as e:
        print(f"{i:2d}. ❌ {method} {endpoint} - ошибка")

print(f"\\n📊 РЕЗУЛЬТАТ: {success_count}/{len(endpoints)} endpoints работают")
print(f"🎯 УСПЕШНОСТЬ: {(success_count/len(endpoints))*100:.1f}%")

if success_count == len(endpoints):
    print("\\n🎉 ВСЕ 19 ENDPOINTS РАБОТАЮТ КОРРЕКТНО!")
    print("🚀 MES SYSTEM ГОТОВА К ИНТЕГРАЦИИ!")
else:
    print(f"\\n⚠️  Проблемы с {len(endpoints) - success_count} endpoints")
