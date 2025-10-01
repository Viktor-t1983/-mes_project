import requests
import time

def quick_test():
    print("🧪 БЫСТРЫЙ ТЕСТ ОСНОВНЫХ ЭНДПОИНТОВ")
    print("=" * 40)
    
    # Ждем запуска сервера
    time.sleep(5)
    
    endpoints = [
        ("Health", "/api/v1/health"),
        ("Orders", "/api/v1/orders"),
        ("Employees", "/api/v1/employees"),
        ("Projects", "/api/v1/projects")
    ]
    
    for name, endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {name}: {response.status_code}")
        except:
            print(f"❌ {name}: Сервер не отвечает")
    
    print("\\n📖 Документация: http://localhost:8000/docs")

quick_test()
