from decimal import Decimal
from sqlmodel import Session, select
from app.models.account.summoner import Summoner, SummonerCreate, SummonerUpdate


class SummonerNotFoundError(Exception):
    pass


class SummonerAlreadyExistsError(Exception):
    pass


def create_summoner(session: Session, summoner: SummonerCreate):
    existing_summoner = session.get(Summoner, summoner.summoner_id)
    if existing_summoner:
        raise SummonerAlreadyExistsError("Summoner already exists")

    db_summoner = Summoner.model_validate(summoner)
    session.add(db_summoner)
    session.commit()
    session.refresh(db_summoner)
    return db_summoner


def get_summoner(session: Session, summoner_id: Decimal):
    db_summoner = session.get(Summoner, summoner_id)
    if not db_summoner:
        raise SummonerNotFoundError("Summoner not found")
    return db_summoner


def get_summoners(session: Session, offset: int, limit: int):
    return session.exec(select(Summoner).offset(offset).limit(limit)).all()


def update_summoner(session: Session, summoner_id: Decimal, summoner: SummonerUpdate):
    db_summoner = session.get(Summoner, summoner_id)
    if not db_summoner:
        raise SummonerNotFoundError("Summoner not found")
    summoner_data = summoner.model_dump(exclude_unset=True)
    for key, value in summoner_data.items():
        setattr(db_summoner, key, value)
    session.add(db_summoner)
    session.commit()
    session.refresh(db_summoner)
    return db_summoner


def delete_summoner(session: Session, summoner_id: Decimal):
    summoner_db = session.get(Summoner, summoner_id)
    if not summoner_db:
        raise SummonerNotFoundError("Summoner not found")
    session.delete(summoner_db)
    session.commit()
    return {"ok": True}
