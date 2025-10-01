import requests
import time

BASE_URL = "http://localhost:8000"

def smoke_test():
    print("🚀 БЫСТРЫЙ ТЕСТ РАБОТОСПОСОБНОСТИ")
    print("=" * 50)
    
    # Проверяем доступность сервера
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ Сервер запущен и отвечает")
        else:
            print(f"❌ Сервер отвечает с ошибкой: {response.status_code}")
            return
    except Exception as e:
        print(f"💥 Сервер не доступен: {e}")
        return
    
    # Быстрая проверка основных эндпоинтов
    endpoints = [
        "/api/v1/qr/order/1",
        "/api/v1/qr/employee/1", 
        "/api/v1/qr/mo/1",
        "/api/v1/orders",
        "/api/v1/mo",
        "/api/v1/employees"
    ]
    
    print("\\n🔍 ПРОВЕРКА ОСНОВНЫХ ЭНДПОИНТОВ:")
    for endpoint in endpoints:
        try:
            start_time = time.time()
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                print(f"   ✅ {endpoint} - {response.status_code} ({response_time:.0f}ms)")
            else:
                print(f"   ❌ {endpoint} - {response.status_code} ({response_time:.0f}ms)")
        except Exception as e:
            print(f"   💥 {endpoint} - {e}")
    
    print("\\n" + "=" * 50)
    print("🎯 СТАТУС: Система проверена")

if __name__ == "__main__":
    smoke_test()
