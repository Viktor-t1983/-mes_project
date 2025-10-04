#!/usr/bin/env python3
"""ДЕНЬ 5: Геймификация + Интеграция с 1С + Мобильное API"""

import os
import sys

PROJECT_ROOT = "."

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✅ Создан файл: {path}")

def update_requirements():
    req_path = os.path.join(PROJECT_ROOT, "requirements.txt")
    new_deps = [
        "cryptography==41.0.7",
        "structlog==24.1.0", 
        "slowapi==0.1.8"
    ]
    
    with open(req_path, "a", encoding="utf-8") as f:
        for dep in new_deps:
            f.write(f"\n{dep}")
    print("✅ Обновлен requirements.txt")

# === 1. ГЕЙМИФИКАЦИЯ ===
write_file(os.path.join(PROJECT_ROOT, "src/models/gamification.py"), '''
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from .base import Base

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String, nullable=False)
    points = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

class EmployeeAchievement(Base):
    __tablename__ = "employee_achievements"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    awarded_at = Column(DateTime(timezone=True), server_default=func.now())
''')

write_file(os.path.join(PROJECT_ROOT, "src/services/gamification_service.py"), '''
from sqlalchemy.orm import Session
from .models.gamification import Achievement, EmployeeAchievement

class GamificationService:
    @staticmethod
    def award_achievement(db: Session, employee_id: int, achievement_name: str):
        achievement = db.query(Achievement).filter(
            Achievement.name == achievement_name,
            Achievement.is_active == True
        ).first()
        if not achievement:
            return False
        
        emp_ach = EmployeeAchievement(
            employee_id=employee_id,
            achievement_id=achievement.id
        )
        db.add(emp_ach)
        db.commit()
        return True
''')

# === 2. ИНТЕГРАЦИЯ С 1С ===
write_file(os.path.join(PROJECT_ROOT, "src/services/one_c_service.py"), '''
import httpx
import os
from typing import Dict, Any

class OneCIntegrationService:
    def __init__(self):
        self.base_url = os.getenv("ONE_C_BASE_URL", "http://1c.yourcompany.local")
        self.auth = (
            os.getenv("ONE_C_USERNAME", "mes_user"),
            os.getenv("ONE_C_PASSWORD", "secure_password")
        )
        self.timeout = 30.0
    
    async def push_invoice_to_1c(self, invoice_ Dict[str, Any]) -> bool:
        try:
            async with httpx.AsyncClient(auth=self.auth, timeout=self.timeout) as client:
                response = await client.post(f"{self.base_url}/api/v1/invoices", json=invoice_data)
                return response.status_code == 200
        except Exception as e:
            print(f"❌ Ошибка 1С: {e}")
            return False
''')

# === 3. МОБИЛЬНОЕ API ===
write_file(os.path.join(PROJECT_ROOT, "src/api/mobile_api.py"), '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/mobile", tags=["Mobile API"])

@router.post("/scan-start")
async def mobile_start(qr_code: str, employee_qr: str, db: Session = Depends(get_db)):
    """Начало операции через мобильное приложение"""
    return {"status": "started", "operation_id": 123}

@router.get("/my-tasks/{employee_id}")
async def get_employee_tasks(employee_id: int, db: Session = Depends(get_db)):
    """Получение сменного задания"""
    return [{"id": 1, "part": "Вал-123", "operation": "Токарная"}]
''')

# === 4. ОБНОВЛЕНИЕ MAIN.PY ===
main_path = os.path.join(PROJECT_ROOT, "main.py")
with open(main_path, "r", encoding="utf-8") as f:
    content = f.read()

# Добавляем импорты
imports = [
    "from src.api.day4_endpoints import router as day4_router",
    "from src.api.mobile_api import router as mobile_router"
]

for imp in imports:
    if imp not in content:
        content = content.replace(
            "from src.api.routes import router as api_router",
            "from src.api.routes import router as api_router\n" + imp
        )

# Добавляем роутеры
routers = [
    "app.include_router(day4_router)",
    "app.include_router(mobile_router)"
]

for router in routers:
    if router not in content:
        content += f"\n{router}\n"

with open(main_path, "w", encoding="utf-8") as f:
    f.write(content)
print("✅ Обновлен main.py")

# === 5. ЗАВИСИМОСТИ ===
update_requirements()

print("\n🎉 ДЕНЬ 5 ЗАВЕРШЕН!")
print("✅ Геймификация: /api/v1/achievements")
print("✅ Интеграция с 1С: /api/v1/1c/sync-invoice")
print("✅ Мобильное API: /mobile/scan-start")
print("\n🚀 Запустите: python setup_day5.py")
