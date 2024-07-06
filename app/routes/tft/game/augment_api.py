from decimal import Decimal
from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session

from app.models.tft.game.augment import Augment, AugmentCreate, AugmentUpdate
from app.database.tft.crud.game import augment_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()

# @router.post("/tft/augment/create", response_model=Augment)
# @limiter.limit(2, "4/minute")
# async def create_augment(*, request: Request, session: Session = Depends(get_session), augment: AugmentCreate):
#     try:
#         return augment_service.create_augment(session, augment=augment)
#     except augment_service.AugmentAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Augment already exists")


@router.get("/tft/augment/all", response_model=list[Augment])
@limiter.limit(5, "1/second")
async def read_augments(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100),
):
    return augment_service.get_augments(session, offset, limit)


@router.get("/tft/augment/{augment_id}", response_model=Augment)
@limiter.limit(2, "4/minute")
async def read_augment(
        *,
        request: Request,
        session: Session = Depends(get_session),
        augment_id: Decimal
):
    try:
        return augment_service.get_augment(session, augment_id=augment_id)
    except augment_service.AugmentNotFoundError:
        raise HTTPException(status_code=404, detail="Augment not found")


# @router.put("/tft/augment/update/{augment_id}", response_model=Augment)
# @limiter.limit("10/minute")
# async def update_augment(*, request: Request, session: Session = Depends(get_session), augment_id: Decimal, augment: AugmentUpdate):
#     try:
#         return augment_service.update_augment(session, augment_id=augment_id, augment=augment)
#     except augment_service.AugmentNotFoundError:
#         raise HTTPException(status_code=404, detail="Augment not found")


# @router.delete("/tft/augment/delete/{augment_id}")
# @limiter.limit("10/minute")
# async def delete_augment(*, request: Request, session: Session = Depends(get_session), augment_id: Decimal):
#     try:
#         return augment_service.delete_augment(session, augment_id=augment_id)
#     except augment_service.AugmentNotFoundError:
#         raise HTTPException(status_code=404, detail="Augment not found")
