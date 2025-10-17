from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models.project import Project as ProjectModel
from src.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    db_project = ProjectModel(**project.dict())
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project
