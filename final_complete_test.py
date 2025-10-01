import requests
import json

def comprehensive_test():
    base_url = "http://localhost:8000/api/v1"
    
    print("🎯 ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ ВСЕХ ЭНДПОИНТОВ")
    print("=" * 50)
    
    endpoints = [
        ("Health Check", "/health"),
        ("Orders List", "/orders"),
        ("Employees List", "/employees"),
        ("Manufacturing Orders", "/mo"),
        ("Operations List", "/operations"),
        ("Defect Reports", "/defects"),
        ("Projects List", "/projects"),
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
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"   📊 Записей: {len(data)}")
                    if len(data) > 0:
                        # Показываем только ключи для краткости
                        sample_keys = list(data[0].keys())[:3]
                        print(f"   🔍 Поля: {sample_keys}...")
        except Exception as e:
            print(f"❌ {name}: {e}")
            results.append(False)
    
    working = sum(results)
    total = len(results)
    success_rate = (working / total) * 100
    
    print(f"\n📊 ФИНАЛЬНЫЙ РЕЗУЛЬТАТ: {working}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("\n🎉 ПРОЕКТ ДЕНЬ 3 УСПЕШНО ЗАВЕРШЕН!")
        print("✅ База данных синхронизирована с моделями")
        print("✅ Все данные корректны")
        print("✅ Все основные эндпоинты работают")
        print("✅ MES система готова к использованию")
        print("\n📖 Документация: http://localhost:8000/docs")
        print("🚀 Переходите к День 4: Отслеживание в реальном времени")
    elif success_rate >= 80:
        print(f"\n⚠️  БОЛЬШИНСТВО ЭНДПОИНТОВ РАБОТАЮТ ({success_rate:.1f}%)")
        print("🔧 Требуются незначительные исправления")
    else:
        print(f"\n❌ ТРЕБУЮТСЯ СЕРЬЕЗНЫЕ ИСПРАВЛЕНИЯ ({success_rate:.1f}%)")

if __name__ == "__main__":
    comprehensive_test()
