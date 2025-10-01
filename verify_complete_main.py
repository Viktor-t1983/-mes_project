import os

def verify_main_complete():
    print("🔍 ПРОВЕРКА ПОЛНОТЫ main_complete.py")
    print("=" * 50)
    
    with open('main_complete.py', 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    print(f"Размер файла: {len(content)} символов")
    print(f"Количество строк: {len(lines)}")
    
    # Ключевые компоненты которые должны быть в файле
    key_components = [
        "from src.database import get_db, engine, Base",
        "EmployeeCreate",
        "ManufacturingOrderCreate", 
        "OperationCreate",
        "DefectReportCreate",
        "OrderCreate",
        "ProjectCreate",
        "@app.post('/api/v1/employees'",
        "@app.post('/api/v1/orders'",
        "@app.post('/api/v1/mo'",
        "@app.post('/api/v1/operations'",
        "@app.post('/api/v1/operations/start'",
        "@app.post('/api/v1/operations/pause'",
        "@app.post('/api/v1/operations/complete'",
        "@app.post('/api/v1/defects'",
        "@app.post('/api/v1/projects'",
        "uvicorn.run(app"
    ]
    
    missing = []
    for component in key_components:
        if component not in content:
            missing.append(component)
    
    if not missing:
        print("✅ Файл содержит все ключевые компоненты!")
        return True
    else:
        print("❌ Отсутствующие компоненты:")
        for item in missing:
            print(f"   - {item}")
        return False

if __name__ == "__main__":
    verify_main_complete()
