from decimal import Decimal
from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session

from app.models.account.league import League
from app.database.tft.crud.account import league_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()


# @router.post("/tft/league/create", response_model=League)
# @limiter.limit(2, "4/minute")
# async def create_league(
#         *,
#         request: Request,
#         session: Session = Depends(get_session),
#         league: LeagueCreate
# ):
#     try:
#         return league_service.create_league(session, league=league)
#     except league_service.LeagueAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="League already exists")


@router.get("/tft/league/all", response_model=list[League])
@limiter.limit(2, "4/minute")
async def read_leagues(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100)
):
    return league_service.get_leagues(session, offset, limit)


@router.get("/tft/league/{league_id}", response_model=League)
@limiter.limit(2, "4/minute")
async def read_league(
        *,
        request: Request,
        session: Session = Depends(get_session),
        league_id: Decimal
):
    try:
        return league_service.get_league(session, league_id=league_id)
    except league_service.LeagueNotFoundError:
        raise HTTPException(status_code=404, detail="League not found")


# @router.put("/tft/league/update/{league_id}", response_model=League)
# @limiter.limit(2, "4/minute")
# async def update_league(
#         *,
#         request: Request,
#         session: Session = Depends(get_session),
#         league_id: Decimal,
#         league: LeagueUpdate
# ):
#     try:
#         return league_service.update_league(session, league_id=league_id, league=league)
#     except league_service.LeagueNotFoundError:
#         raise HTTPException(status_code=404, detail="League not found")
#
#
# @router.delete("/tft/league/delete/{league_id}")
# @limiter.limit(2, "4/minute")
# async def delete_league(
#         *,
#         request: Request,
#         session: Session = Depends(get_session),
#         league_id: Decimal
# ):
#     try:
#         return league_service.delete_league(session, league_id=league_id)
#     except league_service.LeagueNotFoundError:
#         raise HTTPException(status_code=404, detail="League not found")
