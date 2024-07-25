
from typing import List

from sqlalchemy.orm import Session
from repositories import team_repo
from loguru import logger


def create_team(db: Session, name: str, project_ids: List[int]):
    logger.info(f"Creating team with name in service: {name}")
    return team_repo.create_team(db, name, project_ids)
