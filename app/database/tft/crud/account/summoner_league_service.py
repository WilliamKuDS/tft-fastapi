from decimal import Decimal
from sqlmodel import Session, select
from app.models.account.summoner_league import SummonerLeague, SummonerLeagueCreate, SummonerLeagueUpdate


class SummonerLeagueNotFoundError(Exception):
    pass


class SummonerLeagueAlreadyExistsError(Exception):
    pass


def create_summoner_league(session: Session, summoner_league: SummonerLeagueCreate):
    existing_summoner_league = session.get(SummonerLeague, summoner_league.summoner_league_id)
    if existing_summoner_league:
        raise SummonerLeagueAlreadyExistsError("Summoner League already exists")

    db_summoner_league = SummonerLeague.model_validate(summoner_league)
    session.add(db_summoner_league)
    session.commit()
    session.refresh(db_summoner_league)
    return db_summoner_league


def get_summoner_league(session: Session, summoner_league_id: Decimal):
    db_summoner_league = session.get(SummonerLeague, summoner_league_id)
    if not db_summoner_league:
        raise SummonerLeagueNotFoundError("Summoner League not found")
    return db_summoner_league


def get_summoner_leagues(session: Session, offset: int, limit: int):
    return session.exec(select(SummonerLeague).offset(offset).limit(limit)).all()


def update_summoner_league(session: Session, summoner_league_id: Decimal, summoner_league: SummonerLeagueUpdate):
    db_summoner_league = session.get(SummonerLeague, summoner_league_id)
    if not db_summoner_league:
        raise SummonerLeagueNotFoundError("Summoner League not found")
    summoner_league_data = summoner_league.model_dump(exclude_unset=True)
    for key, value in summoner_league_data.items():
        setattr(db_summoner_league, key, value)
    session.add(db_summoner_league)
    session.commit()
    session.refresh(db_summoner_league)
    return db_summoner_league


def delete_summoner_league(session: Session, summoner_league_id: Decimal):
    summoner_league_db = session.get(SummonerLeague, summoner_league_id)
    if not summoner_league_db:
        raise SummonerLeagueNotFoundError("Summoner League not found")
    session.delete(summoner_league_db)
    session.commit()
    return {"ok": True}
