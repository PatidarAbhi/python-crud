from sqlalchemy import text, asc, desc
from sqlalchemy.orm import Session, joinedload
from models.user import User
from payload.user_payload import UsersNameResponse


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session):
    return db.query(User).options(joinedload(User.posts)).all()


def create_user(db: Session, username: str, hashed_password: str):
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users_name(db: Session):
    users = db.query(User).all()
    return users


def get_by_name(db: Session, username: str):
    query = text("SELECT * FROM users WHERE username = :username")
    result = db.execute(query, {"username": username}).fetchone()

    user = db.query(User).filter(User.username == username).first()
    if user:
        return user
    return None


#get users by pagination
def get_all_users(db: Session, skip: int = 0, limit: int = 4, order_by: str = 'id', order: str = 'dsc'):
    query = db.query(User)

    if order == 'asc':
        query = query.order_by(asc(getattr(User, order_by)))
    else:
        query = query.order_by(desc(getattr(User, order_by)))

    users = query.offset(skip).limit(limit).all()

    return users


def delete_user(db: Session, user_id: int):
    result = db.query(User).filter(User.id == user_id).delete(synchronize_session=False)
    db.commit()
    return result
