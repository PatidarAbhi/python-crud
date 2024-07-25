
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.db_connection import get_db
from service import user_service
from payload.user_payload import UserResponse, UserCreate, UsersNameResponse
from loguru import logger

router = APIRouter()


@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating user with username: {user.username}")
    db_user = user_service.create_user(db, user.username, user.password)
    logger.success(f"User created with ID: {db_user.id}")
    return db_user


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching user with ID: {user_id}")
    db_user = user_service.get_user(db, user_id)
    logger.info(f"User found: {db_user.username}")
    return db_user


@router.get("/users/", status_code=status.HTTP_200_OK)
def read_users(db: Session = Depends(get_db)):
    logger.info("Fetching all users")
    db_users = user_service.get_users(db)
    logger.info(f"Number of users retrieved: {len(db_users)}")
    return db_users


@router.get("/users_name/{username}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_by_name(username: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching user with username: {username}")
    db_user = user_service.get_by_name(db, username)
    logger.info(f"User found: {db_user.username}")
    return db_user


@router.get("/users_name/", status_code=status.HTTP_200_OK, response_model=list[UsersNameResponse])
def read_users(db: Session = Depends(get_db)):
    logger.info("Fetching all users' names")
    users_names = user_service.get_users_name(db)
    logger.info(f"Number of users' names retrieved: {len(users_names)}")
    return users_names


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting user with ID: {user_id}")
    result = user_service.delete_user(db, user_id)
    logger.info(f"User with ID: {user_id} deleted successfully")
    return result
