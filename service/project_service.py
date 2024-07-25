from loguru import logger

from sqlalchemy.orm import Session
from repositories import project_repo


def create_project(db: Session, name: str):
    logger.info(f"Creating project with name: {name}")
    return project_repo.create_project(db, name)