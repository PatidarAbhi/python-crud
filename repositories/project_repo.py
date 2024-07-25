from sqlalchemy.orm import Session, joinedload

from models.project import Project


def create_project(db: Session, name: str):
    db_project = Project(name=name)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_all_projects(db: Session):
    return db.query(Project).options(joinedload(Project.teams)).all()


def delete_project(db: Session, project_id: int):
    result = db.query(Project).filter(Project.id == project_id).delete(synchronize_session=False)
    db.commit()
    return result
