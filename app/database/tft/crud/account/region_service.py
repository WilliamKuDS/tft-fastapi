from decimal import Decimal
from sqlmodel import Session, select
from app.models.account.region import Region, RegionCreate, RegionUpdate


class RegionNotFoundError(Exception):
    pass


class RegionAlreadyExistsError(Exception):
    pass


def create_region(session: Session, region: RegionCreate):
    existing_region = session.get(Region, region.region_id)
    if existing_region:
        raise RegionAlreadyExistsError("Region already exists")

    db_region = Region.model_validate(region)
    session.add(db_region)
    session.commit()
    session.refresh(db_region)
    return db_region


def get_region(session: Session, region_id: str):
    db_region = session.get(Region, region_id)
    if not db_region:
        raise RegionNotFoundError("Region not found")
    return db_region


def get_regions(session: Session, offset: int, limit: int):
    return session.exec(select(Region).offset(offset).limit(limit)).all()


def update_region(session: Session, region_id: str, region: RegionUpdate):
    db_region = session.get(Region, region_id)
    if not db_region:
        raise RegionNotFoundError("Region not found")
    region_data = region.model_dump(exclude_unset=True)
    for key, value in region_data.items():
        setattr(db_region, key, value)
    session.add(db_region)
    session.commit()
    session.refresh(db_region)
    return db_region


def delete_region(session: Session, region_id: str):
    region_db = session.get(Region, region_id)
    if not region_db:
        raise RegionNotFoundError("Region not found")
    session.delete(region_db)
    session.commit()
    return {"ok": True}
