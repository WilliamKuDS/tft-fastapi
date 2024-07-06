from decimal import Decimal
from sqlmodel import Session, select
from app.models.account.league import League, LeagueCreate, LeagueUpdate


class LeagueNotFoundError(Exception):
    pass


class LeagueAlreadyExistsError(Exception):
    pass


def create_league(session: Session, league: LeagueCreate):
    existing_league = session.get(League, league.league_id)
    if existing_league:
        raise LeagueAlreadyExistsError("League already exists")

    db_league = League.model_validate(league)
    session.add(db_league)
    session.commit()
    session.refresh(db_league)
    return db_league


def get_league(session: Session, league_id: Decimal):
    db_league = session.get(League, league_id)
    if not db_league:
        raise LeagueNotFoundError("League not found")
    return db_league


def get_leagues(session: Session, offset: int, limit: int):
    return session.exec(select(League).offset(offset).limit(limit)).all()


def update_league(session: Session, league_id: Decimal, league: LeagueUpdate):
    db_league = session.get(League, league_id)
    if not db_league:
        raise LeagueNotFoundError("League not found")
    league_data = league.model_dump(exclude_unset=True)
    for key, value in league_data.items():
        setattr(db_league, key, value)
    session.add(db_league)
    session.commit()
    session.refresh(db_league)
    return db_league


def delete_league(session: Session, league_id: Decimal):
    league_db = session.get(League, league_id)
    if not league_db:
        raise LeagueNotFoundError("League not found")
    session.delete(league_db)
    session.commit()
    return {"ok": True}
