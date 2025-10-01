import os

def check_structure():
    print("📁 ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА")
    print("=" * 50)
    
    required_dirs = ["src", "src/models", "src/schemas", "src/utils"]
    required_files = [
        "src/database.py",
        "src/models/employee.py", 
        "src/models/manufacturing_order.py",
        "src/models/operation.py",
        "src/models/defect_report.py",
        "src/models/order.py",
        "src/models/project.py",
        "src/schemas/employee.py",
        "src/schemas/manufacturing_order.py", 
        "src/schemas/operation.py",
        "src/schemas/defect_report.py",
        "src/schemas/order.py",
        "src/schemas/project.py",
        "src/utils/qrcode_generator.py"
    ]
    
    print("ПАПКИ:")
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path}")
    
    print("\nФАЙЛЫ:")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")

if __name__ == "__main__":
    check_structure()
