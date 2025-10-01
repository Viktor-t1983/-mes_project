import requests
import time
import sys
import os

BASE_URL = "http://localhost:8000"

def check_directory_structure():
    """Проверяем структуру проекта"""
    print("📁 ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА")
    print("=" * 50)
    
    required_dirs = [
        "src/models",
        "src/schemas", 
        "src/utils",
        "migrations"
    ]
    
    required_files = [
        "main.py",
        "src/models/__init__.py",
        "src/models/employee.py",
        "src/models/manufacturing_order.py", 
        "src/models/operation.py",
        "src/models/defect_report.py",
        "src/schemas/__init__.py",
        "src/schemas/employee.py",
        "src/schemas/manufacturing_order.py",
        "src/schemas/operation.py", 
        "src/schemas/defect_report.py",
        "src/utils/qrcode_generator.py",
        ".env"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Папка: {dir_path}")
        else:
            print(f"❌ Отсутствует папка: {dir_path}")
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ Файл: {file_path}")
        else:
            print(f"❌ Отсутствует файл: {file_path}")

def check_server_availability():
    """Проверяем доступность сервера"""
    print("\n🌐 ПРОВЕРКА ДОСТУПНОСТИ СЕРВЕРА")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Сервер запущен и отвечает")
            print(f"📖 Документация: {BASE_URL}/docs")
            return True
        else:
            print(f"❌ Сервер отвечает с кодом: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Сервер не доступен: {e}")
        return False

def check_endpoints_functionality():
    """Проверяем функциональность эндпоинтов"""
    print("\n🔌 ТЕСТИРОВАНИЕ ЭНДПОИНТОВ")
    print("=" * 50)
    
    endpoints = [
        ("GET", "/api/v1/health", "Health Check", None),
        ("GET", "/api/v1/qr/order/1", "QR код заказа", None),
        ("GET", "/api/v1/qr/employee/1", "QR код сотрудника", None),
        ("GET", "/api/v1/qr/mo/1", "QR код производственного задания", None),
        ("GET", "/api/v1/orders", "Список заказов", None),
        ("GET", "/api/v1/mo", "Список производственных заданий", None),
        ("GET", "/api/v1/employees", "Список сотрудников", None),
        ("GET", "/api/v1/operations", "Список операций", None),
        ("GET", "/api/v1/defects", "Список отклонений", None),
        ("GET", "/api/v1/projects", "Список проектов", None),
    ]
    
    working_endpoints = []
    broken_endpoints = []
    
    for method, endpoint, description, data in endpoints:
        try:
            start_time = time.time()
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=10)
            
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                print(f"✅ {description} - 200 OK ({response_time:.0f}ms)")
                working_endpoints.append(endpoint)
            elif response.status_code == 500:
                print(f"⚠️  {description} - 500 (Ошибка БД)")
                broken_endpoints.append(endpoint)
                # Показываем детали ошибки для отладки
                try:
                    error_detail = response.json()
                    if 'detail' in error_detail:
                        print(f"   💡 Ошибка: {error_detail['detail']}")
                except:
                    pass
            else:
                print(f"❌ {description} - {response.status_code}")
                broken_endpoints.append(endpoint)
                
        except requests.exceptions.RequestException as e:
            print(f"🚫 {description} - Ошибка подключения: {e}")
            broken_endpoints.append(endpoint)
        except Exception as e:
            print(f"💥 {description} - Неожиданная ошибка: {e}")
            broken_endpoints.append(endpoint)
    
    return working_endpoints, broken_endpoints

def check_database_connection():
    """Проверяем подключение к БД"""
    print("\n🗄️  ПРОВЕРКА ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ")
    print("=" * 50)
    
    # Проверяем наличие .env файла
    if not os.path.exists('.env'):
        print("❌ Файл .env отсутствует")
        return False
    
    # Читаем настройки БД из .env
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
            if 'DATABASE_URL' in env_content:
                print("✅ Файл .env содержит DATABASE_URL")
                # Проверяем тип БД
                if 'postgresql' in env_content:
                    print("🔷 Используется PostgreSQL")
                elif 'sqlite' in env_content:
                    print("🔶 Используется SQLite")
                else:
                    print("⚠️  Неизвестный тип БД")
                return True
            else:
                print("❌ DATABASE_URL не найден в .env")
                return False
    except Exception as e:
        print(f"❌ Ошибка чтения .env: {e}")
        return False

def check_models_import():
    """Проверяем импорт моделей в main.py"""
    print("\n🔧 ПРОВЕРКА ИМПОРТА МОДЕЛЕЙ")
    print("=" * 50)
    
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_models = [
            'Employee',
            'ManufacturingOrder', 
            'Operation',
            'DefectReport',
            'Order'
        ]
        
        for model in required_models:
            if model in content:
                print(f"✅ Модель {model} импортирована")
            else:
                print(f"❌ Модель {model} не найдена в main.py")
                
    except Exception as e:
        print(f"❌ Ошибка проверки main.py: {e}")

def main():
    print("🎯 КОМПЛЕКСНАЯ ДИАГНОСТИКА СИСТЕМЫ MES")
    print("=" * 60)
    
    # 1. Проверяем структуру проекта
    check_directory_structure()
    
    # 2. Проверяем сервер
    if not check_server_availability():
        print("\n🚨 СЕРВЕР НЕ ДОСТУПЕН! Запустите в Терминале 1:")
        print("uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # 3. Проверяем БД
    check_database_connection()
    
    # 4. Проверяем импорт моделей
    check_models_import()
    
    # 5. Тестируем эндпоинты
    working, broken = check_endpoints_functionality()
    
    # 6. Итоговый отчет
    print("\n📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 50)
    print(f"✅ Работающие эндпоинты: {len(working)}")
    print(f"⚠️  Проблемные эндпоинты: {len(broken)}")
    
    if broken:
        print("\n🔧 Эндпоинты с проблемами:")
        for endpoint in broken:
            print(f"   - {endpoint}")
    
    # Проверяем соответствие День 3
    print("\n🎯 СООТВЕТСТВИЕ 'ДЕНЬ 3: ПРОИЗВОДСТВЕННОЕ ЯДРО'")
    print("=" * 50)
    
    day3_requirements = {
        "Модели данных": [
            "Employee", "ManufacturingOrder", "Operation", "DefectReport"
        ],
        "Схемы Pydantic": [
            "employee.py", "manufacturing_order.py", "operation.py", "defect_report.py"  
        ],
        "Утилиты": [
            "qrcode_generator.py"
        ],
        "Критические эндпоинты": [
            "/api/v1/mo (POST)",
            "/api/v1/operations/start (POST)", 
            "/api/v1/operations/pause (POST)",
            "/api/v1/operations/complete (POST)",
            "/api/v1/defects (POST)",
            "/api/v1/qr/{entity}/{id} (GET)"
        ]
    }
    
    all_requirements_met = True
    
    for category, requirements in day3_requirements.items():
        print(f"\n{category}:")
        for req in requirements:
            # Упрощенная проверка - в реальности нужно проверять функциональность
            if any(req.lower() in endpoint.lower() for endpoint in working):
                print(f"  ✅ {req}")
            else:
                print(f"  ❌ {req}")
                all_requirements_met = False
    
    if all_requirements_met:
        print("\n🎉 ВЫВОД: Система СООТВЕТСТВУЕТ требованиям День 3!")
    else:
        print("\n⚠️  ВЫВОД: Требуются доработки для полного соответствия День 3")

if __name__ == "__main__":
    main()
