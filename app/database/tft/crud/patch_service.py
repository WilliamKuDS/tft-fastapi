from sqlmodel import Session, select
from app.models.tft.misc.patch import Patch, PatchCreate, PatchUpdate
from app.models.tft.misc.set import Set


class PatchNotFoundError(Exception):
    pass


class SetNotFoundError(Exception):
    pass


class PatchAlreadyExistsError(Exception):
    pass


def create_patch(session: Session, patch: PatchCreate):
    db_set = session.get(Set, patch.set_id)
    if not db_set:
        raise SetNotFoundError("Set not found for this patch")

    existing_patch = session.get(Patch, patch.patch_id)
    if existing_patch:
        raise PatchAlreadyExistsError("Patch already exists")

    db_patch = Patch.model_validate(patch)
    session.add(db_patch)
    session.commit()
    session.refresh(db_patch)
    return db_patch


def get_patch(session: Session, patch_id: str):
    db_patch = session.get(Patch, patch_id)
    if not db_patch:
        raise PatchNotFoundError("Patch not found")
    return db_patch


def get_patches(session: Session, offset: int, limit: int):
    return session.exec(select(Patch).offset(offset).limit(limit)).all()


def update_patch(session: Session, patch_id: str, patch: PatchUpdate):
    db_patch = session.get(Patch, patch_id)
    if not db_patch:
        raise PatchNotFoundError("Patch not found")

    db_set = session.get(Set, patch.set_id)
    if not db_set:
        raise SetNotFoundError("Set not found for this patch")

    patch_data = patch.model_dump(exclude_unset=True)
    for key, value in patch_data.items():
        setattr(db_patch, key, value)
    session.add(db_patch)
    session.commit()
    session.refresh(db_patch)
    return db_patch


def delete_patch(session: Session, patch_id: str):
    db_patch = session.get(Patch, patch_id)
    if not db_patch:
        raise PatchNotFoundError("Patch not found")
    session.delete(db_patch)
    session.commit()
    return {"ok": True}