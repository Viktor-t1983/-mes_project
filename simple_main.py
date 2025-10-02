from fastapi import FastAPI
from src.core.database import engine, Base
from src.api.health import router as health_router
from src.api.day4_endpoints import router as day4_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MES System", version="1.0.0")

app.include_router(health_router, tags=["Health"])
app.include_router(day4_router, prefix="/api/v1", tags=["Day 4 - Gamification"])

@app.get("/")
async def root():
    return {"message": "MES System API - Day 4 Ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
