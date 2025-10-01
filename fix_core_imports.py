"""
Исправляем все импорты на использование core.database
"""

def fix_model_imports():
    models = [
        "employee.py",
        "operation.py", 
        "order.py",
        "project.py",
        "manufacturing_order.py", 
        "defect_report.py"
    ]
    
    for model in models:
        filepath = f"src/models/{model}"
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Заменяем все варианты импортов на core.database
            content = content.replace("from src.database import Base", "from src.core.database import Base")
            content = content.replace("from ..database import Base", "from src.core.database import Base")
            content = content.replace("from . import Base", "from src.core.database import Base")
            content = content.replace("from src.core.database import Base", "from src.core.database import Base")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Исправлен импорт в {model}")
        except Exception as e:
            print(f"❌ Ошибка в {model}: {e}")

def fix_main_import():
    """Исправляем импорт в main.py если нужно"""
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Заменяем импорт database если есть
        content = content.replace("from src.database import", "from src.core.database import")
        
        with open("main.py", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Исправлены импорты в main.py")
    except Exception as e:
        print(f"❌ Ошибка в main.py: {e}")

if __name__ == "__main__":
    print("🛠 ИСПРАВЛЕНИЕ ИМПОРТОВ НА CORE.DATABASE")
    fix_model_imports()
    fix_main_import()
    print("\\n✅ ВСЕ ИМПОРТЫ ИСПРАВЛЕНЫ!")
