from typing import List, TYPE_CHECKING

from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.db_connection import Base
from models.association import association_table

if TYPE_CHECKING:
    from models.team import Team


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    teams: Mapped[List["Team"]] = relationship(
        secondary=association_table,
        back_populates="projects"
    )
