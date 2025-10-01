import requests
BASE_URL = "http://localhost:8000"

# Тест полного производственного цикла
print("🏭 ТЕСТ ПОЛНОГО ПРОИЗВОДСТВЕННОГО ЦИКЛА")

# 1. Создаем заказ
order = requests.post(f"{BASE_URL}/api/v1/orders", params={
    "product_name": "Серийный продукт А",
    "quantity": 100
}).json()
print(f"📦 Заказ создан: {order}")

# 2. Создаем MO
mo = requests.post(f"{BASE_URL}/api/v1/mo", params={
    "order_number": "PROD-001",
    "product_name": "Серийный продукт А", 
    "product_code": "PROD-A",
    "quantity": 100
}).json()
print(f"🏭 MO создано: {mo}")

# 3. Создаем операцию
operation = requests.post(f"{BASE_URL}/api/v1/operations", params={
    "manufacturing_order_id": mo['id'],
    "operation_number": "OP-PROD-001",
    "name": "Основная сборка",
    "description": "Основная операция сборки продукта"
}).json()
print(f"⚙️ Операция создана: {operation}")

print("🎉 Производственный цикл готов к работе!")
