import os

def check_schemas():
    print("🔍 ПРОВЕРКА СХЕМ PYDANTIC")
    print("=" * 50)
    
    schemas_dir = "src/schemas"
    schema_files = [
        "employee.py", "manufacturing_order.py", "operation.py", 
        "defect_report.py", "order.py", "project.py"
    ]
    
    for schema_file in schema_files:
        file_path = os.path.join(schemas_dir, schema_file)
        if os.path.exists(file_path):
            print(f"📄 {schema_file}:")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Проверяем наличие Create схем
                if "Create" in content:
                    print(f"   ✅ Create схема присутствует")
                else:
                    print(f"   ❌ Create схема отсутствует")
                
                # Проверяем базовые поля
                if "class " in content:
                    classes = [line for line in content.split('\n') if 'class ' in line and 'Create' in line]
                    for cls in classes:
                        print(f"   📝 {cls.strip()}")
        else:
            print(f"❌ {schema_file} не найден")

if __name__ == "__main__":
    check_schemas()
