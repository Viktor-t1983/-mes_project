import requests
from main import app

def verify_all_endpoints():
    print("✅ ПРОВЕРКА ВСЕХ ЭНДПОИНТОВ ПОСЛЕ ОБНОВЛЕНИЯ")
    print("=" * 60)
    
    endpoints_count = {}
    
    for route in app.routes:
        methods = getattr(route, 'methods', None)
        path = getattr(route, 'path', None)
        if methods and path:
            for method in methods:
                if method not in endpoints_count:
                    endpoints_count[method] = 0
                endpoints_count[method] += 1
                print(f"{method} {path}")
    
    print(f"\n📊 СТАТИСТИКА ЭНДПОИНТОВ:")
    for method, count in endpoints_count.items():
        print(f"   {method}: {count} эндпоинтов")
    
    total_endpoints = sum(endpoints_count.values())
    print(f"   ВСЕГО: {total_endpoints} эндпоинтов")
    
    # Проверяем наличие ключевых POST эндпоинтов
    key_post_endpoints = [
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
    
    print(f"\n🔍 ПРОВЕРКА КЛЮЧЕВЫХ POST ЭНДПОИНТОВ:")
    all_present = True
    for endpoint in key_post_endpoints:
        found = False
        for route in app.routes:
            methods = getattr(route, 'methods', None)
            path = getattr(route, 'path', None)
            if methods and path == endpoint and 'POST' in methods:
                print(f"✅ POST {endpoint}")
                found = True
                break
        if not found:
            print(f"❌ POST {endpoint}")
            all_present = False
    
    if all_present:
        print(f"\n🎉 ВСЕ КЛЮЧЕВЫЕ POST ЭНДПОИНТЫ ДОБАВЛЕНЫ!")
    else:
        print(f"\n⚠️  НЕКОТОРЫЕ POST ЭНДПОИНТЫ ОТСУТСТВУЮТ!")

if __name__ == "__main__":
    verify_all_endpoints()
