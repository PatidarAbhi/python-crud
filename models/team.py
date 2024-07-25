from typing import List

from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.db_connection import Base
from models.association import association_table
from models.project import Project


class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    projects: Mapped[List["Project"]] = relationship(secondary=association_table,
                                                     back_populates="teams")
