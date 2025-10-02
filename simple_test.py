import requests
import time

def test_endpoint(url, name, method='GET'):
    try:
        if method == 'POST':
            response = requests.post(url, timeout=5)
        else:
            response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ {name}: SUCCESS")
            data = response.json()
            
            if 'status' in data:
                print(f"   Status: {data['status']}")
            if 'message' in data:
                print(f"   Message: {data['message']}")
            if isinstance(data, list):
                print(f"   Found {len(data)} items")
                if data and 'name' in data[0]:
                    print(f"   First item: {data[0]['name']}")
            
            return True
        else:
            print(f"❌ {name}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name}: ERROR - {e}")
        return False

print("🚀 TESTING MES DAY 4 SYSTEM")
print("=" * 40)

base_url = "http://localhost:8000"

# Ждем сервер
print("⏳ Waiting for server...")
time.sleep(2)

# Тестируем endpoints
endpoints = [
    (f"{base_url}/", "Root"),
    (f"{base_url}/api/v1/health", "Health"),
    (f"{base_url}/api/v1/ready", "Ready"),
    (f"{base_url}/api/v1/live", "Live"),
    (f"{base_url}/api/v1/achievements", "Achievements"),
    (f"{base_url}/api/v1/leaderboard", "Leaderboard"),
]

results = []
for url, name in endpoints:
    results.append(test_endpoint(url, name))

# Тестируем POST endpoints
post_endpoints = [
    (f"{base_url}/api/v1/achievements", "Create Achievement", "POST"),
    (f"{base_url}/api/v1/1c/sync-invoice", "1C Sync", "POST"),
]

for url, name, method in post_endpoints:
    results.append(test_endpoint(url, name, method))

print("=" * 40)
success = sum(results)
total = len(results)
print(f"📊 RESULTS: {success}/{total} tests passed")

if success == total:
    print("🎉 ALL TESTS PASSED! MES DAY 4 IS OPERATIONAL!")
else:
    print("⚠️ Some tests failed, checking issues...")
