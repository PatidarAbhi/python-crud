
from typing import List

from sqlalchemy.orm import relationship, Mapped

from database.db_connection import Base
from sqlalchemy import Boolean, Column, Integer, String

from models.post import Post


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

