import requests
import json
import time

BASE_URL = "http://localhost:8000"

def wait_for_server():
    """Ждем запуск сервера"""
    print("🔄 Проверяем доступность сервера...")
    for i in range(15):
        try:
            response = requests.get(f"{BASE_URL}/docs", timeout=5)
            if response.status_code == 200:
                print("✅ Сервер запущен и готов!")
                return True
        except Exception as e:
            print(f"⏳ Ожидание сервера... {i+1}/15")
            time.sleep(2)
    print("❌ Сервер не запустился за отведенное время")
    return False

def full_system_test():
    print("\\n🎯 ПОЛНЫЙ ТЕСТ СИСТЕМЫ MES-X API")
    print("=" * 60)
    
    if not wait_for_server():
        return
    
    # 1. СОЗДАЕМ ТЕСТОВЫЕ ДАННЫЕ
    print("\\n1. 📋 СОЗДАЕМ ТЕСТОВЫЕ ДАННЫЕ:")
    
    # Создаем сотрудника (для reported_by)
    try:
        response = requests.post(f"{BASE_URL}/api/v1/employees", params={
            "first_name": "Иван",
            "last_name": "Контролеров", 
            "role": "Контролер качества"
        }, timeout=10)
        print(f"   👥 Сотрудник: {response.status_code}")
        if response.status_code == 200:
            employee_data = response.json()
            print(f"      ID: {employee_data.get('id')}")
            employee_id = employee_data.get('id')
        else:
            print(f"      Ошибка: {response.text}")
            employee_id = 1  # fallback
    except Exception as e:
        print(f"   ❌ Ошибка создания сотрудника: {e}")
        employee_id = 1
    
    # Создаем MO
    try:
        response = requests.post(f"{BASE_URL}/api/v1/mo", params={
            "order_number": "RESTART-TEST-001",
            "product_name": "Тест после перезапуска",
            "product_code": "RESTART-TEST",
            "quantity": 5
        }, timeout=10)
        print(f"   🏭 Производственное задание: {response.status_code}")
        if response.status_code == 200:
            mo_data = response.json()
            mo_id = mo_data.get('id')
            print(f"      ID: {mo_id}")
        else:
            print(f"      Ошибка: {response.text}")
            mo_id = 1
    except Exception as e:
        print(f"   ❌ Ошибка создания MO: {e}")
        mo_id = 1
    
    # Создаем операцию
    try:
        response = requests.post(f"{BASE_URL}/api/v1/operations", params={
            "manufacturing_order_id": mo_id,
            "operation_number": "OP-RESTART-TEST",
            "name": "Тестовая операция",
            "description": "Операция для тестирования после перезапуска"
        }, timeout=10)
        print(f"   ⚙️ Операция: {response.status_code}")
        if response.status_code == 200:
            op_data = response.json()
            operation_id = op_data.get('id')
            print(f"      ID: {operation_id}")
        else:
            print(f"      Ошибка: {response.text}")
            operation_id = 1
    except Exception as e:
        print(f"   ❌ Ошибка создания операции: {e}")
        operation_id = 1
    
    # 2. ТЕСТИРУЕМ ИСПРАВЛЕННЫЙ DEFECTS ЭНДПОИНТ
    print("\\n2. ⚠️ ТЕСТИРУЕМ СИСТЕМУ ДЕФЕКТОВ:")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/defects", params={
            "manufacturing_order_id": mo_id,
            "operation_id": operation_id,
            "reported_by": employee_id,
            "description": "Тестовый дефект после полного перезапуска системы",
            "defect_type": "качество",
            "severity": "medium",
            "quantity_affected": 1
        }, timeout=10)
        
        print(f"   🎯 Создание дефекта: {response.status_code}")
        if response.status_code == 200:
            defect_data = response.json()
            print(f"      ✅ УСПЕХ: {defect_data}")
        else:
            print(f"      ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   💥 Критическая ошибка: {e}")
    
    # 3. ПРОВЕРЯЕМ СПИСОК ДЕФЕКТОВ
    print("\\n3. 📊 ПРОВЕРЯЕМ ДАННЫЕ:")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/defects", timeout=10)
        print(f"   📋 Список дефектов: {response.status_code}")
        if response.status_code == 200:
            defects = response.json()
            print(f"      Найдено дефектов: {len(defects)}")
            for defect in defects[:3]:  # покажем первые 3
                print(f"      - ID: {defect.get('id')}, Описание: {defect.get('defect_description')[:50]}...")
    except Exception as e:
        print(f"   ❌ Ошибка получения дефектов: {e}")
    
    # 4. ПРОВЕРЯЕМ ОСНОВНЫЕ ЭНДПОИНТЫ
    print("\\n4. 🔄 ПРОВЕРЯЕМ ОСНОВНЫЕ ЭНДПОИНТЫ:")
    
    endpoints = [
        "/api/v1/orders",
        "/api/v1/mo", 
        "/api/v1/employees",
        "/api/v1/operations",
        "/api/v1/projects"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {endpoint}: {len(data)} записей")
            else:
                print(f"   ❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"   💥 {endpoint}: ошибка - {e}")
    
    print("\\n" + "=" * 60)
    print("🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
    print("📖 Документация API доступна по адресу: http://localhost:8000/docs")

if __name__ == "__main__":
    full_system_test()
