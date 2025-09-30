# MES-X API v4.0 - Итоги разработки

## ✅ Статус: РАБОЧЕЕ СОСТОЯНИЕ

Все API эндпоинты работают корректно. Данные создаются в PostgreSQL и возвращаются по запросам.

## 📊 Рабочие эндпоинты:

### POST запросы (создание):
- POST /api/v1/mo - создание производственного задания
- POST /api/v1/operations - создание операции
- POST /api/v1/orders - создание заказа
- POST /api/v1/projects - создание проекта
- POST /api/v1/employees - создание сотрудника
- POST /api/v1/defects - создание дефекта
- POST /api/v1/operations/start - запуск операции

### GET запросы (получение):
- GET /api/v1/mo - список производственных заданий
- GET /api/v1/operations - список операций
- GET /api/v1/orders - список заказов
- GET /api/v1/projects - список проектов
- GET /api/v1/employees - список сотрудников
- GET /api/v1/defects - список дефектов
- GET /api/v1/qr/order/{id} - QR код заказа

## 🚀 Запуск:
```bash
cd /d/Git/-mes_project
source venv/Scripts/activate
uvicorn main:app --reload --port 8000
```

## 📚 Документация:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
