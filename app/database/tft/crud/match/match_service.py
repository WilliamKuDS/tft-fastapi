from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.match.match import Match, MatchCreate, MatchUpdate


class MatchNotFoundError(Exception):
    pass


class MatchAlreadyExistsError(Exception):
    pass


def create_match(session: Session, match: MatchCreate):
    existing_match = session.get(Match, match.match_id)
    if existing_match:
        raise MatchAlreadyExistsError("Match already exists")

    db_match = Match.model_validate(match)
    session.add(db_match)
    session.commit()
    session.refresh(db_match)
    return db_match


def get_match(session: Session, match_id: Decimal):
    db_match = session.get(Match, match_id)
    if not db_match:
        raise MatchNotFoundError("Match not found")
    return db_match


def get_matches(session: Session, offset: int, limit: int):
    return session.exec(select(Match).offset(offset).limit(limit)).all()


def update_match(session: Session, match_id: Decimal, match: MatchUpdate):
    db_match = session.get(Match, match_id)
    if not db_match:
        raise MatchNotFoundError("Match not found")
    match_data = match.model_dump(exclude_unset=True)
    for key, value in match_data.items():
        setattr(db_match, key, value)
    session.add(db_match)
    session.commit()
    session.refresh(db_match)
    return db_match


def delete_match(session: Session, match_id: Decimal):
    match_db = session.get(Match, match_id)
    if not match_db:
        raise MatchNotFoundError("Match not found")
    session.delete(match_db)
    session.commit()
    return {"ok": True}
