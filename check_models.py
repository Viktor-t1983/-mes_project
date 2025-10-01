import os

def check_models():
    print("🔍 ПРОВЕРКА МОДЕЛЕЙ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    models_dir = "src/models"
    model_files = [
        "employee.py", "manufacturing_order.py", "operation.py", 
        "defect_report.py", "order.py", "project.py"
    ]
    
    for model_file in model_files:
        file_path = os.path.join(models_dir, model_file)
        if os.path.exists(file_path):
            print(f"📄 {model_file}:")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Ищем поля модели
                if "Column" in content:
                    lines = content.split('\n')
                    for line in lines:
                        if "Column" in line and "=" in line:
                            print(f"   📝 {line.strip()}")
        else:
            print(f"❌ {model_file} не найден")

if __name__ == "__main__":
    check_models()
