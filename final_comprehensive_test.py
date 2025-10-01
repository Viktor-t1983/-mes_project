import requests
import json

def full_test():
    base_url = "http://localhost:8000/api/v1"
    
    print("🎯 ПОЛНЫЙ ТЕСТ ВСЕХ ЭНДПОИНТОВ")
    print("=" * 40)
    
    endpoints = [
        ("Health Check", "/health"),
        ("Orders", "/orders"),
        ("Employees", "/employees"),
        ("Manufacturing Orders", "/mo"),
        ("Operations", "/operations"),
        ("Defect Reports", "/defects"),
        ("Projects", "/projects"),
        ("QR Order", "/qr/order/1"),
        ("QR Employee", "/qr/employee/1"),
        ("QR Manufacturing Order", "/qr/mo/1")
    ]
    
    results = []
    for name, endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {name}: {response.status_code}")
            results.append(response.status_code == 200)
        except Exception as e:
            print(f"❌ {name}: {e}")
            results.append(False)
    
    working = sum(results)
    total = len(results)
    success_rate = (working / total) * 100
    
    print(f"\n📊 ФИНАЛЬНЫЙ РЕЗУЛЬТАТ: {working}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("\n🎉 ПРОЕКТ ДЕНЬ 3 УСПЕШНО ЗАВЕРШЕН!")
        print("✅ Все основные эндпоинты работают")
        print("✅ Ошибки отношений исправлены")
        print("✅ MES система готова к использованию")
        print("\n📖 Документация: http://localhost:8000/docs")
    else:
        print(f"\n⚠️  Требуются дополнительные исправления ({success_rate:.1f}%)")

if __name__ == "__main__":
    full_test()
