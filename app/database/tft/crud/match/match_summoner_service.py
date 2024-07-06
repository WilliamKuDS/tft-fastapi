from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.match.match_summoner import MatchSummoner, MatchSummonerCreate, MatchSummonerUpdate


class MatchSummonerNotFoundError(Exception):
    pass


class MatchSummonerAlreadyExistsError(Exception):
    pass


def create_match_summoner(session: Session, match_summoner: MatchSummonerCreate):
    existing_match_summoner = session.get(MatchSummoner, match_summoner.match_summoner_id)
    if existing_match_summoner:
        raise MatchSummonerAlreadyExistsError("Match Summoner already exists")

    db_match_summoner = MatchSummoner.model_validate(match_summoner)
    session.add(db_match_summoner)
    session.commit()
    session.refresh(db_match_summoner)
    return db_match_summoner


def get_match_summoner(session: Session, match_summoner_id: Decimal):
    db_match_summoner = session.get(MatchSummoner, match_summoner_id)
    if not db_match_summoner:
        raise MatchSummonerNotFoundError("Match Summoner not found")
    return db_match_summoner


def get_match_summoners(session: Session, offset: int, limit: int):
    return session.exec(select(MatchSummoner).offset(offset).limit(limit)).all()


def update_match_summoner(session: Session, match_summoner_id: Decimal, match_summoner: MatchSummonerUpdate):
    db_match_summoner = session.get(MatchSummoner, match_summoner_id)
    if not db_match_summoner:
        raise MatchSummonerNotFoundError("Match Summoner not found")
    match_summoner_data = match_summoner.model_dump(exclude_unset=True)
    for key, value in match_summoner_data.items():
        setattr(db_match_summoner, key, value)
    session.add(db_match_summoner)
    session.commit()
    session.refresh(db_match_summoner)
    return db_match_summoner


def delete_match_summoner(session: Session, match_summoner_id: Decimal):
    match_summoner_db = session.get(MatchSummoner, match_summoner_id)
    if not match_summoner_db:
        raise MatchSummonerNotFoundError("Match Summoner not found")
    session.delete(match_summoner_db)
    session.commit()
    return {"ok": True}
