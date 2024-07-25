
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.db_connection import get_db
from service import person_service
from payload.user_payload import UserBase
from loguru import logger

router = APIRouter()


@router.post("/persons/", status_code=status.HTTP_201_CREATED)
def create_person(person: UserBase, db: Session = Depends(get_db)):
    logger.info(f"Creating person with name: {person.username}")
    person = person_service.create_person(db, person.username)
    logger.info(f"Person created with ID: {person.id}")
    return person


@router.get("/persons/", status_code=status.HTTP_200_OK)
def get_all_persons(db: Session = Depends(get_db)):
    logger.info("Fetching all persons")
    persons = person_service.get_all_persons(db)
    logger.info(f"Number of persons retrieved: {len(persons)}")
    return persons

