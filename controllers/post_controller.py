from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.db_connection import get_db
from service import post_service
from payload.user_payload import PostResponse, PostBase


router = APIRouter()


@router.post("/posts/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostBase, db: Session = Depends(get_db)):
    db_post = post_service.create_post(db, post.title, post.content, post.owner_id)
    return db_post


#here we can get entity or also we can get custom response
@router.get("/posts/", status_code=status.HTTP_201_CREATED)
def get_all_posts(db: Session = Depends(get_db)):
    db_post = post_service.get_all_post(db)
    return db_post
