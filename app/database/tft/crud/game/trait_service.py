from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.game.trait import Trait, TraitCreate, TraitUpdate


class TraitNotFoundError(Exception):
    pass


class TraitAlreadyExistsError(Exception):
    pass


def create_trait(session: Session, trait: TraitCreate):
    existing_trait = session.get(Trait, trait.trait_id)
    if existing_trait:
        raise TraitAlreadyExistsError("Trait already exists")

    db_trait = Trait.model_validate(trait)
    session.add(db_trait)
    session.commit()
    session.refresh(db_trait)
    return db_trait


def get_trait(session: Session, trait_id: Decimal):
    db_trait = session.get(Trait, trait_id)
    if not db_trait:
        raise TraitNotFoundError("Trait not found")
    return db_trait


def get_traits(session: Session, offset: int, limit: int):
    return session.exec(select(Trait).offset(offset).limit(limit)).all()


def update_trait(session: Session, trait_id: Decimal, trait: TraitUpdate):
    db_trait = session.get(Trait, trait_id)
    if not db_trait:
        raise TraitNotFoundError("Trait not found")
    trait_data = trait.model_dump(exclude_unset=True)
    for key, value in trait_data.items():
        setattr(db_trait, key, value)
    session.add(db_trait)
    session.commit()
    session.refresh(db_trait)
    return db_trait


def delete_trait(session: Session, trait_id: Decimal):
    trait_db = session.get(Trait, trait_id)
    if not trait_db:
        raise TraitNotFoundError("Trait not found")
    session.delete(trait_db)
    session.commit()
    return {"ok": True}
