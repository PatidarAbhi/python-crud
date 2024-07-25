from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, Mapped

from database.db_connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey


if TYPE_CHECKING:
    from models.person import Person


class Passport(Base):
    __tablename__ = 'passport'

    id = Column(Integer, primary_key=True, index=True)
    passport_number = Column(String(50), unique=True, index=True)
    person_id = Column(Integer, ForeignKey('person.id'), unique=True, nullable=False)

    person: Mapped["Person"] = relationship(back_populates="passport")
