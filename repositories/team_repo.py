from loguru import logger
from typing import List

from sqlalchemy.orm import Session, joinedload

from models import Team, Project


def create_team(db: Session, name: str, project_ids: List[int]):
    db_team = Team(name=name)
    if project_ids:
        logger.info(f"Project ids in create team: {project_ids}")
        projects = db.query(Project).filter(Project.id.in_(project_ids)).all()
        db_team.projects.extend(projects)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_all_teams(db: Session):
    return db.query(Team).options(joinedload(Team.projects)).all()
