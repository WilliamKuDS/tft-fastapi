from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.misc.set import Set, SetCreate, SetUpdate


class SetNotFoundError(Exception):
    pass


class SetAlreadyExistsError(Exception):
    pass


def create_set(session: Session, set: SetCreate):
    existing_set = session.get(Set, set.set_id)
    if existing_set:
        raise SetAlreadyExistsError("Set already exists")

    db_set = Set.model_validate(set)
    session.add(db_set)
    session.commit()
    session.refresh(db_set)
    return db_set


def get_set(session: Session, set_id: Decimal):
    db_set = session.get(Set, set_id)
    if not db_set:
        raise SetNotFoundError("Set not found")
    return db_set


def get_sets(session: Session, offset: int, limit: int):
    return session.exec(select(Set).offset(offset).limit(limit)).all()


def update_set(session: Session, set_id: Decimal, set: SetUpdate):
    db_set = session.get(Set, set_id)
    if not db_set:
        raise SetNotFoundError("Set not found")
    set_data = set.model_dump(exclude_unset=True)
    for key, value in set_data.items():
        setattr(db_set, key, value)
    session.add(db_set)
    session.commit()
    session.refresh(db_set)
    return db_set


def delete_set(session: Session, set_id: Decimal):
    set_db = session.get(Set, set_id)
    if not set_db:
        raise SetNotFoundError("Set not found")
    session.delete(set_db)
    session.commit()
    return {"ok": True}