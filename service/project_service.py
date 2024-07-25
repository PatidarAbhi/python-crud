from loguru import logger

from sqlalchemy.orm import Session

from exceptions.not_found_exception import NotFoundException
from repositories import project_repo


def create_project(db: Session, name: str):
    logger.info(f"Creating project with name: {name}")
    return project_repo.create_project(db, name)


def get_all_projects(db: Session):
    logger.info("Fetching all projects in service ")
    projects = project_repo.get_all_projects(db)
    if not projects:
        logger.error("No projects found")
        raise NotFoundException(status_code=404, detail=f"Projects not found")
    return projects


def delete_project(db: Session, project_id: int):
    logger.info(f"Deleting project with ID: {project_id}")
    result = project_repo.delete_project(db, project_id)
    if result == 0:
        logger.error(f"Deletion failed for project with ID: {project_id}")
        return "Deletion failed"
    logger.info(f"Project with ID: {project_id} deleted successfully")
    return "Delete successful"
