
from sqlalchemy.orm import Session

from exceptions.not_found_exception import NotFoundException
from repositories import person_repo
from loguru import logger


def create_person(db: Session, name: str):
    logger.info(f"Creating person with name in service: {name}")
    return person_repo.create_person(db, name)


def get_all_persons(db: Session):
    logger.info("Fetching all persons")
    persons = person_repo.get_all_persons(db)
    return persons



