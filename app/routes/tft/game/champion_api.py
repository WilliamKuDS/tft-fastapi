from decimal import Decimal
from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session

from app.models.tft.game.champion import Champion, ChampionCreate, ChampionUpdate
from app.database.tft.crud.game import champion_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()

# @router.post("/tft/champion/create", response_model=Champion)
# @limiter.limit(2, "4/minute")
# async def create_champion(*, request: Request, session: Session = Depends(get_session), champion: ChampionCreate):
#     try:
#         return champion_service.create_champion(session, champion=champion)
#     except champion_service.ChampionAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Champion already exists")


@router.get("/tft/champion/all", response_model=list[Champion])
@limiter.limit(5, "1/second")
async def read_champions(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100),
):
    return champion_service.get_champions(session, offset, limit)


@router.get("/tft/champion/{champion_id}", response_model=Champion)
@limiter.limit(2, "4/minute")
async def read_champion(
        *,
        request: Request,
        session: Session = Depends(get_session),
        champion_id: Decimal
):
    try:
        return champion_service.get_champion(session, champion_id=champion_id)
    except champion_service.ChampionNotFoundError:
        raise HTTPException(status_code=404, detail="Champion not found")


# @router.put("/tft/champion/update/{champion_id}", response_model=Champion)
# @limiter.limit("10/minute")
# async def update_champion(*, request: Request, session: Session = Depends(get_session), champion_id: Decimal, champion: ChampionUpdate):
#     try:
#         return champion_service.update_champion(session, champion_id=champion_id, champion=champion)
#     except champion_service.ChampionNotFoundError:
#         raise HTTPException(status_code=404, detail="Champion not found")


# @router.delete("/tft/champion/delete/{champion_id}")
# @limiter.limit("10/minute")
# async def delete_champion(*, request: Request, session: Session = Depends(get_session), champion_id: Decimal):
#     try:
#         return champion_service.delete_champion(session, champion_id=champion_id)
#     except champion_service.ChampionNotFoundError:
#         raise HTTPException(status_code=404, detail="Champion not found")
