import requests
import json

BASE_URL = "http://localhost:8001"

def test_basic_functionality():
    print("🚀 ТЕСТИРУЕМ БАЗОВУЮ ФУНКЦИОНАЛЬНОСТЬ MES СИСТЕМЫ")
    print("=" * 50)
    
    try:
        # 1. Проверяем здоровье системы
        print("1. 🔍 ПРОВЕРЯЕМ ЗДОРОВЬЕ СИСТЕМЫ")
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Система работает: {response.json()}")
        else:
            print(f"   ❌ Ошибка здоровья: {response.status_code}")
            return
        
        # 2. Создаем тестового сотрудника
        print("\n2. 👥 СОЗДАЕМ ТЕСТОВОГО СОТРУДНИКА")
        employee_data = {
            "qr_code": "TEST001",
            "first_name": "Тест",
            "last_name": "Тестов",
            "position": "Тестовая должность",
            "department": "Тестовый отдел"
        }
        
        response = requests.post(f"{BASE_URL}/employees/", json=employee_data, timeout=5)
        if response.status_code == 201:
            employee = response.json()
            print(f"   ✅ Создан сотрудник: {employee['first_name']} {employee['last_name']} (ID: {employee['id']})")
            employee_id = employee['id']
        else:
            print(f"   ❌ Ошибка создания сотрудника: {response.text}")
            return
        
        # 3. Создаем тестовое производственное задание
        print("\n3. 🏭 СОЗДАЕМ ТЕСТОВОЕ ЗАДАНИЕ")
        order_data = {
            "order_number": "TEST-ORDER-001",
            "product_name": "Тестовый продукт",
            "product_code": "TEST-PROD",
            "quantity": 10
        }
        
        response = requests.post(f"{BASE_URL}/manufacturing-orders/", json=order_data, timeout=5)
        if response.status_code == 201:
            order = response.json()
            print(f"   ✅ Создано задание: {order['product_name']} (ID: {order['id']})")
            order_id = order['id']
        else:
            print(f"   ❌ Ошибка создания задания: {response.text}")
            return
        
        # 4. Получаем список сотрудников
        print("\n4. 📊 ПРОВЕРЯЕМ ДАННЫЕ")
        response = requests.get(f"{BASE_URL}/employees/", timeout=5)
        if response.status_code == 200:
            employees = response.json()
            print(f"   ✅ Сотрудников в системе: {len(employees)}")
        
        response = requests.get(f"{BASE_URL}/manufacturing-orders/", timeout=5)
        if response.status_code == 200:
            orders = response.json()
            print(f"   ✅ Заданий в системе: {len(orders)}")
        
        print("\n" + "=" * 50)
        print("🎉 БАЗОВОЕ ТЕСТИРОВАНИЕ УСПЕШНО!")
        print("📚 Полная документация: http://localhost:8001/docs")
        
    except requests.exceptions.Timeout:
        print("❌ Таймаут запроса - сервер не отвечает")
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения - сервер не запущен")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    test_basic_functionality()
