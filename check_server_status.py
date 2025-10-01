import requests
import time

def check_server():
    print("🔍 ПРОВЕРКА СТАТУСА СЕРВЕРА")
    print("=" * 40)
    
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/api/v1/health", timeout=2)
            if response.status_code == 200:
                print("✅ Сервер запущен и отвечает!")
                return True
        except:
            if i < max_retries - 1:
                print(f"⏳ Ожидание запуска сервера... ({i+1}/{max_retries})")
                time.sleep(2)
            else:
                print("❌ Сервер не запущен после ожидания")
                return False
    
    return False

if __name__ == "__main__":
    if check_server():
        print("\n🌐 Сервер доступен по: http://localhost:8000")
        print("📖 Документация: http://localhost:8000/docs")
    else:
        print("\n🚨 Сервер не запущен! Вернитесь в Терминал 1 и запустите:")
        print("   uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
