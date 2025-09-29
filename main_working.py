from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.core.database import engine, get_db
from src.models.base import Base
from src.models.project import Project
from src.models.operation import Operation

app = FastAPI(
    title="MES-X v4.0 Working",
    description="Система управления производством - рабочая версия",
    version="0.1.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def root():
    return {"message": "Добро пожаловать в MES-X v4.0!"}

@app.get("/health")
def health():
    return {"status": "OK"}

# Рабочие эндпоинты
@app.post("/api/v1/projects")
async def create_project(name: str, description: str, db: AsyncSession = Depends(get_db)):
    project = Project(name=name, description=description)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return {"id": project.id, "name": project.name, "description": project.description}

@app.get("/api/v1/projects")
async def get_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return [{"id": p.id, "name": p.name, "description": p.description} for p in projects]

@app.post("/api/v1/operations")
async def create_operation(name: str, description: str, db: AsyncSession = Depends(get_db)):
    operation = Operation(name=name, description=description)
    db.add(operation)
    await db.commit()
    await db.refresh(operation)
    return {"id": operation.id, "name": operation.name, "description": operation.description}

@app.get("/api/v1/operations")
async def get_operations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Operation))
    operations = result.scalars().all()
    return [{"id": o.id, "name": o.name, "description": o.description} for o in operations]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
