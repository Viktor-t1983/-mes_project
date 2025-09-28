from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.core.database import get_db
from src.models.project import Project

router = APIRouter()

@router.get("/projects")
async def get_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return projects

@router.post("/projects")
async def create_project(name: str, description: str, db: AsyncSession = Depends(get_db)):
    project = Project(name=name, description=description)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project
