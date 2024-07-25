from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.db_connection import get_db
from service import passport_service
from payload.user_payload import PassportRequest
from loguru import logger

router = APIRouter()


@router.post("/passports/", status_code=status.HTTP_201_CREATED)
def create_passport(passport: PassportRequest, db: Session = Depends(get_db)):
    logger.info(f"Creating passport with passport id : {passport.person_id}")
    created_passport = passport_service.create_passport(db, passport.passport_number, passport.person_id)
    logger.info(f"Passport created with ID: {created_passport.id}")
    return created_passport


@router.get("/passports/", status_code=status.HTTP_200_OK)
def get_all_passports(db: Session = Depends(get_db)):
    logger.info("Fetching all passports")
    passports = passport_service.get_all_passports(db)
    logger.info(f"Number of passports retrieve: {len(passports)}")
    return passports
