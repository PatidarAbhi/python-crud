
from sqlalchemy.orm import Session

from exceptions.not_found_exception import NotFoundException
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
    if not db_users:
        logger.error("No users found")
        raise NotFoundException(status_code=404, detail=f"Users not found")
    return db_users


def create_user(db: Session, username: str, hashed_password: str):
    logger.info(f"Creating user with username: {username}")
    return user_repo.create_user(db, username, hashed_password)


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
    if not db_user:
        logger.error(f"User not found in service")
        raise NotFoundException(status_code=404, detail=f"Users not found ")
    return db_user


def delete_user(db: Session, user_id: int):
    logger.info(f"Deleting user with ID: {user_id}")
    get_user(db, user_id)
    result = user_repo.delete_user(db, user_id)
    if result == 0:
        logger.error(f"Deletion failed for user with ID: {user_id}")
        return "Deletion failed"
    logger.info(f"User with ID: {user_id} deleted successfully")
    return "Delete successful"
