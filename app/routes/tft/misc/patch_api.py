from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.models.tft.misc.patch import Patch
from app.database.tft.crud.misc import patch_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()


# @router.post("/tft/patch/create", response_model=Patch)
# @limiter.limit(2, "4/minute")
# async def create_patch(*, request: Request, session: Session = Depends(get_session), patch: PatchCreate):
#     try:
#         return patch_service.create_patch(session, patch=patch)
#     except patch_service.SetNotFoundError:
#         raise HTTPException(status_code=404, detail="Set not found for this patch")
#     except patch_service.PatchAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Patch already exists")


@router.get("/tft/patch/all", response_model=list[Patch])
@limiter.limit(5, "1/second")
async def read_patches(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100),
):
    return patch_service.get_patches(session, offset, limit)


@router.get("/tft/patch/{patch_id}", response_model=Patch)
@limiter.limit(2, "4/minute")
async def read_patch(
        *,
        request: Request,
        session: Session = Depends(get_session),
        patch_id: str
):
    try:
        return patch_service.get_patch(session, patch_id=patch_id)
    except patch_service.PatchNotFoundError:
        raise HTTPException(status_code=404, detail="Patch not found")


@router.get("/tft/patch/set/{set_id}", response_model=list[Patch])
@limiter.limit(2, "4/minute")
async def read_patch_by_set(
        *,
        request: Request,
        session: Session = Depends(get_session),
        set_id: str
):
    try:
        return patch_service.get_patch_by_set(session, set_id=set_id)
    except patch_service.PatchNotFoundError:
        raise HTTPException(status_code=404, detail="Patch not found")


# @router.put("/tft/patch/update/{patch_id}", response_model=Patch)
# @limiter.limit("10/minute")
# async def update_patch(*, request: Request, session: Session = Depends(get_session), patch_id: str, patch: PatchUpdate):
#     try:
#         return patch_service.update_patch(session, patch_id=patch_id, patch=patch)
#     except patch_service.PatchNotFoundError:
#         raise HTTPException(status_code=404, detail="Patch not found")
#     except patch_service.SetNotFoundError:
#         raise HTTPException(status_code=404, detail="Set not found for this patch")
#
#
# @router.delete("/tft/patch/delete/{patch_id}")
# @limiter.limit("10/minute")
# async def delete_patch(*, request: Request, session: Session = Depends(get_session), patch_id: str):
#     try:
#         return patch_service.delete_patch(session, patch_id=patch_id)
#     except patch_service.PatchNotFoundError:
#         raise HTTPException(status_code=404, detail="Patch not found")
