from typing import List

from sqlalchemy.orm import relationship, Mapped

from database.db_connection import Base
from sqlalchemy import Boolean, Column, Integer, String

from models.post import Post


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    posts: Mapped[List["Post"]] = relationship()

