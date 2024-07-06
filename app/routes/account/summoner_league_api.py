from decimal import Decimal
from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.models.account.summoner_league import SummonerLeague
from app.database.tft.crud.account import summoner_league_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()


# @router.post("/tft/summoner_league/create", response_model=SummonerLeague)
# @limiter.limit("10/minute")
# async def create_summoner_league(*, request: Request, session: Session = Depends(get_session),
#                                  summoner_league: SummonerLeagueCreate):
#     try:
#         return summoner_league_service.create_summoner_league(session, summoner_league=summoner_league)
#     except summoner_league_service.SummonerLeagueAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Summoner League already exists")


@router.get("/tft/summoner_league/all", response_model=list[SummonerLeague])
@limiter.limit(2, "4/minute")
async def read_summoner_leagues(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100)
):
    return summoner_league_service.get_summoner_leagues(session, offset, limit)


@router.get("/tft/summoner_league/{summoner_league_id}", response_model=SummonerLeague)
@limiter.limit(2, "4/minute")
async def read_summoner_league(
        *,
        request: Request,
        session: Session = Depends(get_session),
        summoner_league_id: Decimal
):
    try:
        return summoner_league_service.get_summoner_league(session, summoner_league_id=summoner_league_id)
    except summoner_league_service.SummonerLeagueNotFoundError:
        raise HTTPException(status_code=404, detail="Summoner League not found")


# @router.put("/tft/summoner_league/update/{summoner_league_id}", response_model=SummonerLeague)
# @limiter.limit("1/minute")
# async def update_summoner_league(*, request: Request, session: Session = Depends(get_session),
#                                  summoner_league_id: Decimal, summoner_league: SummonerLeagueUpdate):
#     try:
#         return summoner_league_service.update_summoner_league(session, summoner_league_id=summoner_league_id,
#                                                               summoner_league=summoner_league)
#     except summoner_league_service.SummonerLeagueNotFoundError:
#         raise HTTPException(status_code=404, detail="Summoner League not found")
#
#
# @router.delete("/tft/summoner_league/delete/{summoner_league_id}")
# @limiter.limit("5/minute")
# async def delete_summoner_league(*, request: Request, session: Session = Depends(get_session),
#                                  summoner_league_id: Decimal):
#     try:
#         return summoner_league_service.delete_summoner_league(session, summoner_league_id=summoner_league_id)
#     except summoner_league_service.SummonerLeagueNotFoundError:
#         raise HTTPException(status_code=404, detail="Summoner League not found")
