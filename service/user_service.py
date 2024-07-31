from sqlalchemy.orm import Session

from exceptions.deletion_failed_exception import DeletionFailedException
from exceptions.not_found_exception import NotFoundException
from payload.user_payload import UserRequest
from repositories import user_repo
from loguru import logger


def get_user(db: Session, user_id: int):
    logger.info(f"Fetching user with ID: {user_id}")
    db_user = user_repo.get_user(db, user_id)
    if db_user is None:
        logger.error(f"User not found with ID: {user_id}")
        raise NotFoundException(status_code=404, detail=f"User not found with id : {user_id}")
    logger.info(f"User found with ID: {user_id}: {db_user.username}")
    return db_user


def get_users(db: Session):
    logger.info("Fetching all users")
    db_users = user_repo.get_users(db)
    return db_users


def create_user(db: Session, username: str, hashed_password: str):
    try:
        logger.info(f"Creating user with username: {username}")
        user = user_repo.create_user(db, username, hashed_password)
        return user
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        db.rollback()
        raise ex


def get_by_name(db: Session, username: str):
    logger.info(f"Fetching user with username: {username}")
    db_user = user_repo.get_by_name(db, username)
    if not db_user:
        logger.error(f"User not found with username: {username}")
        raise NotFoundException(status_code=404, detail=f"User not found with name : {username}")
    return db_user


def get_users_name(db: Session):
    logger.info("Fetching all users in service ' names")
    db_user = user_repo.get_all_users_name(db)
    return db_user


def delete_user(db: Session, user_id: int):
    try:
        logger.info(f"Deleting user with ID: {user_id}")
        get_user(db, user_id)
        result = user_repo.delete_user(db, user_id)
        if result == 0:
            logger.error(f"Deletion failed for user with ID: {user_id}")
            raise DeletionFailedException(status_code=500, detail=f"Failed to delete user with ID: {user_id}")
        logger.info(f"User with ID: {user_id} deleted successfully")
        return "Delete successful"
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        db.rollback()
        raise ex


def update_user(db: Session, user_id: int, user: UserRequest):
    try:
        logger.info(f"Updating use with id {user_id}")
        existing_user = get_user(db, user_id)
        existing_user.username = user.username
        existing_user.hashed_password = user.password
        updated_user = user_repo.update_user(db, existing_user)
        logger.info(f"Existing user after update {updated_user.username}")
        return updated_user
    except NotFoundException as nf:
        logger.error(f"NotFoundException exception occurred: {nf}")
        db.rollback()
        raise nf
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        db.rollback()
        raise ex
