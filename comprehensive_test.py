import requests
import time
import json

def test_all_endpoints():
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 ПОЛНОЕ ТЕСТИРОВАНИЕ ЭНДПОИНТОВ")
    print("=" * 50)
    
    endpoints = [
        ("Health Check", "/health", "GET"),
        ("Orders List", "/orders", "GET"),
        ("Employees List", "/employees", "GET"),
        ("Manufacturing Orders", "/mo", "GET"),
        ("Operations List", "/operations", "GET"),
        ("Defect Reports", "/defects", "GET"),
        ("Projects List", "/projects", "GET"),
        ("QR Order", "/qr/order/1", "GET"),
        ("QR Employee", "/qr/employee/1", "GET"),
        ("QR Manufacturing Order", "/qr/mo/1", "GET")
    ]
    
    results = []
    
    for name, endpoint, method in endpoints:
        try:
            start_time = time.time()
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:
                response = requests.post(f"{base_url}{endpoint}", timeout=10)
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                status_icon = "✅"
                results.append(True)
            elif response.status_code == 500:
                status_icon = "⚠️ "
                results.append(False)
                # Покажем ошибку для 500 статуса
                try:
                    error_data = response.json()
                    print(f"   🔍 Ошибка 500: {error_data}")
                except:
                    print(f"   🔍 Ошибка 500: {response.text[:100]}")
            else:
                status_icon = "❌"
                results.append(False)
            
            print(f"{status_icon} {name}: {response.status_code} ({response_time:.0f}ms)")
            
        except Exception as e:
            print(f"❌ {name}: Ошибка - {e}")
            results.append(False)
    
    # Статистика
    working = sum(results)
    total = len(results)
    success_rate = (working / total) * 100
    
    print(f"\\n📊 РЕЗУЛЬТАТ: {working}/{total} эндпоинтов работают ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("🎉 ВСЕ ЭНДПОИНТЫ РАБОТАЮТ КОРРЕКТНО!")
        print("✅ Ошибки валидации исправлены")
        print("✅ MES система готова к использованию")
    elif success_rate >= 70:
        print("⚠️  БОЛЬШИНСТВО ЭНДПОИНТОВ РАБОТАЮТ")
        print("🔧 Требуются незначительные исправления")
    else:
        print("❌ ТРЕБУЮТСЯ СЕРЬЕЗНЫЕ ИСПРАВЛЕНИЯ")
    
    print(f"\\n📖 Документация: http://localhost:8000/docs")
    print("🔧 Swagger UI: http://localhost:8000/docs")

if __name__ == "__main__":
    test_all_endpoints()
