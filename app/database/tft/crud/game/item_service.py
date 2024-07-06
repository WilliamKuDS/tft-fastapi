from decimal import Decimal
from sqlmodel import Session, select
from app.models.tft.game.item import Item, ItemCreate, ItemUpdate


class ItemNotFoundError(Exception):
    pass


class ItemAlreadyExistsError(Exception):
    pass


def create_item(session: Session, item: ItemCreate):
    existing_item = session.get(Item, item.item_id)
    if existing_item:
        raise ItemAlreadyExistsError("Item already exists")

    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_item(session: Session, item_id: Decimal):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise ItemNotFoundError("Item not found")
    return db_item


def get_items(session: Session, offset: int, limit: int):
    return session.exec(select(Item).offset(offset).limit(limit)).all()


def update_item(session: Session, item_id: Decimal, item: ItemUpdate):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise ItemNotFoundError("Item not found")
    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def delete_item(session: Session, item_id: Decimal):
    item_db = session.get(Item, item_id)
    if not item_db:
        raise ItemNotFoundError("Item not found")
    session.delete(item_db)
    session.commit()
    return {"ok": True}
