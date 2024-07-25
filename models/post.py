

from database.db_connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)


