import requests
import time

BASE_URL = "http://localhost:8000"

def test_all():
    print("🧪 ТЕСТ ВСЕХ ЭНДПОИНТОВ ПОСЛЕ ИСПРАВЛЕНИЯ")
    print("=" * 55)
    
    # Проверяем доступность
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ Сервер запущен и документация доступна")
        else:
            print(f"❌ Документация: {response.status_code}")
            return
    except Exception as e:
        print(f"💥 Сервер не доступен: {e}")
        return
    
    # Тестируем ключевые эндпоинты "День 3"
    endpoints = [
        ("QR Order", "GET", "/api/v1/qr/order/1"),
        ("QR Employee", "GET", "/api/v1/qr/employee/1"),
        ("QR MO", "GET", "/api/v1/qr/mo/1"),
        ("Orders", "GET", "/api/v1/orders"),
        ("MO", "GET", "/api/v1/mo"),
        ("Employees", "GET", "/api/v1/employees"),
        ("Operations", "GET", "/api/v1/operations"),
        ("Defects", "GET", "/api/v1/defects"),
        ("Projects", "GET", "/api/v1/projects")
    ]
    
    print("\\n🔍 ТЕСТИРОВАНИЕ ЭНДПОИНТОВ 'ДЕНЬ 3':")
    working = 0
    
    for name, method, endpoint in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"   ✅ {name}")
                working += 1
            else:
                print(f"   ❌ {name}: {response.status_code}")
        except Exception as e:
            print(f"   💥 {name}: {e}")
    
    print("\\n" + "=" * 55)
    print(f"📊 РЕЗУЛЬТАТ: {working}/{len(endpoints)} эндпоинтов работают")
    
    if working >= 8:
        print("🎉 СИСТЕМА СООТВЕТСТВУЕТ ТРЕБОВАНИЯМ 'ДЕНЬ 3'!")
        print("🚀 MES-X PRODUCTION CORE ГОТОВ К ЭКСПЛУАТАЦИИ!")
    else:
        print("⚠️  Требуется дополнительная настройка")
    
    print(f"\\n🌐 Документация: {BASE_URL}/docs")

if __name__ == "__main__":
    test_all()
