
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.db_connection import get_db
from service import team_service
from payload.user_payload import TeamRequest
from loguru import logger

router = APIRouter()


@router.post("/teams/", status_code=status.HTTP_201_CREATED)
def create_team(team: TeamRequest, db: Session = Depends(get_db)):
    logger.info(f"Creating team with name: {team.name}")
    db_team = team_service.create_team(db, team.name, team.project_ids)
    logger.info(f"Team created with ID: {db_team.id}")
    return db_team

