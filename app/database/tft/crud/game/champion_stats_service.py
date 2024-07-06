from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.game.champion_stats import ChampionStats, ChampionStatsCreate, ChampionStatsUpdate


class ChampionStatsNotFoundError(Exception):
    pass


class ChampionStatsAlreadyExistsError(Exception):
    pass


def create_champion_stats(session: Session, champion_stats: ChampionStatsCreate):
    existing_champion_stats = session.get(ChampionStats, champion_stats.champion_stats_id)
    if existing_champion_stats:
        raise ChampionStatsAlreadyExistsError("ChampionStats already exists")

    db_champion_stats = ChampionStats.model_validate(champion_stats)
    session.add(db_champion_stats)
    session.commit()
    session.refresh(db_champion_stats)
    return db_champion_stats


def get_champion_stats(session: Session, champion_stats_id: Decimal):
    db_champion_stats = session.get(ChampionStats, champion_stats_id)
    if not db_champion_stats:
        raise ChampionStatsNotFoundError("ChampionStats not found")
    return db_champion_stats


def get_champion_stats_list(session: Session, offset: int, limit: int):
    return session.exec(select(ChampionStats).offset(offset).limit(limit)).all()


def update_champion_stats(session: Session, champion_stats_id: Decimal, champion_stats: ChampionStatsUpdate):
    db_champion_stats = session.get(ChampionStats, champion_stats_id)
    if not db_champion_stats:
        raise ChampionStatsNotFoundError("ChampionStats not found")
    champion_stats_data = champion_stats.model_dump(exclude_unset=True)
    for key, value in champion_stats_data.items():
        setattr(db_champion_stats, key, value)
    session.add(db_champion_stats)
    session.commit()
    session.refresh(db_champion_stats)
    return db_champion_stats


def delete_champion_stats(session: Session, champion_stats_id: Decimal):
    champion_stats_db = session.get(ChampionStats, champion_stats_id)
    if not champion_stats_db:
        raise ChampionStatsNotFoundError("ChampionStats not found")
    session.delete(champion_stats_db)
    session.commit()
    return {"ok": True}
