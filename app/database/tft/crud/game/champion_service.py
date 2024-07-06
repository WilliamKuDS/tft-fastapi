from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.game.champion import Champion, ChampionCreate, ChampionUpdate


class ChampionNotFoundError(Exception):
    pass


class ChampionAlreadyExistsError(Exception):
    pass


def create_champion(session: Session, champion: ChampionCreate):
    existing_champion = session.get(Champion, champion.champion_id)
    if existing_champion:
        raise ChampionAlreadyExistsError("Champion already exists")

    db_champion = Champion.model_validate(champion)
    session.add(db_champion)
    session.commit()
    session.refresh(db_champion)
    return db_champion


def get_champion(session: Session, champion_id: Decimal):
    db_champion = session.get(Champion, champion_id)
    if not db_champion:
        raise ChampionNotFoundError("Champion not found")
    return db_champion


def get_champions(session: Session, offset: int, limit: int):
    return session.exec(select(Champion).offset(offset).limit(limit)).all()


def update_champion(session: Session, champion_id: Decimal, champion: ChampionUpdate):
    db_champion = session.get(Champion, champion_id)
    if not db_champion:
        raise ChampionNotFoundError("Champion not found")
    champion_data = champion.model_dump(exclude_unset=True)
    for key, value in champion_data.items():
        setattr(db_champion, key, value)
    session.add(db_champion)
    session.commit()
    session.refresh(db_champion)
    return db_champion


def delete_champion(session: Session, champion_id: Decimal):
    champion_db = session.get(Champion, champion_id)
    if not champion_db:
        raise ChampionNotFoundError("Champion not found")
    session.delete(champion_db)
    session.commit()
    return {"ok": True}
