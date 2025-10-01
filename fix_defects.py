# Исправляем эндпоинт defects в main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим старый эндпоинт defects и заменяем его
import re

new_defects_endpoint = '''@app.post("/api/v1/defects")
async def create_defect_report(
    manufacturing_order_id: int,
    operation_id: int,
    description: str,
    reported_by: int,
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

# Заменяем старый эндпоинт на новый
pattern = r'@app\.post\("/api/v1/defects"\)[\s\S]*?return \{"message": "Брак зарегистрирован", "id": defect\.id\}'
content = re.sub(pattern, new_defects_endpoint, content)

# Сохраняем исправленный файл
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Эндпоинт defects исправлен!")
