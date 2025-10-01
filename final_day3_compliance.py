import requests
from main import app

def check_day3_compliance():
    print("🎯 ФИНАЛЬНАЯ ПРОВЕРКА СООТВЕТСТВИЯ ДЕНЬ 3")
    print("=" * 60)
    
    # Собираем все эндпоинты из приложения
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
    
    print("🔍 ПРОВЕРКА НАЛИЧИЯ ЭНДПОИНТОВ:")
    print("-" * 40)
    
    all_present = True
    total_required = 0
    total_present = 0
    
    for method, required_endpoints in day3_requirements.items():
        print(f"\n{method} методы:")
        for endpoint in required_endpoints:
            total_required += 1
            if endpoint in endpoints and method in endpoints[endpoint]:
                print(f"   ✅ {endpoint}")
                total_present += 1
            else:
                print(f"   ❌ {endpoint}")
                all_present = False
    
    compliance_percentage = (total_present / total_required) * 100
    
    print(f"\n📊 СТАТИСТИКА:")
    print(f"   Найдено: {total_present}/{total_required} эндпоинтов")
    print(f"   Соответствие: {compliance_percentage:.1f}%")
    
    if compliance_percentage == 100:
        print("🎉 100% СООТВЕТСТВИЕ ДЕНЬ 3 ДОСТИГНУТО!")
        print("✅ Все необходимые эндпоинты присутствуют")
        print("🚀 Система готова к использованию!")
    else:
        print(f"🔧 Требуется исправить {total_required - total_present} эндпоинтов")
    
    return compliance_percentage

if __name__ == "__main__":
    check_day3_compliance()
