from loguru import logger

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.db_connection import get_db
from service import project_service
from payload.user_payload import ProjectRequest

router = APIRouter()


@router.post("/projects/", status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectRequest, db: Session = Depends(get_db)):
    logger.info(f"Creating project with name: {project.name}")
    db_user = project_service.create_project(db, project.name)
    logger.info(f"Project created with ID: {db_user.id}")
    return db_user
