import requests
import inspect
from main import app

def list_all_endpoints():
    print("🔍 ВСЕ ЗАРЕГИСТРИРОВАННЫЕ ЭНДПОИНТЫ")
    print("=" * 50)
    
    for route in app.routes:
        methods = getattr(route, 'methods', None)
        path = getattr(route, 'path', None)
        if methods and path:
            print(f"{', '.join(methods)} {path}")

if __name__ == "__main__":
    list_all_endpoints()
