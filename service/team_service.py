from typing import List

from sqlalchemy.orm import Session

from exceptions.not_found_exception import NotFoundException
from repositories import team_repo
from loguru import logger


def create_team(db: Session, name: str, project_ids: List[int]):
    logger.info(f"Creating team with name in service: {name}")
    return team_repo.create_team(db, name, project_ids)


def get_all_teams(db: Session):
    logger.info("Fetching all teams in service ")
    teams = team_repo.get_all_teams(db)
    if not teams:
        logger.error("No teams found")
        raise NotFoundException(status_code=404, detail=f"Teams not found")
    return teams
