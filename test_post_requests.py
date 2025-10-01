import requests
import json

def test_post_endpoints():
    base_url = "http://localhost:8000/api/v1"
    
    print("🧪 ТЕСТИРОВАНИЕ POST ЗАПРОСОВ")
    print("=" * 40)
    
    test_data = [
        {
            "endpoint": "/employees",
            "data": {
                "qr_code": "EMP-TEST-001",
                "first_name": "Тестовый",
                "last_name": "Сотрудник",
                "role": "operator",
                "allowed_workcenters": ["wc1", "wc2"]
            }
        },
        {
            "endpoint": "/orders", 
            "data": {
                "project_id": 1,
                "name": "Тестовый заказ",
                "description": "Описание тестового заказа",
                "product_name": "Тестовый продукт",
                "quantity": 10,
                "status": "pending"
            }
        },
        {
            "endpoint": "/projects",
            "data": {
                "name": "Тестовый проект",
                "description": "Описание тестового проекта",
                "status": "active"
            }
        }
    ]
    
    for test in test_data:
        endpoint = test["endpoint"]
        data = test["data"]
        
        print(f"\\n📝 Создание записи через {endpoint}:")
        try:
            response = requests.post(f"{base_url}{endpoint}", json=data, timeout=10)
            
            if response.status_code == 200:
                print("✅ Успешно создано!")
                result = response.json()
                print(f"   📊 Ответ: {json.dumps(result, default=str, indent=2)}")
            elif response.status_code == 422:
                print("❌ Ошибка валидации 422")
                error_data = response.json()
                print(f"   🔍 Детали: {json.dumps(error_data, indent=2)}")
            else:
                print(f"⚠️  Статус: {response.status_code}")
                print(f"   🔍 Ответ: {response.text[:200]}")
                
        except Exception as e:
            print(f"🚫 Ошибка: {e}")

if __name__ == "__main__":
    test_post_endpoints()
