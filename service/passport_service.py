
from sqlalchemy.orm import Session

from exceptions.not_found_exception import NotFoundException
from repositories import passport_repo
from loguru import logger


def create_passport(db: Session, number: str, person_id: int ):
    logger.info(f"Creating passport with person id in service: {person_id}")
    return passport_repo.create_passport(db, number, person_id)


def get_all_passports(db: Session):
    logger.info("Fetching all passports")
    passports = passport_repo.get_all_passports(db)
    return passports





