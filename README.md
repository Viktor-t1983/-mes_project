# MES-X v4.0

Система управления производством для несерийного производства

## Технологии

- **FastAPI** - веб-фреймворк
- **PostgreSQL** - база данных
- **SQLAlchemy** - ORM
- **Pydantic** - валидация данных
- **Uvicorn** - ASGI сервер

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Viktor-t1983/-mes_project.git
cd -mes_project
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте базу данных PostgreSQL и создайте файл `.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mes_db
```

5. Запустите сервер:
```bash
uvicorn main:app --reload
```

6. Откройте документацию API: http://127.0.0.1:8000/docs

## API Endpoints

- `GET /` - Главная страница
- `GET /health` - Проверка здоровья
- `GET /api/v1/projects` - Список проектов
- `POST /api/v1/projects` - Создать проект
- `GET /api/v1/orders` - Список заказов
- `POST /api/v1/orders` - Создать заказ

## Структура проекта

```
src/
├── api/          # Маршруты API
├── core/         # Настройки базы данных
├── models/       # SQLAlchemy модели
└── schemas/      # Pydantic схемы
```
