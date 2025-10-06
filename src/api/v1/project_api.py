from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.database import get_db
from src.models.project import Project as ProjectModel
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[str] = "planning"

class ProjectCreate(ProjectBase):
    pass

@router.post("/", response_model=ProjectBase, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    # Проверка дубликата
    existing = await db.execute(select(ProjectModel).where(ProjectModel.name == project.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    
    db_project = ProjectModel(**project.model_dump())
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

@router.get("/")
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectModel).where(ProjectModel.is_active == True))
    return result.scalars().all()
