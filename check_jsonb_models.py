import os

print("🔍 Проверка использования JSONB в моделях:")
print("=" * 45)

# Проверяем модель Operation
operation_file = 'src/models/operation.py'
if os.path.exists(operation_file):
    with open(operation_file, 'r', encoding='utf-8') as f:
        op_content = f.read()
    
    if 'JSONB' in op_content:
        print("✅ Модель Operation использует JSONB для pause_events")
    else:
        print("⚠️  Модель Operation использует Text для pause_events")

# Проверяем модель DefectReport  
defect_file = 'src/models/defect_report.py'
if os.path.exists(defect_file):
    with open(defect_file, 'r', encoding='utf-8') as f:
        defect_content = f.read()
    
    if 'JSONB' in defect_content:
        print("✅ Модель DefectReport готова для JSONB")
    else:
        print("⚠️  Модель DefectReport может быть улучшена с JSONB")

print("\\n💡 Рекомендация: JSONB улучшает производительность для JSON данных")
print("   но текущая реализация с Text также работоспособна")
