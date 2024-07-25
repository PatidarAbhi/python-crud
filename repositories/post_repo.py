
from sqlalchemy.orm import Session, joinedload
from models.user import Post


def create_post(db: Session, title: str, content: str, owner_id: int):
    db_post = Post(title=title, content=content, owner_id=owner_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_all_post(db: Session):
    return db.query(Post).all()
