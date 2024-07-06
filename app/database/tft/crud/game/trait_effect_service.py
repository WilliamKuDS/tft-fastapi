from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.game.trait_effect import TraitEffect, TraitEffectCreate, TraitEffectUpdate


class TraitEffectNotFoundError(Exception):
    pass


class TraitEffectAlreadyExistsError(Exception):
    pass


def create_trait_effect(session: Session, trait_effect: TraitEffectCreate):
    existing_trait_effect = session.get(TraitEffect, trait_effect.trait_effect_id)
    if existing_trait_effect:
        raise TraitEffectAlreadyExistsError("TraitEffect already exists")

    db_trait_effect = TraitEffect.model_validate(trait_effect)
    session.add(db_trait_effect)
    session.commit()
    session.refresh(db_trait_effect)
    return db_trait_effect


def get_trait_effect(session: Session, trait_effect_id: Decimal):
    db_trait_effect = session.get(TraitEffect, trait_effect_id)
    if not db_trait_effect:
        raise TraitEffectNotFoundError("TraitEffect not found")
    return db_trait_effect


def get_trait_effects(session: Session, offset: int, limit: int):
    return session.exec(select(TraitEffect).offset(offset).limit(limit)).all()


def update_trait_effect(session: Session, trait_effect_id: Decimal, trait_effect: TraitEffectUpdate):
    db_trait_effect = session.get(TraitEffect, trait_effect_id)
    if not db_trait_effect:
        raise TraitEffectNotFoundError("TraitEffect not found")
    trait_effect_data = trait_effect.model_dump(exclude_unset=True)
    for key, value in trait_effect_data.items():
        setattr(db_trait_effect, key, value)
    session.add(db_trait_effect)
    session.commit()
    session.refresh(db_trait_effect)
    return db_trait_effect


def delete_trait_effect(session: Session, trait_effect_id: Decimal):
    trait_effect_db = session.get(TraitEffect, trait_effect_id)
    if not trait_effect_db:
        raise TraitEffectNotFoundError("TraitEffect not found")
    session.delete(trait_effect_db)
    session.commit()
    return {"ok": True}
