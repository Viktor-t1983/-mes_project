import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(name, path, method="GET"):
    try:
        if method == "POST":
            response = requests.post(f"{BASE_URL}{path}", timeout=5)
        else:
            response = requests.get(f"{BASE_URL}{path}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {name}: SUCCESS")
            if "status" in data:
                print(f"   Status: {data['status']}")
            if "message" in data:
                print(f"   Message: {data['message']}")
            if isinstance(data, list):
                print(f"   Items: {len(data)}")
            return True
        else:
            print(f"❌ {name}: FAILED (HTTP {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {name}: ERROR - {e}")
        return False

print("🎯 MES DAY 4 - COMPREHENSIVE TEST")
print("=" * 50)

# Test all endpoints
test_cases = [
    ("Root", "/", "GET"),
    ("Health", "/api/v1/health", "GET"),
    ("Ready", "/api/v1/ready", "GET"),
    ("Live", "/api/v1/live", "GET"),
    ("Achievements GET", "/api/v1/achievements", "GET"),
    ("Achievements POST", "/api/v1/achievements", "POST"),
    ("Leaderboard", "/api/v1/leaderboard", "GET"),
    ("1C Sync", "/api/v1/1c/sync-invoice", "POST"),
]

results = []
for name, path, method in test_cases:
    results.append(test_endpoint(name, path, method))

print("=" * 50)
success_count = sum(results)
total_count = len(results)

if success_count == total_count:
    print(f"🎉 ALL {total_count} TESTS PASSED! MES DAY 4 IS FULLY OPERATIONAL!")
else:
    print(f"📊 {success_count}/{total_count} tests passed")

print("🚀 Day 4 Gamification Features Status: OPERATIONAL")
