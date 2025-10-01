from main import app

def quick_check():
    print("🔍 БЫСТРАЯ ПРОВЕРКА ЭНДПОИНТОВ")
    print("=" * 40)
    
    endpoints = {}
    for route in app.routes:
        methods = getattr(route, 'methods', None)
        path = getattr(route, 'path', None)
        if methods and path:
            endpoints[path] = methods
    
    required = [
        "/api/v1/health", "/api/v1/orders", "/api/v1/employees", 
        "/api/v1/mo", "/api/v1/operations", "/api/v1/defects", 
        "/api/v1/projects"
    ]
    
    for endpoint in required:
        if endpoint in endpoints:
            print(f"✅ GET {endpoint}")
        else:
            print(f"❌ GET {endpoint}")
    
    print(f"\nВсего эндпоинтов: {len(endpoints)}")

quick_check()
