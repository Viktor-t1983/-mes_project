from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.core.database import engine, get_db
from src.models.base import Base
from src.models.project import Project
from src.models.operation import Operation

app = FastAPI(title="MES-X Test API Fixed")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Простые эндпоинты без сложных схем
@app.post("/simple/projects")
async def create_simple_project(name: str, description: str, db: AsyncSession = Depends(get_db)):
    project = Project(name=name, description=description)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return {"id": project.id, "name": project.name, "description": project.description}

@app.get("/simple/projects")
async def get_simple_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return [{"id": p.id, "name": p.name, "description": p.description} for p in projects]

@app.post("/simple/operations")
async def create_simple_operation(
    name: str,
    description: str, 
    db: AsyncSession = Depends(get_db)
):
    # Используем только те поля, которые есть в модели Operation
    operation = Operation(
        name=name,
        description=description
        # Добавляем только существующие поля из модели
    )
    db.add(operation)
    await db.commit()
    await db.refresh(operation)
    return {"id": operation.id, "name": operation.name, "description": operation.description}

@app.get("/simple/operations")
async def get_simple_operations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Operation))
    operations = result.scalars().all()
    return [{"id": o.id, "name": o.name, "description": o.description} for o in operations]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
