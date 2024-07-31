from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database.db_connection import get_db
from exceptions.deletion_failed_exception import DeletionFailedException
from exceptions.not_found_exception import NotFoundException
from service import post_service
from payload.user_payload import PostResponse, PostBase, UpdatePostPayload
from loguru import logger

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostBase, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating post with title: {post.title}")
        db_post = post_service.create_post(db, post)
        logger.success(f"Post created with ID: {db_post.id}")
        return db_post
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_posts(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all posts")
        db_posts = post_service.get_all_post(db)
        logger.info(f"Number of posts retrieved: {len(db_posts)}")
        return db_posts
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/{post_id}", status_code=status.HTTP_200_OK)
def get_by_id(post_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"API call to fetch post with ID: {post_id}")
        post = post_service.get_post_by_id(db, post_id)
        return post
    except NotFoundException as nf:
        logger.error(f"NotFoundException: {nf}")
        raise nf
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting post with ID: {post_id}")
        result = post_service.delete_post(db, post_id)
        logger.info(f"Post with ID: {post_id} deleted successfully")
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


@router.put("/update/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post: UpdatePostPayload, post_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"updating post with id {post_id}")
        return post_service.update_post(db, post_id, post)
    except NotFoundException as nf:
        logger.error(f"NotFoundException: {nf}")
        raise nf
    except Exception as ex:
        logger.error(f"Unhandled exception occurred: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
