#!/usr/bin/env python3
"""INDUSTRIAL-GRADE настройка MES системы для Дня 4 - промышленная надежность"""

import os
import sys
import shutil
import ast
import asyncio
import subprocess
from datetime import datetime

# === КОНФИГУРАЦИЯ ===
PROJECT_ROOT = "."

def write_file(path, content):
    """Записывает файл с контентом"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✅ Создан файл: {path}")

def check_docker_installed():
    """✅ ПРОВЕРКА НАЛИЧИЯ DOCKER ДЛЯ MES РАЗВЕРТЫВАНИЯ"""
    print("🐳 Проверка Docker...")
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        print(f"✅ {version}")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Docker не установлен. Пропускаем Docker-настройки")
        return False
    except Exception as e:
        print(f"⚠️  Ошибка проверки Docker: {e}")
        return False

def create_advanced_health_check():
    """✅ РАСШИРЕННЫЙ HEALTHCHECK С РЕАЛЬНОЙ ПРОВЕРКОЙ БД"""
    health_check_content = '''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database import get_db
import psutil
import os
from datetime import datetime

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    disk_usage = psutil.disk_usage("/")
    disk_free_gb = disk_usage.free / (1024**3)
    disk_status = "healthy" if disk_free_gb > 1.0 else "warning"
    
    memory = psutil.virtual_memory()
    memory_status = "healthy" if memory.percent < 90 else "warning"
    
    overall_status = "healthy" if db_status == "healthy" else "unhealthy"
    
    return {
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": db_status,
            "disk": disk_status,
            "memory": memory_status
        }
    }

@router.get("/ready")
async def readiness_check():
    return {"status": "ready"}

@router.get("/live")
async def liveness_check():
    return {"status": "live"}
'''
    write_file(os.path.join(PROJECT_ROOT, "src/api/health.py"), health_check_content)

def create_production_dockerfile():
    """✅ PRODUCTION DOCKERFILE С HEALTHCHECKS"""
    dockerfile_content = '''
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
'''
    write_file(os.path.join(PROJECT_ROOT, "Dockerfile"), dockerfile_content)

def create_docker_env_files():
    """✅ СОЗДАНИЕ .env ФАЙЛОВ ДЛЯ РАЗНЫХ СРЕД MES"""
    docker_env_content = '''
DATABASE_URL=postgresql+asyncpg://mes_user:mes_password@postgres:5432/mes_db
DEBUG=false
'''
    write_file(os.path.join(PROJECT_ROOT, ".env.docker"), docker_env_content)
    
    production_env_content = '''
DATABASE_URL=postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:5432/${DB_NAME}
DEBUG=false
'''
    write_file(os.path.join(PROJECT_ROOT, ".env.production.example"), production_env_content)

def create_deployment_scripts():
    """✅ СОЗДАНИЕ СКРИПТОВ РАЗВЕРТЫВАНИЯ ДЛЯ MES"""
    scripts_dir = os.path.join(PROJECT_ROOT, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)
    
    dev_script = '''#!/bin/bash
echo "🚀 Starting MES Development..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi
docker-compose -f docker-compose.dev.yml up --build
'''
    write_file(os.path.join(scripts_dir, "start-dev.sh"), dev_script)
    subprocess.run(["chmod", "+x", os.path.join(scripts_dir, "start-dev.sh")], shell=True)
    
    prod_script = '''#!/bin/bash
echo "🚀 Deploying MES to Production..."
docker build -t mes-app:latest .
docker run -d --name mes-production -p 8000:8000 --env-file .env.production mes-app:latest
echo "✅ MES Production deployed"
'''
    write_file(os.path.join(scripts_dir, "start-prod.sh"), prod_script)
    subprocess.run(["chmod", "+x", os.path.join(scripts_dir, "start-prod.sh")], shell=True)

def create_docker_compose_dev():
    """✅ СОЗДАНИЕ DOCKER-COMPOSE ДЛЯ MES РАЗРАБОТКИ"""
    compose_content = '''
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: mes_db
      POSTGRES_USER: mes_user
      POSTGRES_PASSWORD: mes_password
    ports: ["5432:5432"]
    volumes: ["postgres_data:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mes_user -d mes_db"]
      interval: 5s; timeout: 5s; retries: 5
  app:
    build: .
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql+asyncpg://mes_user:mes_password@postgres:5432/mes_db
    volumes: [".:/app"]
    depends_on:
      postgres:
        condition: service_healthy
    command: sh -c "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
volumes:
  postgres_data:
'''
    write_file(os.path.join(PROJECT_ROOT, "docker-compose.dev.yml"), compose_content)

def update_main_with_healthcheck():
    """✅ ДОБАВЛЕНИЕ HEALTHCHECK ROUTER В MAIN.PY"""
    main_path = os.path.join(PROJECT_ROOT, "main.py")
    try:
        with open(main_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Добавляем импорт
        if "from src.api.health import router as health_router" not in content:
            content = content.replace(
                "from src.api.routes import router as api_router",
                "from src.api.routes import router as api_router\nfrom src.api.health import router as health_router"
            )
        
        # Добавляем роутер
        if "app.include_router(health_router)" not in content:
            content = content.replace(
                "app.include_router(api_router, prefix=\"/api/v1\")",
                "app.include_router(api_router, prefix=\"/api/v1\")\napp.include_router(health_router)"
            )
        
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Health router добавлен в main.py")
    except Exception as e:
        print(f"⚠️ Ошибка обновления main.py: {e}")

async def main():
    print("🏭 INDUSTRIAL-GRADE НАСТРОЙКА MES СИСТЕМЫ")
    print("=" * 70)
    
    docker_ok = check_docker_installed()
    create_advanced_health_check()
    create_production_dockerfile()
    create_docker_env_files()
    create_deployment_scripts()
    create_docker_compose_dev()
    update_main_with_healthcheck()
    
    print("\n🎉 INDUSTRIAL-GRADE MES СИСТЕМА ГОТОВА!")
    print("✅ Healthchecks, Docker, скрипты развертывания созданы")

if __name__ == "__main__":
    asyncio.run(main())
