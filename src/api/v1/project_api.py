from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.database import get_db
from src.models.project import Project as ProjectModel
from src.schemas.project import ProjectCreate, Project  # ← Импортируем Project

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])

@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)  # ← Указываем response_model
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(ProjectModel).where(ProjectModel.name == project.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    
    db_project = ProjectModel(**project.model_dump())
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

@router.get("/", response_model=list[Project])
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectModel).where(ProjectModel.is_active == True))
    return result.scalars().all()
