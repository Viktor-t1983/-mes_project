import os

def check_file_completeness():
    print("🔍 ПРОВЕРКА ПОЛНОТЫ ФАЙЛА main_complete_fixed.py")
    print("=" * 50)
    
    with open('main_complete_fixed.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_components = [
        "from src.database import get_db, engine, Base",
        "from src.models.employee import Employee",
        "from src.schemas.employee import EmployeeCreate",
        "@app.post('/api/v1/employees'",
        "@app.post('/api/v1/orders'",
        "@app.post('/api/v1/mo'",
        "@app.post('/api/v1/operations/start'",
        "@app.post('/api/v1/operations/pause'",
        "@app.post('/api/v1/operations/complete'",
        "@app.post('/api/v1/defects'",
        "@app.post('/api/v1/projects'"
    ]
    
    missing_count = 0
    for component in required_components:
        if component in content:
            print(f"✅ {component}")
        else:
            print(f"❌ {component}")
            missing_count += 1
    
    if missing_count == 0:
        print(f"\n🎉 Файл содержит все необходимые компоненты!")
        return True
    else:
        print(f"\n⚠️  Отсутствует {missing_count} компонентов!")
        return False

if __name__ == "__main__":
    check_file_completeness()
