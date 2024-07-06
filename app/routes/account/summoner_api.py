from decimal import Decimal
from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.models.account.summoner import Summoner
from app.database.tft.crud.account import summoner_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()


# @router.post("/tft/summoner/create", response_model=Summoner)
# @limiter.limit("10/minute")
# async def create_summoner(*, request: Request, session: Session = Depends(get_session), summoner: SummonerCreate):
#     try:
#         return summoner_service.create_summoner(session, summoner=summoner)
#     except summoner_service.SummonerAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Summoner already exists")


@router.get("/tft/summoner/all", response_model=list[Summoner])
@limiter.limit(2, "4/minute")
async def read_summoners(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100)
):
    return summoner_service.get_summoners(session, offset, limit)


@router.get("/tft/summoner/{summoner_id}", response_model=Summoner)
@limiter.limit(2, "4/minute")
async def read_summoner(
        *,
        request: Request,
        session: Session = Depends(get_session),
        summoner_id: Decimal
):
    try:
        return summoner_service.get_summoner(session, summoner_id=summoner_id)
    except summoner_service.SummonerNotFoundError:
        raise HTTPException(status_code=404, detail="Summoner not found")


# @router.put("/tft/summoner/update/{summoner_id}", response_model=Summoner)
# @limiter.limit("1/minute")
# async def update_summoner(*, request: Request, session: Session = Depends(get_session), summoner_id: Decimal,
#                           summoner: SummonerUpdate):
#     try:
#         return summoner_service.update_summoner(session, summoner_id=summoner_id, summoner=summoner)
#     except summoner_service.SummonerNotFoundError:
#         raise HTTPException(status_code=404, detail="Summoner not found")
#
#
# @router.delete("/tft/summoner/delete/{summoner_id}")
# @limiter.limit("5/minute")
# async def delete_summoner(*, request: Request, session: Session = Depends(get_session), summoner_id: Decimal):
#     try:
#         return summoner_service.delete_summoner(session, summoner_id=summoner_id)
#     except summoner_service.SummonerNotFoundError:
#         raise HTTPException(status_code=404, detail="Summoner not found")
