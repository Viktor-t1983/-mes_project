import os

def analyze_missing_endpoints():
    print("🔧 ДЕТАЛЬНЫЙ АНАЛИЗ ОТСУТСТВУЮЩИХ ЭНДПОИНТОВ")
    print("=" * 60)
    
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Все необходимые POST эндпоинты для День 3
    required_endpoints = {
        "POST": [
            ("/api/v1/employees", "Создание сотрудника"),
            ("/api/v1/orders", "Создание заказа"),
            ("/api/v1/mo", "Создание производственного задания"),
            ("/api/v1/defects", "Создание отклонения"),
            ("/api/v1/projects", "Создание проекта"),
            ("/api/v1/operations", "Создание операции"),
            ("/api/v1/operations/start", "Запуск операции"),
            ("/api/v1/operations/pause", "Пауза операции"),
            ("/api/v1/operations/complete", "Завершение операции")
        ]
    }
    
    missing_count = 0
    print("ОТСУТСТВУЮЩИЕ POST ЭНДПОИНТЫ:")
    print("-" * 40)
    
    for method, endpoints in required_endpoints.items():
        for endpoint, description in endpoints:
            endpoint_pattern = f"@app.{method.lower()}('{endpoint}')"
            if endpoint_pattern in content:
                print(f"✅ {method} {endpoint} - {description}")
            else:
                print(f"❌ {method} {endpoint} - {description}")
                missing_count += 1
    
    print(f"\n📊 ИТОГО: Отсутствует {missing_count} POST эндпоинтов")
    
    # Проверяем наличие необходимых импортов
    print(f"\n🔍 ПРОВЕРКА ИМПОРТОВ:")
    print("-" * 40)
    
    required_imports = [
        "EmployeeCreate", "ManufacturingOrderCreate", "OperationCreate",
        "DefectReportCreate", "OrderCreate", "ProjectCreate"
    ]
    
    for imp in required_imports:
        if imp in content:
            print(f"✅ {imp}")
        else:
            print(f"❌ {imp}")
    
    return missing_count

if __name__ == "__main__":
    analyze_missing_endpoints()
