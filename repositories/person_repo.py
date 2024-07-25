from sqlalchemy.orm import Session, joinedload

from models import Person


def create_person(db: Session, name: str):
    person = Person(username=name)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def get_all_persons(db: Session):
    return db.query(Person).options(joinedload(Person.passport)).all()
