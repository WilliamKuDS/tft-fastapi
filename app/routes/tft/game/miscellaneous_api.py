from decimal import Decimal

from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.models.tft.game.miscellaneous import Miscellaneous, MiscellaneousCreate, MiscellaneousUpdate
from app.database.tft.crud.game import miscellaneous_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()

# @router.post("/tft/miscellaneous/create", response_model=Miscellaneous)
# @limiter.limit(2, "4/minute")
# async def create_miscellaneous(*, request: Request, session: Session = Depends(get_session), miscellaneous: MiscellaneousCreate):
#     try:
#         return miscellaneous_service.create_miscellaneous(session, miscellaneous=miscellaneous)
#     except miscellaneous_service.MiscellaneousAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Miscellaneous already exists")


@router.get("/tft/miscellaneous/all", response_model=list[Miscellaneous])
@limiter.limit(5, "1/second")
async def read_miscellaneous(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100),
):
    return miscellaneous_service.get_miscellaneous_list(session, offset, limit)


@router.get("/tft/miscellaneous/{miscellaneous_id}", response_model=Miscellaneous)
@limiter.limit(2, "4/minute")
async def read_miscellaneous(
        *,
        request: Request,
        session: Session = Depends(get_session),
        miscellaneous_id: Decimal
):
    try:
        return miscellaneous_service.get_miscellaneous(session, miscellaneous_id=miscellaneous_id)
    except miscellaneous_service.MiscellaneousNotFoundError:
        raise HTTPException(status_code=404, detail="Miscellaneous not found")


# @router.put("/tft/miscellaneous/update/{miscellaneous_id}", response_model=Miscellaneous)
# @limiter.limit("10/minute")
# async def update_miscellaneous(*, request: Request, session: Session = Depends(get_session), miscellaneous_id: Decimal, miscellaneous: MiscellaneousUpdate):
#     try:
#         return miscellaneous_service.update_miscellaneous(session, miscellaneous_id=miscellaneous_id, miscellaneous=miscellaneous)
#     except miscellaneous_service.MiscellaneousNotFoundError:
#         raise HTTPException(status_code=404, detail="Miscellaneous not found")


# @router.delete("/tft/miscellaneous/delete/{miscellaneous_id}")
# @limiter.limit("10/minute")
# async def delete_miscellaneous(*, request: Request, session: Session = Depends(get_session), miscellaneous_id: Decimal):
#     try:
#         return miscellaneous_service.delete_miscellaneous(session, miscellaneous_id=miscellaneous_id)
#     except miscellaneous_service.MiscellaneousNotFoundError:
#         raise HTTPException(status_code=404, detail="Miscellaneous not found")
