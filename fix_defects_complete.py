# Полное исправление эндпоинта defects
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Ищем и заменяем эндпоинт defects
import re

# Новый корректный эндпоинт
new_defect_endpoint = '''@app.post("/api/v1/defects")
async def create_defect_report(
    manufacturing_order_id: int,
    operation_id: int,
    reported_by: int,
    description: str,
    defect_type: str = "качество",
    severity: str = "medium",
    quantity_affected: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """
    Создание отчета о дефекте
    """
    defect = DefectReport(
        manufacturing_order_id=manufacturing_order_id,
        operation_id=operation_id,
        reported_by=reported_by,
        defect_description=description,
        defect_type=defect_type,
        severity=severity,
        quantity_affected=quantity_affected,
        status="reported"
    )
    db.add(defect)
    await db.commit()
    await db.refresh(defect)
    return {"message": "Брак зарегистрирован", "id": defect.id}'''

# Заменяем старый эндпоинт
old_pattern = r'@app\.post\("/api/v1/defects"\)[^}]*?defect\.id\}'
content = re.sub(old_pattern, new_defect_endpoint, content, flags=re.DOTALL)

# Сохраняем исправления
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Эндпоинт defects исправлен!")
print("📋 Добавлены обязательные поля: manufacturing_order_id, operation_id, reported_by")
