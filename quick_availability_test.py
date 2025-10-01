import requests
import time

def quick_test():
    print("🚀 БЫСТРЫЙ ТЕСТ ДОСТУПНОСТИ")
    print("=" * 40)
    
    test_urls = [
        "http://localhost:8000/docs",
        "http://127.0.0.1:8000/docs", 
        "http://0.0.0.0:8000/docs"
    ]
    
    for url in test_urls:
        try:
            start = time.time()
            response = requests.get(url, timeout=5)
            response_time = (time.time() - start) * 1000
            print(f"✅ {url} - {response.status_code} ({response_time:.0f}ms)")
            
            # Если один из URL работает, тестируем основные эндпоинты
            if response.status_code == 200:
                test_main_endpoints()
                return True
                
        except Exception as e:
            print(f"❌ {url} - {e}")
    
    print("\n💡 СОВЕТ: Проверьте что сервер запущен в Терминале 1")
    return False

def test_main_endpoints():
    print("\n🔍 ТЕСТ ОСНОВНЫХ ЭНДПОИНТОВ:")
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/api/v1/qr/order/1",
        "/api/v1/qr/employee/1",
        "/api/v1/qr/mo/1",
        "/api/v1/orders",
        "/api/v1/mo"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=3)
            status = "✅" if response.status_code == 200 else "⚠️"
            print(f"   {status} {endpoint} - {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint} - {e}")

if __name__ == "__main__":
    if quick_test():
        print("\n🎉 СЕРВЕР РАБОТАЕТ! Система готова к тестированию.")
    else:
        print("\n❌ СЕРВЕР НЕ ДОСТУПЕН. Проверьте запуск в Терминале 1.")
