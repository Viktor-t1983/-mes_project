from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.security import setup_security_middleware
from src.core.database import engine, Base
from src.api.health import router as health_router
from src.api.day4_endpoints import router as day4_router

app = FastAPI(
    title="MES System - Production",
    version="1.0.0"
)

setup_security_middleware(app)
Base.metadata.create_all(bind=engine)
app.include_router(health_router)
app.include_router(day4_router)

@app.get("/")
async def root():
    return {"message": "MES Production", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
