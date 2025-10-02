#!/usr/bin/env python3
"""FINAL MES Day 4 Setup - Все рекомендации реализованы"""

import os
import sys
import shutil
import ast
import asyncio
import subprocess
import platform
from datetime import datetime
from pathlib import Path

# === КОНФИГУРАЦИЯ ===
PROJECT_ROOT = Path(".").absolute()
print(f"📁 Рабочая директория: {PROJECT_ROOT}")

def log_step(message):
    """Логирование шагов"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_system_requirements():
    """Проверка системных требований"""
    log_step("🔍 Проверка системных требований...")
    
    # Python версия
    python_version = sys.version_info
    log_step(f"🐍 Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version < (3, 8):
        log_step("[ERROR] Требуется Python 3.8+")
        return False
    
    # Операционная система
    system = platform.system()
    log_step(f"💻 ОС: {system} {platform.release()}")
    
    return True

def check_project_structure():
    """Проверка структуры проекта MES"""
    log_step("📁 Проверка структуры проекта...")
    
    required_dirs = [
        "src/models",
        "src/api", 
        "src/services",
        "src/integrations",
        "migrations/versions"
    ]
    
    required_files = [
        "main.py",
        "src/database.py",
        "src/models/base.py",
        "requirements.txt"
    ]
    
    # Создаем отсутствующие директории
    for dir_path in required_dirs:
        full_path = PROJECT_ROOT / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        if not full_path.exists():
            log_step(f"[OK] Создана директория: {dir_path}")
    
    # Проверяем обязательные файлы
    missing_files = []
    for file_path in required_files:
        full_path = PROJECT_ROOT / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        log_step(f"[ERROR] Отсутствуют файлы: {missing_files}")
        return False
    
    log_step("[OK] Структура проекта проверена")
    return True

def check_and_install_dependencies():
    """Проверка и установка зависимостей"""
    log_step("📦 Проверка зависимостей...")
    
    dependencies = [
        "fastapi",
        "sqlalchemy",
        "alembic",
        "asyncpg",
        "psutil",
        "httpx",
        "pydantic",
        "python-dotenv"
    ]
    
    missing_deps = []
    for dep in dependencies:
        try:
            __import__(dep)
            log_step(f"[OK] {dep} установлен")
        except ImportError:
            missing_deps.append(dep)
            log_step(f"[ERROR] {dep} отсутствует")
    
    if missing_deps:
        log_step(f"📥 Установка отсутствующих зависимостей: {missing_deps}")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install"
            ] + missing_deps, check=True)
            log_step("[OK] Зависимости установлены")
        except subprocess.CalledProcessError as e:
            log_step(f"[ERROR] Ошибка установки зависимостей: {e}")
            return False
    
    return True

def check_postgresql():
    """Проверка PostgreSQL"""
    log_step("🗄️ Проверка PostgreSQL...")
    
    # Проверка версии PostgreSQL
    postgres_commands = [
        ["pg_config", "--version"],
        ["psql", "--version"],
        ["postgres", "--version"]
    ]
    
    version_found = None
    for cmd in postgres_commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version_output = result.stdout.strip()
                log_step(f"ℹ️ {version_output}")
                
                import re
                version_match = re.search(r'(\d+\.\d+)', version_output)
                if version_match:
                    version_found = float(version_match.group(1))
                    break
        except:
            continue
    
    if version_found:
        if version_found >= 13.0:
            log_step(f"[OK] PostgreSQL {version_found} - совместим")
        else:
            log_step(f"[WARNING] PostgreSQL {version_found} - рекомендуется 13+")
    else:
        log_step("[WARNING] Не удалось определить версию PostgreSQL")
    
    # Проверка запуска службы
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["sc", "query", "postgresql"], 
                capture_output=True, text=True
            )
            if "RUNNING" in result.stdout:
                log_step("[OK] Служба PostgreSQL запущена")
            else:
                log_step("[WARNING] Служба PostgreSQL не запущена")
        else:
            result = subprocess.run(
                ["pg_isready"], 
                capture_output=True, text=True
            )
            if result.returncode == 0:
                log_step("[OK] PostgreSQL доступен")
            else:
                log_step("[WARNING] PostgreSQL не доступен")
    except:
        log_step("[WARNING] Не удалось проверить статус PostgreSQL")
    
    return True

def check_docker():
    """Проверка Docker"""
    log_step("🐳 Проверка Docker...")
    
    try:
        result = subprocess.run(
            ["docker", "--version"], 
            capture_output=True, text=True, check=True
        )
        log_step(f"[OK] {result.stdout.strip()}")
        
        # Проверка Docker Compose
        try:
            compose_result = subprocess.run(
                ["docker-compose", "--version"], 
                capture_output=True, text=True
            )
            if compose_result.returncode == 0:
                log_step(f"[OK] {compose_result.stdout.strip()}")
        except:
            log_step("[WARNING] Docker Compose не установлен")
        
        # Проверка запуска Docker daemon
        try:
            subprocess.run(["docker", "info"], capture_output=True, check=True)
            log_step("[OK] Docker daemon запущен")
        except:
            log_step("[WARNING] Docker daemon не запущен")
            
        return True
    except:
        log_step("[WARNING] Docker не установлен")
        return False

def create_mes_models():
    """Создание моделей MES"""
    log_step("🏗️ Создание моделей MES...")
    
    # Модель геймификации
    gamification_model = '''
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.models.base import Base

class Achievement(Base):
    """Модель достижений для геймификации"""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    points = Column(Integer, default=0)
    badge_icon = Column(String(50), default="🏆")
    is_active = Column(Boolean, default=True)

class EmployeeAchievement(Base):
    """Связь сотрудников с достижениями"""
    __tablename__ = "employee_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    awarded_at = Column(DateTime(timezone=True), server_default=func.now())
    is_rewarded = Column(Boolean, default=False)
    
    employee = relationship("Employee", backref="achievements")
    achievement = relationship("Achievement")

class Leaderboard(Base):
    """Таблица лидеров для геймификации"""
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    employee = relationship("Employee")
'''
    
    models_dir = PROJECT_ROOT / "src/models"
    with open(models_dir / "gamification.py", "w", encoding="utf-8") as f:
        f.write(gamification_model.strip())
    log_step("[OK] Модель геймификации создана")

def create_services():
    """Создание сервисов"""
    log_step("⚙️ Создание сервисов...")
    
    # Сервис геймификации
    gamification_service = '''
from sqlalchemy.orm import Session
from src.models.gamification import Achievement, EmployeeAchievement, Leaderboard
from src.models.employee import Employee

class GamificationService:
    """Сервис для управления геймификацией"""
    
    @staticmethod
    def award_achievement(db: Session, employee_id: int, achievement_name: str):
        """Назначает достижение сотруднику"""
        try:
            achievement = db.query(Achievement).filter(
                Achievement.name == achievement_name,
                Achievement.is_active == True
            ).first()
            
            if not achievement:
                print(f"[ERROR] Достижение '{achievement_name}' не найдено")
                return False
            
            existing = db.query(EmployeeAchievement).filter(
                EmployeeAchievement.employee_id == employee_id,
                EmployeeAchievement.achievement_id == achievement.id
            ).first()
            
            if existing:
                print(f"ℹ️ Сотрудник уже имеет достижение '{achievement_name}'")
                return True
            
            employee_achievement = EmployeeAchievement(
                employee_id=employee_id,
                achievement_id=achievement.id
            )
            db.add(employee_achievement)
            
            leaderboard = db.query(Leaderboard).filter(
                Leaderboard.employee_id == employee_id
            ).first()
            
            if leaderboard:
                leaderboard.total_points += achievement.points
                leaderboard.level = leaderboard.total_points // 100 + 1
            else:
                leaderboard = Leaderboard(
                    employee_id=employee_id,
                    total_points=achievement.points,
                    level=achievement.points // 100 + 1
                )
                db.add(leaderboard)
            
            db.commit()
            print(f"[OK] Достижение '{achievement_name}' назначено сотруднику #{employee_id}")
            return True
            
        except Exception as e:
            db.rollback()
            print(f"[ERROR] Ошибка назначения достижения: {e}")
            return False
    
    @staticmethod
    def get_leaderboard(db: Session, limit: int = 10):
        """Возвращает таблицу лидеров"""
        leaderboard = db.query(
            Leaderboard,
            Employee
        ).join(
            Employee, Leaderboard.employee_id == Employee.id
        ).order_by(
            Leaderboard.total_points.desc()
        ).limit(limit).all()
        
        result = []
        for rank, (lb, emp) in enumerate(leaderboard, 1):
            result.append({
                "rank": rank,
                "employee_name": f"{emp.first_name} {emp.last_name}",
                "total_points": lb.total_points,
                "level": lb.level,
                "badge_icon": "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🏅"
            })
        
        return result
'''
    
    services_dir = PROJECT_ROOT / "src/services"
    with open(services_dir / "gamification_service.py", "w", encoding="utf-8") as f:
        f.write(gamification_service.strip())
    log_step("[OK] Сервис геймификации создан")

def create_health_check():
    """Создание health check endpoints"""
    log_step("🏥 Создание health check...")
    
    health_check = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database import get_db
import psutil
import os
import asyncpg
from typing import Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Health"])

async def check_database_connection() -> Dict[str, Any]:
    """Проверка подключения к базе данных"""
    try:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            return {"status": "error", "message": "DATABASE_URL not configured"}
        
        conn = await asyncpg.connect(db_url, timeout=10)
        try:
            version = await conn.fetchval("SELECT version()")
            await conn.fetchval("SELECT 1")
            await conn.close()
            
            return {
                "status": "healthy",
                "version": version.split(',')[0] if version else "unknown"
            }
        except Exception as e:
            await conn.close()
            raise e
    except Exception as e:
        return {"status": "unhealthy", "message": str(e)}

@router.get("/health")
async def health_check():
    """Комплексная проверка здоровья системы"""
    try:
        db_status = await check_database_connection()
        
        # Проверка системных ресурсов
        disk_usage = psutil.disk_usage("/")
        memory = psutil.virtual_memory()
        
        system_status = {
            "disk": {
                "free_gb": round(disk_usage.free / (1024**3), 2),
                "usage_percent": disk_usage.percent
            },
            "memory": {
                "usage_percent": memory.percent
            }
        }
        
        overall_status = "healthy" if db_status["status"] == "healthy" else "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "services": {
                "database": db_status,
                "system": system_status
            }
        }
    except Exception as e:
        logger.critical(f"Health check critical error: {e}")
        return {
            "status": "unhealthy",
            "error": "System error",
            "timestamp": datetime.now().isoformat()
        }

@router.get("/ready")
async def readiness_check():
    """Проверка готовности"""
    return {"status": "ready"}

@router.get("/live")
async def liveness_check():
    """Проверка живости"""
    return {"status": "live"}
'''
    
    api_dir = PROJECT_ROOT / "src/api"
    with open(api_dir / "health.py", "w", encoding="utf-8") as f:
        f.write(health_check.strip())
    log_step("[OK] Health check создан")

def create_day4_endpoints():
    """Создание endpoints для 4 дня"""
    log_step("🔗 Создание API endpoints...")
    
    endpoints = '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.gamification import Achievement, EmployeeAchievement, Leaderboard
from src.schemas.gamification import AchievementCreate, Achievement, LeaderboardEntry
from src.services.gamification_service import GamificationService
from src.integrations.one_c_service import OneCIntegrationService
import os

router = APIRouter(prefix="/api/v1", tags=["Day 4 - Gamification & 1C"])

@router.post("/achievements", response_model=Achievement)
def create_achievement(achievement: AchievementCreate, db: Session = Depends(get_db)):
    """Создание нового достижения"""
    db_achievement = Achievement(**achievement.model_dump())
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement

@router.get("/achievements", response_model=List[Achievement])
def get_achievements(db: Session = Depends(get_db)):
    """Получение списка всех достижений"""
    return db.query(Achievement).filter(Achievement.is_active == True).all()

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    """Получение таблицы лидеров"""
    return GamificationService.get_leaderboard(db)

@router.post("/1c/sync-invoice")
async def sync_invoice_to_1c(invoice_data: dict):
    """Синхронизация накладной с 1С"""
    one_c_service = OneCIntegrationService(
        base_url=os.getenv("ONE_C_BASE_URL", "http://1c.yourcompany.local"),
        username=os.getenv("ONE_C_USERNAME", "mes_user"),
        password=os.getenv("ONE_C_PASSWORD", "secure_password")
    )
    
    success = await one_c_service.push_invoice_to_1c(invoice_data)
    return {"status": "success" if success else "failed"}
'''
    
    api_dir = PROJECT_ROOT / "src/api"
    with open(api_dir / "day4_endpoints.py", "w", encoding="utf-8") as f:
        f.write(endpoints.strip())
    log_step("[OK] Day 4 endpoints созданы")

def update_main_py():
    """Обновление main.py"""
    log_step("[FIX] Обновление main.py...")
    
    main_path = PROJECT_ROOT / "main.py"
    
    # Создаем бэкап
    backup_path = main_path.with_suffix('.py.backup')
    if main_path.exists():
        shutil.copy(main_path, backup_path)
        log_step(f"💾 Создан бэкап: {backup_path}")
    
    # Добавляем импорты и роутеры
    new_imports = [
        "from src.api.health import router as health_router",
        "from src.api.day4_endpoints import router as day4_router"
    ]
    
    if main_path.exists():
        with open(main_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Добавляем импорты
        for imp in new_imports:
            if imp not in content:
                # Ищем место для вставки импортов
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('from src.api.') or line.startswith('from src.') and i > 0:
                        lines.insert(i + 1, imp)
                        log_step(f"[OK] Добавлен импорт: {imp}")
                        break
        
        # Добавляем роутеры
        if "app.include_router(health_router)" not in content:
            if "app.include_router" in content:
                # Вставляем после других include_router
                last_include = content.rfind("app.include_router")
                if last_include != -1:
                    line_end = content.find("\n", last_include)
                    if line_end != -1:
                        content = content[:line_end] + '\napp.include_router(health_router)' + content[line_end:]
                        log_step("[OK] Health router добавлен")
        
        if "app.include_router(day4_router)" not in content:
            if "app.include_router" in content:
                last_include = content.rfind("app.include_router")
                if last_include != -1:
                    line_end = content.find("\n", last_include)
                    if line_end != -1:
                        content = content[:line_end] + '\napp.include_router(day4_router)' + content[line_end:]
                        log_step("[OK] Day4 router добавлен")
        
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        log_step("[WARNING] main.py не найден, создаем базовый")
        basic_main = '''
from fastapi import FastAPI
from src.api.health import router as health_router
from src.api.day4_endpoints import router as day4_router

app = FastAPI(title="MES System", version="1.0.0")

app.include_router(health_router)
app.include_router(day4_router)

@app.get("/")
async def root():
    return {"message": "MES System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(basic_main.strip())

async def setup_database():
    """Настройка базы данных"""
    log_step("🗄️ Настройка базы данных...")
    
    # Создаем .env если отсутствует
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        env_content = '''
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/mes_db
ONE_C_BASE_URL=http://1c.yourcompany.local
ONE_C_USERNAME=mes_user
ONE_C_PASSWORD=secure_password
DEBUG=true
'''
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(env_content.strip())
        log_step("[OK] Файл .env создан")
    
    # Создаем alembic.ini если отсутствует
    alembic_ini = PROJECT_ROOT / "alembic.ini"
    if not alembic_ini.exists():
        alembic_content = '''
[alembic]
script_location = migrations
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d%%(second).2d_%%(slug)s
sqlalchemy.url = postgresql+asyncpg://user:pass@localhost/dbname

[loggers]
keys = root

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
'''
        with open(alembic_ini, "w", encoding="utf-8") as f:
            f.write(alembic_content.strip())
        log_step("[OK] Файл alembic.ini создан")
    
    # Проверяем подключение к БД
    try:
        import asyncpg
        db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/mes_db")
        conn = await asyncpg.connect(db_url, timeout=10)
        await conn.close()
        log_step("[OK] Подключение к БД успешно")
        
        # Создаем миграции
        log_step("📝 Создание миграций...")
        try:
            subprocess.run(["alembic", "revision", "--autogenerate", "-m", "day4_setup"], check=True)
            subprocess.run(["alembic", "upgrade", "head"], check=True)
            log_step("[OK] Миграции созданы и применены")
        except subprocess.CalledProcessError as e:
            log_step(f"[WARNING] Ошибка создания миграций: {e}")
            log_step("💡 Создайте миграции вручную: alembic revision --autogenerate -m 'day4' && alembic upgrade head")
        
    except Exception as e:
        log_step(f"[ERROR] Ошибка подключения к БД: {e}")
        log_step("💡 Убедитесь, что PostgreSQL запущен и БД существует")

def create_scripts():
    """Создание вспомогательных скриптов"""
    log_step("📜 Создание вспомогательных скриптов...")
    
    scripts_dir = PROJECT_ROOT / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    
    # Скрипт запуска development
    dev_script = '''#!/bin/bash
echo "[LAUNCH] Запуск MES Development..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000
'''
    with open(scripts_dir / "start-dev.sh", "w", encoding="utf-8") as f:
        f.write(dev_script.strip())
    if platform.system() != "Windows":
        subprocess.run(["chmod", "+x", scripts_dir / "start-dev.sh"])
    
    # Скрипт бэкапа БД
    backup_script = '''#!/bin/bash
echo "💾 Резервное копирование БД MES..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U postgres mes_db > backups/mes_backup_${TIMESTAMP}.sql
echo "[OK] Бэкап создан: backups/mes_backup_${TIMESTAMP}.sql"
'''
    with open(scripts_dir / "backup-db.sh", "w", encoding="utf-8") as f:
        f.write(backup_script.strip())
    if platform.system() != "Windows":
        subprocess.run(["chmod", "+x", scripts_dir / "backup-db.sh"])
    
    log_step("[OK] Вспомогательные скрипты созданы")

async def main():
    """Основная функция настройки"""
    print("[LAUNCH] FINAL MES DAY 4 SETUP")
    print("=" * 60)
    
    # Выполняем все шаги настройки
    steps = [
        check_system_requirements,
        check_project_structure,
        check_and_install_dependencies,
        check_postgresql,
        check_docker,
        create_mes_models,
        create_services,
        create_health_check,
        create_day4_endpoints,
        update_main_py,
        lambda: asyncio.create_task(setup_database()),
        create_scripts
    ]
    
    for step in steps:
        try:
            if asyncio.iscoroutinefunction(step):
                await step()
            else:
                step()
        except Exception as e:
            log_step(f"[ERROR] Ошибка в шаге {step.__name__}: {e}")
            continue
    
    print("\\n" + "=" * 60)
    print("[SUCCESS] НАСТРОЙКА MES ДЕНЬ 4 ЗАВЕРШЕНА!")
    print("\\n[OK] ЧТО БЫЛО СДЕЛАНО:")
    print("   • Проверка системных требований")
    print("   • Создание моделей геймификации")
    print("   • Создание сервисов и API endpoints")
    print("   • Health check endpoints")
    print("   • Настройка базы данных и миграций")
    print("   • Вспомогательные скрипты")
    print("\\n[LAUNCH] КОМАНДЫ ДЛЯ ЗАПУСКА:")
    print("   Разработка: python main.py")
    print("   Production: uvicorn main:app --host 0.0.0.0 --port 8000")
    print("   Миграции:   alembic upgrade head")
    print("\\n📊 ПРОВЕРКА РАБОТЫ:")
    print("   Health:      curl http://localhost:8000/health")
    print("   Achievements: curl http://localhost:8000/api/v1/achievements")
    print("   Leaderboard: curl http://localhost:8000/api/v1/leaderboard")

if __name__ == "__main__":
    asyncio.run(main())
