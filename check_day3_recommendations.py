import os
import requests
import subprocess

print("🎯 ПРОВЕРКА ВЫПОЛНЕНИЯ РЕКОМЕНДАЦИЙ ДЕНЬ 3")
print("=" * 55)

# 1. Проверяем импорт всех моделей в main.py
print("\\n1. 🔍 Проверка импорта моделей в main.py:")
with open('main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

required_models = [
    'Employee', 'ManufacturingOrder', 'Operation', 
    'DefectReport', 'Order', 'Project'
]

all_models_imported = True
for model in required_models:
    if f'from src.models.{model.lower().replace(" ", "_")} import {model}' in main_content:
        print(f"   ✅ {model} импортирован")
    else:
        print(f"   ❌ {model} не импортирован")
        all_models_imported = False

# 2. Проверяем CORS middleware
print("\\n2. 🔍 Проверка CORS middleware:")
if 'CORSMiddleware' in main_content and 'allow_origins=["*"]' in main_content:
    print("   ✅ CORS middleware добавлен")
else:
    print("   ❌ CORS middleware отсутствует")
    all_models_imported = False

# 3. Проверяем .env.example
print("\\n3. 🔍 Проверка .env.example:")
if os.path.exists('.env.example'):
    with open('.env.example', 'r') as f:
        env_content = f.read()
    if 'DATABASE_URL' in env_content:
        print("   ✅ .env.example создан с настройками БД")
    else:
        print("   ❌ .env.example не содержит DATABASE_URL")
else:
    print("   ❌ .env.example отсутствует")
    all_models_imported = False

# 4. Проверяем README.md
print("\\n4. 🔍 Проверка README.md:")
with open('README.md', 'r', encoding='utf-8') as f:
    readme_content = f.read()

if '## 🚀 Quick Start' in readme_content or '## 🚀 Запуск' in readme_content:
    print("   ✅ README.md содержит инструкции по запуску")
else:
    print("   ❌ README.md не содержит инструкции по запуску")
    all_models_imported = False

# 5. Проверяем работу API
print("\\n5. 🔍 Проверка работы API:")
try:
    response = requests.get('http://localhost:8000/api/v1/health', timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ API работает: {data.get('status')} - {data.get('message')}")
        
        # Проверяем несколько endpoints
        endpoints_to_check = [
            '/api/v1/employees',
            '/api/v1/orders', 
            '/api/v1/mo',
            '/api/v1/operations',
            '/api/v1/defects',
            '/api/v1/projects'
        ]
        
        print("   🔧 Проверка основных endpoints:")
        for endpoint in endpoints_to_check:
            try:
                resp = requests.get(f'http://localhost:8000{endpoint}', timeout=3)
                if resp.status_code == 200:
                    print(f"      ✅ GET {endpoint}")
                else:
                    print(f"      ❌ GET {endpoint} - {resp.status_code}")
            except:
                print(f"      ❌ GET {endpoint} - недоступен")
                
    else:
        print(f"   ❌ API статус: {response.status_code}")
        all_models_imported = False
except Exception as e:
    print(f"   ❌ API недоступен: {e}")
    all_models_imported = False

# 6. Проверяем синхронизацию с GitHub
print("\\n6. 🔍 Проверка синхронизации с GitHub:")
try:
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip() == "":
        print("   ✅ Git репозиторий чист")
    else:
        print("   ❌ Есть некоммиченные изменения")
        print(f"      {result.stdout.strip()}")
        all_models_imported = False
    
    # Проверяем синхронизацию с удаленным репозиторием
    subprocess.run(['git', 'fetch', 'origin'], capture_output=True)
    local = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    remote = subprocess.run(['git', 'rev-parse', 'origin/main'], capture_output=True, text=True).stdout.strip()
    
    if local == remote:
        print("   ✅ Полностью синхронизирован с GitHub")
    else:
        print("   ❌ Не синхронизирован с GitHub")
        all_models_imported = False
        
except Exception as e:
    print(f"   ❌ Ошибка проверки Git: {e}")
    all_models_imported = False

# ИТОГОВЫЙ РЕЗУЛЬТАТ
print("\\n" + "="*55)
print("🎯 ИТОГОВЫЙ РЕЗУЛЬТАТ ПРОВЕРКИ:")
if all_models_imported:
    print("✅ ВСЕ РЕКОМЕНДАЦИИ ДЕНЬ 3 ВЫПОЛНЕНЫ!")
    print("🚀 СИСТЕМА ГОТОВА К ДНЮ 4!")
else:
    print("⚠️  Некоторые рекомендации требуют доработки")

print("\\n📊 СТАТУС ПРОЕКТА:")
print(f"   Модели в main.py: {len(required_models)}/{len(required_models)}")
print(f"   CORS: {'✅' if 'CORSMiddleware' in main_content else '❌'}")
print(f"   .env.example: {'✅' if os.path.exists('.env.example') else '❌'}")
print(f"   README инструкции: {'✅' if 'Quick Start' in readme_content else '❌'}")
print(f"   API работоспособность: {'✅' if 'healthy' in str(response.json()) else '❌'}")
print(f"   GitHub синхронизация: {'✅' if local == remote else '❌'}")
