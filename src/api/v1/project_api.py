from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.database import get_db
from src.models.project import Project as ProjectModel
from src.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    # Проверка дубликата
    existing = await db.execute(select(ProjectModel).where(ProjectModel.name == project.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    
    # Создание проекта — ИСПОЛЬЗУЕМ model_dump()
    db_project = ProjectModel(**project.model_dump())
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)  # ← Загружает id, created_at и т.д.
    return db_project
