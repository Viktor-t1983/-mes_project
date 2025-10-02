import requests
import time
import os

def monitor_system():
    print("📊 МОНИТОРИНГ MES DAY 4 СИСТЕМЫ")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    check_count = 0
    
    while True:
        check_count += 1
        print(f"\n🔍 Проверка #{check_count} - {time.strftime('%H:%M:%S')}")
        print("-" * 30)
        
        # Проверяем основные endpoints
        endpoints = [
            ("/api/v1/health", "Health"),
            ("/api/v1/achievements", "Achievements"), 
            ("/api/v1/leaderboard", "Leaderboard")
        ]
        
        all_healthy = True
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=3)
                if response.status_code == 200:
                    print(f"✅ {name}: ONLINE")
                else:
                    print(f"❌ {name}: OFFLINE (HTTP {response.status_code})")
                    all_healthy = False
            except:
                print(f"❌ {name}: OFFLINE (Connection failed)")
                all_healthy = False
        
        if all_healthy:
            print("🟢 СИСТЕМА: НОРМА")
        else:
            print("🔴 СИСТЕМА: ПРОБЛЕМЫ")
        
        print("⏳ Следующая проверка через 10 секунд...")
        time.sleep(10)

if __name__ == "__main__":
    try:
        monitor_system()
    except KeyboardInterrupt:
        print("\n🛑 Мониторинг остановлен")
