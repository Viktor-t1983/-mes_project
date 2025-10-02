from fastapi import FastAPI
import sys
import os

# Добавляем src в путь для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

app = FastAPI(
    title='MES System - Day 4',
    description='Manufacturing Execution System with Gamification',
    version='1.0.0'
)

# Импортируем и подключаем роутеры
try:
    from api.health import router as health_router
    app.include_router(health_router)
    print('✅ Health router connected')
except ImportError as e:
    print(f'❌ Health router error: {e}')

try:
    from api.day4_endpoints import router as day4_router
    app.include_router(day4_router)
    print('✅ Day4 router connected')
except ImportError as e:
    print(f'❌ Day4 router error: {e}')

@app.get('/')
async def root():
    return {
        'message': 'MES System API - Day 4 Fully Operational',
        'version': '1.0.0',
        'status': 'running'
    }

if __name__ == '__main__':
    import uvicorn
    print('🚀 Starting MES Day 4 Server on port 8000...')
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)
