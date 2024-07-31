from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database.db_connection import get_db
from exceptions.deletion_failed_exception import DeletionFailedException
from exceptions.not_found_exception import NotFoundException
from models import User
from service import user_service
from payload.user_payload import UserResponse, UserRequest, UsersNameResponse
from loguru import logger

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating user with username: {user.username}")
        db_user = user_service.create_user(db, user.username, user.password)
        logger.success(f"User created with ID: {db_user.id}")
        return db_user
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"API call to fetch user with ID: {user_id}")
        db_user = user_service.get_user(db, user_id)
        return db_user
    except NotFoundException as nf:
        logger.error(f"NotFoundException: {nf}")
        raise nf
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/", status_code=status.HTTP_200_OK)
def read_users(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all users")
        db_users = user_service.get_users(db)
        logger.info(f"Number of users retrieved: {len(db_users)}")
        return db_users
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/users_name/{username}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_by_name(username: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching user with username: {username}")
        db_user = user_service.get_by_name(db, username)
        logger.info(f"User found: {db_user.username}")
        return db_user
    except NotFoundException as nf:
        logger.error(f"NotFoundException: {nf}")
        raise nf
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/all_name/users_name", status_code=status.HTTP_200_OK, response_model=list[UsersNameResponse])
def get_all_user_names(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all users' names")
        users_names = user_service.get_users_name(db)
        logger.info(f"Number of users' names retrieved: {len(users_names)}")
        return users_names
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting user with ID: {user_id}")
        result = user_service.delete_user(db, user_id)
        logger.info(f"User with ID: {user_id} deleted successfully")
        return result
    except NotFoundException as nf:
        logger.error(f"NotFoundException: {nf}")
        raise nf
    except DeletionFailedException as df:
        logger.error(f"DeletionFailedException: {df}")
        raise df
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user: UserRequest, user_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"updating use with id {user_id}")
        return user_service.update_user(db, user_id, user)
    except NotFoundException as nf:
        logger.error(f"NotFoundException: {nf}")
        raise nf
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
