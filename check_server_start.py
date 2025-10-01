import requests
import time
import sys

def check_server():
    print("⏳ Проверка запуска сервера...")
    
    for i in range(15):
        try:
            response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ Сервер запущен! Попытка {i+1}")
                print("📊 Ответ health check:", response.json())
                return True
        except requests.exceptions.ConnectionError:
            print(f"⏳ Ожидание... {i+1}/15")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️  Другая ошибка: {e}")
            time.sleep(2)
    
    print("❌ Сервер не запустился за 30 секунд")
    return False

if __name__ == "__main__":
    if check_server():
        print("\\n🎉 СЕРВЕР УСПЕШНО ЗАПУЩЕН!")
        print("📖 Документация: http://localhost:8000/docs")
        print("🔧 Тестируйте эндпоинты через Swagger UI")
    else:
        print("\\n⚠️  СЕРВЕР НЕ ЗАПУСТИЛСЯ")
        print("Проверьте ошибки в Терминале 1")
