"""
Проверяем отношения между моделями
"""

def check_model_relationships():
    models = [
        "employee.py",
        "operation.py", 
        "order.py",
        "project.py",
        "manufacturing_order.py",
        "defect_report.py"
    ]
    
    print("🔍 ПРОВЕРКА ОТНОШЕНИЙ В МОДЕЛЯХ")
    print("=" * 40)
    
    for model in models:
        filepath = f"src/models/{model}"
        print(f"\n📄 {model}:")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Ищем отношения
            if "relationship" in content:
                lines = [line for line in content.split('\n') if "relationship" in line]
                for line in lines:
                    print(f"   🔗 {line.strip()}")
            
            # Ищем ForeignKey
            if "ForeignKey" in content:
                lines = [line for line in content.split('\n') if "ForeignKey" in line]
                for line in lines:
                    print(f"   🗝️  {line.strip()}")
                    
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")

if __name__ == "__main__":
    check_model_relationships()
