from sqlalchemy.orm import Session, joinedload

from models import Passport


def create_passport(db: Session, number: str, person_id: int):
    person = Passport(passport_number=number, person_id=person_id)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def get_all_passports(db: Session):
    return db.query(Passport).options(joinedload(Passport.person)).all()



