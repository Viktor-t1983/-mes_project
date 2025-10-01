import requests
import os

def generate_final_report():
    print("🎯 ФИНАЛЬНЫЙ ОТЧЕТ СООТВЕТСТВИЯ 'ДЕНЬ 3: ПРОИЗВОДСТВЕННОЕ ЯДРО'")
    print("=" * 70)
    
    # Требования День 3
    requirements = {
        "🔹 МОДЕЛИ ДАННЫХ": {
            "Employee": "Сотрудники",
            "ManufacturingOrder": "Производственные задания", 
            "Operation": "Операции",
            "DefectReport": "Отчеты о дефектах"
        },
        "🔹 СХЕМЫ PYDANTIC": {
            "employee.py": "Схемы сотрудников",
            "manufacturing_order.py": "Схемы производственных заданий",
            "operation.py": "Схемы операций", 
            "defect_report.py": "Схемы дефектов"
        },
        "🔹 УТИЛИТЫ": {
            "qrcode_generator.py": "Генератор QR-кодов"
        },
        "🔹 КЛЮЧЕВЫЕ ЭНДПОИНТЫ": {
            "POST /api/v1/mo": "Создание производственного задания",
            "POST /api/v1/operations/start": "Запуск операции",
            "POST /api/v1/operations/pause": "Пауза операции", 
            "POST /api/v1/operations/complete": "Завершение операции",
            "POST /api/v1/defects": "Создание отклонения",
            "GET /api/v1/qr/{entity}/{id}": "Генерация QR-кодов"
        },
        "🔹 МИГРАЦИИ": {
            "migrations/ folder": "Папка миграций Alembic",
            "alembic.ini": "Конфигурация Alembic"
        }
    }
    
    compliance_score = 0
    total_requirements = 0
    
    for category, items in requirements.items():
        print(f"\n{category}")
        print("-" * 40)
        
        for item, description in items.items():
            total_requirements += 1
            
            # Проверяем наличие файлов/папок
            if item.endswith('.py') or 'folder' in item:
                if os.path.exists(item.replace('folder', '')):
                    print(f"  ✅ {description}")
                    compliance_score += 1
                else:
                    print(f"  ❌ {description}")
            
            # Проверяем эндпоинты
            elif item.startswith(('GET', 'POST')):
                method, endpoint = item.split(' ')
                try:
                    if method == 'GET':
                        response = requests.get(f"http://localhost:8000{endpoint.replace('{id}', '1').replace('{entity}', 'order')}")
                    else:
                        response = requests.post(f"http://localhost:8000{endpoint}", json={})
                    
                    if response.status_code in [200, 201, 422]:  # 422 - validation error, but endpoint exists
                        print(f"  ✅ {description}")
                        compliance_score += 1
                    else:
                        print(f"  ⚠️  {description} (код: {response.status_code})")
                except:
                    print(f"  ❌ {description}")
    
    # Расчет соответствия
    compliance_percentage = (compliance_score / total_requirements) * 100
    
    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"   Выполнено требований: {compliance_score}/{total_requirements}")
    print(f"   Процент соответствия: {compliance_percentage:.1f}%")
    
    print(f"\n🎯 ВЕРДИКТ СООТВЕТСТВИЯ ДЕНЬ 3:")
    if compliance_percentage >= 90:
        print("   ✅ ПОЛНОСТЬЮ СООТВЕТСТВУЕТ - Производственное ядро реализовано!")
    elif compliance_percentage >= 70:
        print("   ⚠️  ЧАСТИЧНО СООТВЕТСТВУЕТ - Требуются minor доработки")  
    else:
        print("   ❌ НЕ СООТВЕТСТВУЕТ - Требуется significant работа")
    
    print(f"\n🔍 РЕКОМЕНДАЦИИ:")
    if compliance_percentage < 100:
        print("   1. Проверьте наличие всех моделей в src/models/")
        print("   2. Убедитесь, что все эндпоинты импортированы в main.py")
        print("   3. Проверьте подключение к БД в .env файле")
        print("   4. Запустите миграции: alembic upgrade head")
    else:
        print("   🎉 Система готова к переходу на День 4!")

if __name__ == "__main__":
    generate_final_report()
