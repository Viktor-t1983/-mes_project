import requests
import time

BASE_URL = "http://localhost:8000"

def quick_test():
    print("🧪 БЫСТРЫЙ ТЕСТ QR-КОДОВ")
    print("=" * 40)
    
    # Тестируем все три типа сущностей
    test_cases = [
        ('order', 1),
        ('employee', 1), 
        ('mo', 1)
    ]
    
    for entity, entity_id in test_cases:
        try:
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/api/v1/qr/{entity}/{entity_id}", timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {entity} {entity_id}: {response.status_code} ({response_time:.0f}ms)")
                print(f"   QR: {data['qr_data']}")
            else:
                print(f"❌ {entity} {entity_id}: {response.status_code} ({response_time:.0f}ms)")
                print(f"   Ошибка: {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"⏰ {entity} {entity_id}: Таймаут")
        except Exception as e:
            print(f"💥 {entity} {entity_id}: {e}")
    
    print("\\n" + "=" * 40)

if __name__ == "__main__":
    quick_test()
