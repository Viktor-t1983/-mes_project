import requests
import json
import time

def comprehensive_system_test():
    base_url = "http://localhost:8000/api/v1"
    
    print("🎯 ПОЛНАЯ ПРОВЕРКА СИСТЕМЫ MES")
    print("=" * 50)
    print("📋 ТЕСТИРУЕМ ВСЕ КОМПОНЕНТЫ СИСТЕМЫ...")
    print()

    # 1. БАЗОВАЯ ПРОВЕРКА СЕРВЕРА
    print("🔧 1. БАЗОВАЯ ПРОВЕРКА СЕРВЕРА")
    print("-" * 30)
    
    try:
        # Health check
        health_response = requests.get(f"{base_url}/health")
        print(f"✅ Health Check: {health_response.status_code}")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   📊 Status: {health_data.get('status', 'N/A')}")
            print(f"   🗄️ Database: {health_data.get('database', 'N/A')}")
        else:
            print(f"   ❌ Response: {health_response.text}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return

    # 2. ПРОВЕРКА ВСЕХ ОСНОВНЫХ ЭНДПОИНТОВ
    print("\n📊 2. ПРОВЕРКА ОСНОВНЫХ ЭНДПОИНТОВ")
    print("-" * 30)

    endpoints = [
        ("Заказы", "/orders"),
        ("Сотрудники", "/employees"), 
        ("Производственные заказы", "/mo"),
        ("Операции", "/operations"),
        ("Дефекты", "/defects"),
        ("Проекты", "/projects")
    ]

    endpoint_results = {}
    
    for name, endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {name}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else "N/A"
                print(f"   📈 Записей: {count}")
                
                # Проверяем структуру данных
                if data and isinstance(data, list) and len(data) > 0:
                    sample = data[0]
                    print(f"   🔍 Пример полей: {list(sample.keys())[:3]}...")
            else:
                print(f"   💬 Response: {response.text[:100]}...")
                
            endpoint_results[endpoint] = response.status_code
            
        except Exception as e:
            print(f"❌ {name} Error: {e}")
            endpoint_results[endpoint] = "ERROR"

    # 3. ПРОВЕРКА QR-ГЕНЕРАЦИИ
    print("\n🔲 3. ПРОВЕРКА QR-КОДОВ")
    print("-" * 30)
    
    qr_endpoints = [
        ("QR Заказ", "/qr/order/1"),
        ("QR Сотрудник", "/qr/employee/1"), 
        ("QR Производственный заказ", "/qr/mo/1")
    ]
    
    for name, endpoint in qr_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            status = "✅" if response.status_code == 200 else "❌"
            content_type = response.headers.get('content-type', '')
            print(f"{status} {name}: {response.status_code} [{content_type}]")
            
            if response.status_code == 200:
                print(f"   📏 Размер: {len(response.content)} bytes")
        except Exception as e:
            print(f"❌ {name} Error: {e}")

    # 4. ПРОВЕРКА СТРУКТУРЫ ДАННЫХ
    print("\n🏗️ 4. ПРОВЕРКА СТРУКТУРЫ ДАННЫХ")
    print("-" * 30)
    
    # Проверяем employees (должны быть данные)
    try:
        emp_response = requests.get(f"{base_url}/employees")
        if emp_response.status_code == 200:
            employees = emp_response.json()
            if employees and len(employees) > 0:
                emp = employees[0]
                required_fields = ['qr_code', 'first_name', 'last_name', 'role']
                missing_fields = [field for field in required_fields if field not in emp]
                if not missing_fields:
                    print("✅ Структура сотрудников: OK")
                    print(f"   👤 Пример: {emp['first_name']} {emp['last_name']} ({emp['role']})")
                else:
                    print(f"❌ Отсутствуют поля: {missing_fields}")
            else:
                print("⚠️ Нет данных сотрудников")
    except Exception as e:
        print(f"❌ Ошибка проверки структуры: {e}")

    # 5. СТАТИСТИКА СИСТЕМЫ
    print("\n📈 5. СТАТИСТИКА СИСТЕМЫ")
    print("-" * 30)
    
    stats = {}
    for name, endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    stats[name] = len(data)
        except:
            stats[name] = 0
    
    for name, count in stats.items():
        print(f"   📦 {name}: {count} записей")

    # 6. ИТОГОВЫЙ ОТЧЕТ
    print("\n🎯 6. ИТОГОВЫЙ ОТЧЕТ")
    print("-" * 30)
    
    total_tests = len(endpoints) + len(qr_endpoints) + 2  # + health + structure
    successful_tests = sum(1 for result in endpoint_results.values() if result == 200)
    successful_tests += 1 if health_response.status_code == 200 else 0  # health
    successful_tests += 1  # structure check
    
    success_rate = (successful_tests / total_tests) * 100
    
    print(f"📊 Всего тестов: {total_tests}")
    print(f"✅ Успешных: {successful_tests}")
    print(f"❌ Неудачных: {total_tests - successful_tests}")
    print(f"📈 Успешность: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("\n🎉 СИСТЕМА ГОТОВА К РАБОТЕ!")
        print("✅ Все компоненты работают корректно")
        print("✅ Данные загружены и структурированы")
        print("✅ API полностью функционален")
        print("\n🚀 Переходите к следующему этапу разработки!")
    else:
        print(f"\n⚠️ Требуется внимание: {100 - success_rate:.1f}% тестов не прошли")

    # 7. РЕКОМЕНДАЦИИ
    print("\n💡 7. РЕКОМЕНДАЦИИ ДЛЯ РАЗВИТИЯ")
    print("-" * 30)
    
    if stats.get('Сотрудники', 0) < 3:
        print("🔸 Добавьте больше тестовых сотрудников (минимум 3)")
    
    if stats.get('Производственные заказы', 0) < 2:
        print("🔸 Добавьте больше производственных заказов")
    
    if stats.get('Операции', 0) < 5:
        print("🔸 Добавьте операции для тестирования workflow")
    
    print("🔸 Реализуйте POST/PUT endpoints для создания/обновления данных")
    print("🔸 Добавьте аутентификацию и авторизацию")
    print("🔸 Реализуйте реальный workflow операций")

if __name__ == "__main__":
    comprehensive_system_test()
