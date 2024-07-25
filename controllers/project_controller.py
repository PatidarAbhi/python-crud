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


@router.get("/projects/", status_code=status.HTTP_200_OK)
def get_all_projects(db: Session = Depends(get_db)):
    logger.info(f"Fetching all projects in controller")
    projects = project_service.get_all_projects(db)
    logger.info(f"Number of projects retrieved: {len(projects)}")
    return projects


@router.delete("/projects/{project_id}", status_code=status.HTTP_200_OK)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting project with ID: {project_id}")
    result = project_service.delete_project(db, project_id)
    logger.info(f"Project with ID: {project_id} deleted successfully")
    return result
