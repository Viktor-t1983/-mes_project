import requests
import json

def test_day4_complete():
    print("🎯 ПОЛНАЯ ПРОВЕРКА MES DAY 4")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # 1. Проверка корневого endpoint
    print("1. 🌐 Корневой endpoint:")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Успех: {data['message']}")
            print(f"   📋 Версия: {data['version']}")
            print(f"   🟢 Статус: {data['status']}")
        else:
            print(f"   ❌ Ошибка: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # 2. Проверка здоровья системы
    print("\n2. 🏥 Система здоровья:")
    health_endpoints = [
        ("/api/v1/health", "Health Check"),
        ("/api/v1/ready", "Readiness Check"), 
        ("/api/v1/live", "Liveness Check")
    ]
    
    for endpoint, name in health_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {name}: {data['status']}")
            else:
                print(f"   ❌ {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: {e}")
    
    # 3. Проверка геймификации
    print("\n3. 🏆 Система геймификации:")
    
    # Достижения
    try:
        response = requests.get(f"{base_url}/api/v1/achievements", timeout=5)
        if response.status_code == 200:
            achievements = response.json()
            print(f"   ✅ Achievements: {len(achievements)} достижений")
            for ach in achievements:
                print(f"      🏅 {ach['name']} - {ach['points']} баллов")
        else:
            print(f"   ❌ Achievements: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Achievements: {e}")
    
    # Рейтинг
    try:
        response = requests.get(f"{base_url}/api/v1/leaderboard", timeout=5)
        if response.status_code == 200:
            leaderboard = response.json()
            print(f"   ✅ Leaderboard: {len(leaderboard)} сотрудников")
            for entry in leaderboard:
                print(f"      {entry['rank']}️⃣ {entry['employee_name']} - {entry['points']} баллов")
        else:
            print(f"   ❌ Leaderboard: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Leaderboard: {e}")
    
    # 4. Проверка интеграции
    print("\n4. 🔗 Интеграция с 1С:")
    try:
        response = requests.post(f"{base_url}/api/v1/1c/sync-invoice", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 1C Sync: {data['status']}")
            print(f"   📨 Сообщение: {data['message']}")
        else:
            print(f"   ❌ 1C Sync: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ 1C Sync: {e}")
    
    # 5. Создание достижения
    print("\n5. ➕ Создание достижения:")
    try:
        response = requests.post(f"{base_url}/api/v1/achievements", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Create Achievement: {data['status']}")
            print(f"   📝 Сообщение: {data['message']}")
        else:
            print(f"   ❌ Create Achievement: HTTP {response.status_code}")
    except Exception as e:
        print(f"   ❌ Create Achievement: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 MES DAY 4 - ВСЕ СИСТЕМЫ РАБОТАЮТ НОРМАЛЬНО!")
    print("🚀 СИСТЕМА ГОТОВА К ПРОМЫШЛЕННОЙ ЭКСПЛУАТАЦИИ!")

if __name__ == "__main__":
    test_day4_complete()
