from decimal import Decimal
from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.database.database import engine
from app.models.tft.misc.set import Set, SetCreate, SetUpdate
from app.database.tft.crud import set_service
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/tft/set/create", response_model=Set)
@limiter.limit("10/minute")
async def create_set(*, request: Request, session: Session = Depends(get_session), set: SetCreate):
    try:
        return set_service.create_set(session, set=set)
    except set_service.SetAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Set already exists")


@router.get("/tft/set/all", response_model=list[Set])
@limiter.limit("1/minute")
async def read_sets(
        *,
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100),
):
    return set_service.get_sets(session, offset, limit)


@router.get("/tft/set/{set_id}", response_model=Set)
@limiter.limit("100/minute")
async def read_set(*, request: Request, session: Session = Depends(get_session), set_id: Decimal):
    try:
        return set_service.get_set(session, set_id=set_id)
    except set_service.SetNotFoundError:
        raise HTTPException(status_code=404, detail="Set not found")


@router.put("/tft/set/update/{set_id}", response_model=Set)
@limiter.limit("1/minute")
async def update_set(*, request: Request, session: Session = Depends(get_session), set_id: Decimal, set: SetUpdate):
    try:
        return set_service.update_set(session, set_id=set_id, set=set)
    except set_service.SetNotFoundError:
        raise HTTPException(status_code=404, detail="Set not found")


@router.delete("/tft/set/delete/{set_id}")
@limiter.limit("5/minute")
async def delete_set(*, request: Request, session: Session = Depends(get_session), set_id: Decimal):
    try:
        return set_service.delete_set(session, set_id=set_id)
    except set_service.SetNotFoundError:
        raise HTTPException(status_code=404, detail="Set not found")
