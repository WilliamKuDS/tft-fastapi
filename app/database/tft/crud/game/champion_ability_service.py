from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.game.champion_ability import ChampionAbility, ChampionAbilityCreate, ChampionAbilityUpdate


class ChampionAbilityNotFoundError(Exception):
    pass


class ChampionAbilityAlreadyExistsError(Exception):
    pass


def create_champion_ability(session: Session, champion_ability: ChampionAbilityCreate):
    existing_champion_ability = session.get(ChampionAbility, champion_ability.champion_ability_id)
    if existing_champion_ability:
        raise ChampionAbilityAlreadyExistsError("ChampionAbility already exists")

    db_champion_ability = ChampionAbility.model_validate(champion_ability)
    session.add(db_champion_ability)
    session.commit()
    session.refresh(db_champion_ability)
    return db_champion_ability


def get_champion_ability(session: Session, champion_ability_id: Decimal):
    db_champion_ability = session.get(ChampionAbility, champion_ability_id)
    if not db_champion_ability:
        raise ChampionAbilityNotFoundError("ChampionAbility not found")
    return db_champion_ability


def get_champion_abilities(session: Session, offset: int, limit: int):
    return session.exec(select(ChampionAbility).offset(offset).limit(limit)).all()


def update_champion_ability(session: Session, champion_ability_id: Decimal, champion_ability: ChampionAbilityUpdate):
    db_champion_ability = session.get(ChampionAbility, champion_ability_id)
    if not db_champion_ability:
        raise ChampionAbilityNotFoundError("ChampionAbility not found")
    champion_ability_data = champion_ability.model_dump(exclude_unset=True)
    for key, value in champion_ability_data.items():
        setattr(db_champion_ability, key, value)
    session.add(db_champion_ability)
    session.commit()
    session.refresh(db_champion_ability)
    return db_champion_ability


def delete_champion_ability(session: Session, champion_ability_id: Decimal):
    champion_ability_db = session.get(ChampionAbility, champion_ability_id)
    if not champion_ability_db:
        raise ChampionAbilityNotFoundError("ChampionAbility not found")
    session.delete(champion_ability_db)
    session.commit()
    return {"ok": True}
