from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.misc.companion import Companion, CompanionCreate, CompanionUpdate


class CompanionNotFoundError(Exception):
    pass


class CompanionAlreadyExistsError(Exception):
    pass


def create_companion(session: Session, companion: CompanionCreate):
    existing_companion = session.get(Companion, companion.companion_id)
    if existing_companion:
        raise CompanionAlreadyExistsError("Companion already exists")

    db_companion = Companion.model_validate(companion)
    session.add(db_companion)
    session.commit()
    session.refresh(db_companion)
    return db_companion


def get_companion(session: Session, companion_id: Decimal):
    db_companion = session.get(Companion, companion_id)
    if not db_companion:
        raise CompanionNotFoundError("Companion not found")
    return db_companion


def get_companions(session: Session, offset: int, limit: int):
    return session.exec(select(Companion).offset(offset).limit(limit)).all()


def update_companion(session: Session, companion_id: Decimal, companion: CompanionUpdate):
    db_companion = session.get(Companion, companion_id)
    if not db_companion:
        raise CompanionNotFoundError("Companion not found")
    companion_data = companion.model_dump(exclude_unset=True)
    for key, value in companion_data.items():
        setattr(db_companion, key, value)
    session.add(db_companion)
    session.commit()
    session.refresh(db_companion)
    return db_companion


def delete_companion(session: Session, companion_id: Decimal):
    companion_db = session.get(Companion, companion_id)
    if not companion_db:
        raise CompanionNotFoundError("Companion not found")
    session.delete(companion_db)
    session.commit()
    return {"ok": True}
