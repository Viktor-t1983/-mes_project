import os

def verify_final_main():
    print("🔍 ПРОВЕРКА ФИНАЛЬНОГО main.py")
    print("=" * 50)
    
    with open('main_complete_final.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Размер файла: {len(content)} символов")
    
    # Ключевые POST эндпоинты которые должны быть
    required_post_endpoints = [
        "@app.post('/api/v1/employees'",
        "@app.post('/api/v1/orders'", 
        "@app.post('/api/v1/mo'",
        "@app.post('/api/v1/operations'",
        "@app.post('/api/v1/operations/start'",
        "@app.post('/api/v1/operations/pause'",
        "@app.post('/api/v1/operations/complete'",
        "@app.post('/api/v1/defects'",
        "@app.post('/api/v1/projects'"
    ]
    
    missing = []
    for endpoint in required_post_endpoints:
        if endpoint not in content:
            missing.append(endpoint)
    
    if not missing:
        print("✅ ВСЕ POST ЭНДПОИНТЫ ПРИСУТСТВУЮТ!")
        print("✅ Файл готов к использованию!")
        return True
    else:
        print("❌ Отсутствующие эндпоинты:")
        for item in missing:
            print(f"   - {item}")
        return False

if __name__ == "__main__":
    verify_final_main()
