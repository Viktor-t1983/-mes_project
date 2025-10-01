# MES System - Manufacturing Execution System

Полнофункциональная система управления производством, реализованная на FastAPI и PostgreSQL.

## 🚀 Возможности системы

- **Управление сотрудниками** с QR-кодами
- **Планирование производственных заданий**
- **Управление операциями** с workflow (start/complete)
- **Контроль качества** и отчеты о браке
- **Управление складскими запасами**
- **Автоматический расчет премий**

## 🏗️ Архитектура

```
MES System
├── 👥 Employees
├── 🏭 Manufacturing Orders
├── ⚙️ Operations
├── ⚠️ Defect Reports
├── 📦 Warehouse Items
└── 💰 Incentives
```

## 📚 Документация API

После запуска сервера документация доступна по адресу:
http://localhost:8001/docs

## ⚡ Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/Viktor-t1983/-mes_project.git
cd -mes_project

# Активировать виртуальное окружение
source venv/Scripts/activate

# Запустить сервер
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

## 🚀 Quick Start
1. Create database: `createdb mes_db`
2. Copy environment: `cp .env.example .env`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `uvicorn main:app --reload`
5. Open: http://localhost:8000/docs
