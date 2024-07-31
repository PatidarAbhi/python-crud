
from sqlalchemy.orm import Session
from models.user import Post
from payload.user_payload import PostBase


def create_post(db: Session, post: PostBase):
    db_post = Post(title=post.title, content=post.content, owner_id=post.owner_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_all_post(db: Session):
    return db.query(Post).all()


def delete_post(db: Session, post_id: int):
    result = db.query(Post).filter(Post.id == post_id).delete(synchronize_session=False)
    db.commit()
    return result


def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def update_post(db: Session, post: Post):
    db.commit()
    db.refresh(post)
    return post
