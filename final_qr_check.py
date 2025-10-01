import requests

BASE_URL = "http://localhost:8000"

def final_check():
    print("🎯 ФИНАЛЬНАЯ ПРОВЕРКА QR-КОДОВ")
    print("=" * 50)
    
    success_count = 0
    total_tests = 3
    
    for entity in ['order', 'employee', 'mo']:
        try:
            response = requests.get(f"{BASE_URL}/api/v1/qr/{entity}/1")
            if response.status_code == 200:
                print(f"✅ {entity}: РАБОТАЕТ - {response.json()['qr_data']}")
                success_count += 1
            else:
                print(f"❌ {entity}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"💥 {entity}: {e}")
    
    print("\\n" + "=" * 50)
    print(f"📊 РЕЗУЛЬТАТ: {success_count}/{total_tests} эндпоинтов работают")
    
    if success_count == total_tests:
        print("🎉 ВСЕ QR-КОДЫ РАБОТАЮТ!")
        print("🚀 СИСТЕМА СООТВЕТСТВУЕТ 'ДЕНЬ 3'!")
    else:
        print("⚠️  Есть проблемы с QR-кодами")

if __name__ == "__main__":
    final_check()
