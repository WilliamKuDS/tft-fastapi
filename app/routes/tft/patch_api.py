from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.database.database import engine
from app.models.tft.misc.patch import Patch, PatchCreate, PatchUpdate
from app.database.tft.crud import patch_service
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/tft/patch/create", response_model=Patch)
@limiter.limit("10/minute")
async def create_patch(*, request: Request, session: Session = Depends(get_session), patch: PatchCreate):
    try:
        return patch_service.create_patch(session, patch=patch)
    except patch_service.SetNotFoundError:
        raise HTTPException(status_code=404, detail="Set not found for this patch")
    except patch_service.PatchAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Patch already exists")


@router.get("/tft/patch/all", response_model=list[Patch])
@limiter.limit("10/minute")
async def read_patches(
        *,
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100),
):
    return patch_service.get_patches(session, offset, limit)


@router.get("/tft/patch/{patch_id}", response_model=Patch)
@limiter.limit("10/minute")
async def read_patch(*, request: Request, session: Session = Depends(get_session), patch_id: str):
    try:
        return patch_service.get_patch(session, patch_id=patch_id)
    except patch_service.PatchNotFoundError:
        raise HTTPException(status_code=404, detail="Patch not found")


@router.put("/tft/patch/update/{patch_id}", response_model=Patch)
@limiter.limit("10/minute")
async def update_patch(*, request: Request, session: Session = Depends(get_session), patch_id: str, patch: PatchUpdate):
    try:
        return patch_service.update_patch(session, patch_id=patch_id, patch=patch)
    except patch_service.PatchNotFoundError:
        raise HTTPException(status_code=404, detail="Patch not found")
    except patch_service.SetNotFoundError:
        raise HTTPException(status_code=404, detail="Set not found for this patch")


@router.delete("/tft/patch/delete/{patch_id}")
@limiter.limit("10/minute")
async def delete_patch(*, request: Request, session: Session = Depends(get_session), patch_id: str):
    try:
        return patch_service.delete_patch(session, patch_id=patch_id)
    except patch_service.PatchNotFoundError:
        raise HTTPException(status_code=404, detail="Patch not found")
