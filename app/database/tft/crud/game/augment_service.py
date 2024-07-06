from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.game.augment import Augment, AugmentCreate, AugmentUpdate


class AugmentNotFoundError(Exception):
    pass


class AugmentAlreadyExistsError(Exception):
    pass


def create_augment(session: Session, augment: AugmentCreate):
    existing_augment = session.get(Augment, augment.augment_id)
    if existing_augment:
        raise AugmentAlreadyExistsError("Augment already exists")

    db_augment = Augment.model_validate(augment)
    session.add(db_augment)
    session.commit()
    session.refresh(db_augment)
    return db_augment


def get_augment(session: Session, augment_id: Decimal):
    db_augment = session.get(Augment, augment_id)
    if not db_augment:
        raise AugmentNotFoundError("Augment not found")
    return db_augment


def get_augments(session: Session, offset: int, limit: int):
    return session.exec(select(Augment).offset(offset).limit(limit)).all()


def update_augment(session: Session, augment_id: Decimal, augment: AugmentUpdate):
    db_augment = session.get(Augment, augment_id)
    if not db_augment:
        raise AugmentNotFoundError("Augment not found")
    augment_data = augment.model_dump(exclude_unset=True)
    for key, value in augment_data.items():
        setattr(db_augment, key, value)
    session.add(db_augment)
    session.commit()
    session.refresh(db_augment)
    return db_augment


def delete_augment(session: Session, augment_id: Decimal):
    augment_db = session.get(Augment, augment_id)
    if not augment_db:
        raise AugmentNotFoundError("Augment not found")
    session.delete(augment_db)
    session.commit()
    return {"ok": True}
