import requests
import sys

def quick_test():
    print("🔍 Быстрая проверка MES Day 4")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    endpoints = [
        ("/", "Системный статус"),
        ("/api/v1/health", "Health Check"),
        ("/api/v1/achievements", "Достижения"),
        ("/api/v1/leaderboard", "Рейтинг"),
    ]
    
    all_ok = True
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=3)
            if response.status_code == 200:
                print(f"✅ {name}: РАБОТАЕТ")
            else:
                print(f"❌ {name}: ОШИБКА {response.status_code}")
                all_ok = False
        except:
            print(f"❌ {name}: НЕДОСТУПЕН")
            all_ok = False
    
    print("=" * 40)
    if all_ok:
        print("🎉 ВСЕ СИСТЕМЫ РАБОТАЮТ НОРМАЛЬНО!")
        print("🚀 MES Day 4 операционален!")
    else:
        print("⚠️ Есть проблемы с некоторыми сервисами")
    
    return all_ok

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
