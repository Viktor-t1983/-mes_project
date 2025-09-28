import requests
import json

# URL API
BASE_URL = "http://127.0.0.1:8000/api/v1"

# Создаем проект
project_data = {
    "name": "Проект из Python",
    "description": "Тест через Python requests",
    "status": "production"
}

response = requests.post(f"{BASE_URL}/projects", json=project_data)
print("Создан проект:", response.json())

# Получаем список проектов
response = requests.get(f"{BASE_URL}/projects")
print("Список проектов:", response.json())
