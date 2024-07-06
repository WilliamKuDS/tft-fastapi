from decimal import Decimal
from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.models.tft.misc.set import Set
from app.database.tft.crud.misc import set_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()


# @router.post("/tft/set/create", response_model=Set)
# @limiter.limit("10/minute")
# async def create_set(*, request: Request, session: Session = Depends(get_session), set: SetCreate):
#     try:
#         return set_service.create_set(session, set=set)
#     except set_service.SetAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Set already exists")


@router.get("/tft/set/all", response_model=list[Set])
@limiter.limit(2, "4/minute")
async def read_sets(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100),
):
    return set_service.get_sets(session, offset, limit)


@router.get("/tft/set/{set_id}", response_model=Set)
@limiter.limit(2, "4/minute")
async def read_set(
        *,
        request: Request,
        session: Session = Depends(get_session),
        set_id: Decimal
):
    try:
        return set_service.get_set(session, set_id=set_id)
    except set_service.SetNotFoundError:
        raise HTTPException(status_code=404, detail="Set not found")


# @router.put("/tft/set/update/{set_id}", response_model=Set)
# @limiter.limit("1/minute")
# async def update_set(*, request: Request, session: Session = Depends(get_session), set_id: Decimal, set: SetUpdate):
#     try:
#         return set_service.update_set(session, set_id=set_id, set=set)
#     except set_service.SetNotFoundError:
#         raise HTTPException(status_code=404, detail="Set not found")
#
#
# @router.delete("/tft/set/delete/{set_id}")
# @limiter.limit("5/minute")
# async def delete_set(*, request: Request, session: Session = Depends(get_session), set_id: Decimal):
#     try:
#         return set_service.delete_set(session, set_id=set_id)
#     except set_service.SetNotFoundError:
#         raise HTTPException(status_code=404, detail="Set not found")
