import requests
import time
import sys

def wait_for_server():
    print("⏳ Ожидание перезапуска сервера...")
    for i in range(10):
        try:
            response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
            if response.status_code == 200:
                print("✅ Сервер перезапущен!")
                return True
        except:
            print(f"⏳ {i+1}/10...")
            time.sleep(2)
    return False

def test_critical_endpoints():
    base_url = "http://localhost:8000/api/v1"
    
    print("\n🧪 ТЕСТИРОВАНИЕ КРИТИЧЕСКИХ ЭНДПОИНТОВ")
    print("=" * 45)
    
    endpoints = [
        ("Health", "/health"),
        ("Orders", "/orders"),
        ("Employees", "/employees"),
        ("Manufacturing Orders", "/mo"),
        ("Operations", "/operations"),
        ("Projects", "/projects")
    ]
    
    results = []
    for name, endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {name}: {response.status_code}")
            results.append(response.status_code == 200)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"   📊 Записей: {len(data)}")
        except Exception as e:
            print(f"❌ {name}: Ошибка - {e}")
            results.append(False)
    
    working = sum(results)
    total = len(results)
    
    print(f"\n📊 РЕЗУЛЬТАТ: {working}/{total} эндпоинтов работают")
    
    if working >= 5:
        print("🎉 ОСНОВНЫЕ ЭНДПОИНТЫ РАБОТАЮТ!")
        print("✅ Ошибки отношений исправлены")
    else:
        print("⚠️  Требуются дополнительные исправления")

if __name__ == "__main__":
    if wait_for_server():
        test_critical_endpoints()
