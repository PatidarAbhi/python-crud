from sqlalchemy.orm import Session
from repositories import post_repo


def create_post(db: Session, title: str, content: str, owner_id: int):
    return post_repo.create_post(db, title, content, owner_id)


def get_all_post(db: Session):
    return post_repo.get_all_post(db)
