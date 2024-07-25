from sqlalchemy import Table, Column, ForeignKey
from database.db_connection import Base

association_table = Table(
    "project_team",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("team_id", ForeignKey("teams.id"), primary_key=True),
)
