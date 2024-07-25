from sqlalchemy.orm import Session

from models.project import Project


def create_project(db: Session, name: str):
    db_project = Project(name=name)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
