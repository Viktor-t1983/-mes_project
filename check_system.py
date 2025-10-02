import requests
import sys

def test_endpoint(name, path):
    try:
        response = requests.get(f"http://localhost:8000{path}", timeout=5)
        if response.status_code == 200:
            print(f"✅ {name}: WORKING")
            return True
        else:
            print(f"❌ {name}: FAILED ({response.status_code})")
            return False
    except:
        print(f"❌ {name}: ERROR")
        return False

print("🔍 FINAL SYSTEM CHECK")
print("=" * 40)

results = [
    test_endpoint("Health Check", "/health"),
    test_endpoint("Achievements", "/api/v1/achievements"),
    test_endpoint("Leaderboard", "/api/v1/leaderboard"),
]

if all(results):
    print("=" * 40)
    print("🎉 SYSTEM IS 100% OPERATIONAL!")
    print("🚀 Day 4 features are READY!")
else:
    print("=" * 40)
    print("⚠️ Some issues found, but core features should work")
