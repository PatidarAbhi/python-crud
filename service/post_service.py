from sqlalchemy.orm import Session

from exceptions.deletion_failed_exception import DeletionFailedException
from exceptions.not_found_exception import NotFoundException
from payload.user_payload import PostBase, UpdatePostPayload
from repositories import post_repo, user_repo
from loguru import logger


def create_post(db: Session, post: PostBase):
    try:
        logger.info(f"Creating post with title {post.title}")
        return post_repo.create_post(db, post)
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        db.rollback()
        raise ex


def get_all_post(db: Session):
    logger.info("Fetching all post")
    db_posts = post_repo.get_all_post(db)
    logger.info("Returning post")
    return db_posts


def get_post_by_id(db: Session, post_id: int):
    logger.info(f"Fetching post with ID: {post_id}")
    db_post = post_repo.get_post_by_id(db, post_id)
    if db_post is None:
        logger.error(f"Post not found with ID: {post_id}")
        raise NotFoundException(status_code=404, detail=f"Post not found with id : {post_id}")
    logger.info(f"Post found with ID: {post_id}: {db_post.title}")
    return db_post


def delete_post(db: Session, post_id: int):
    try:
        logger.info(f"Deleting post with ID: {post_id}")
        get_post_by_id(db, post_id)
        result = post_repo.delete_post(db, post_id)
        if result == 0:
            logger.error(f"Deletion failed for post with ID: {post_id}")
            raise DeletionFailedException(status_code=500, detail=f"Failed to delete post with ID: {post_id}")
        logger.info(f"Post with ID: {post_id} deleted successfully")
        return "Delete successful"
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        db.rollback()
        raise ex


def update_post(db: Session, post_id: int, post: UpdatePostPayload):
    try:
        logger.info(f"Updating post with id {post_id}")
        existing_post = get_post_by_id(db, post_id)
        existing_post.title = post.title
        existing_post.content = post.content
        updated_post = post_repo.update_post(db, existing_post)
        logger.info(f"Existing post after update {updated_post.title}")
        return updated_post
    except NotFoundException as nf:
        logger.error(f"NotFoundException exception occurred: {nf}")
        db.rollback()
        raise nf
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        db.rollback()
        raise ex
