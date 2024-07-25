
from sqlalchemy.orm import relationship, Mapped

from database.db_connection import Base
from sqlalchemy import Column, Integer, String

from models.passport import Passport


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    passport: Mapped["Passport"] = relationship(back_populates="person", cascade='all, delete-orphan')
