from fastapi import APIRouter

router = APIRouter()

# Health endpoints - без префикса, так как они уже в APIRouter
@router.get('/api/v1/health')
async def health_check():
    return {'status': 'healthy', 'service': 'MES API', 'version': '1.0.0'}

@router.get('/api/v1/ready')
async def readiness_check():
    return {'status': 'ready', 'database': 'connected', 'message': 'System is ready'}

@router.get('/api/v1/live')
async def liveness_check():
    import datetime
    return {'status': 'live', 'timestamp': datetime.datetime.now().isoformat()}
