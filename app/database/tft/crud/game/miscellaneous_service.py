from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.game.miscellaneous import Miscellaneous, MiscellaneousCreate, MiscellaneousUpdate


class MiscellaneousNotFoundError(Exception):
    pass


class MiscellaneousAlreadyExistsError(Exception):
    pass


def create_miscellaneous(session: Session, miscellaneous: MiscellaneousCreate):
    existing_miscellaneous = session.get(Miscellaneous, miscellaneous.miscellaneous_id)
    if existing_miscellaneous:
        raise MiscellaneousAlreadyExistsError("Miscellaneous already exists")

    db_miscellaneous = Miscellaneous.model_validate(miscellaneous)
    session.add(db_miscellaneous)
    session.commit()
    session.refresh(db_miscellaneous)
    return db_miscellaneous


def get_miscellaneous(session: Session, miscellaneous_id: Decimal):
    db_miscellaneous = session.get(Miscellaneous, miscellaneous_id)
    if not db_miscellaneous:
        raise MiscellaneousNotFoundError("Miscellaneous not found")
    return db_miscellaneous


def get_miscellaneous_list(session: Session, offset: int, limit: int):
    return session.exec(select(Miscellaneous).offset(offset).limit(limit)).all()


def update_miscellaneous(session: Session, miscellaneous_id: Decimal, miscellaneous: MiscellaneousUpdate):
    db_miscellaneous = session.get(Miscellaneous, miscellaneous_id)
    if not db_miscellaneous:
        raise MiscellaneousNotFoundError("Miscellaneous not found")
    miscellaneous_data = miscellaneous.model_dump(exclude_unset=True)
    for key, value in miscellaneous_data.items():
        setattr(db_miscellaneous, key, value)
    session.add(db_miscellaneous)
    session.commit()
    session.refresh(db_miscellaneous)
    return db_miscellaneous


def delete_miscellaneous(session: Session, miscellaneous_id: Decimal):
    miscellaneous_db = session.get(Miscellaneous, miscellaneous_id)
    if not miscellaneous_db:
        raise MiscellaneousNotFoundError("Miscellaneous not found")
    session.delete(miscellaneous_db)
    session.commit()
    return {"ok": True}
