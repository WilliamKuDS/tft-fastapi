from decimal import Decimal
from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.models.tft.match.match_summoner import MatchSummoner
from app.database.tft.crud.match import match_summoner_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()


# @router.post("/tft/match/summoner/create", response_model=MatchSummoner)
# @limiter.limit(2, "4/minute")
# async def create_match_summoner(*, request: Request, session: Session = Depends(get_session),
#                                 match_summoner: MatchSummonerCreate):
#     try:
#         return match_summoner_service.create_match_summoner(session, match_summoner=match_summoner)
#     except match_summoner_service.MatchSummonerAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Match Summoner already exists")


@router.get("/tft/match/summoner/all", response_model=list[MatchSummoner])
@limiter.limit(2, "4/minute")
async def read_match_summoners(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100)
):
    return match_summoner_service.get_match_summoners(session, offset, limit)


@router.get("/tft/match/summoner/{match_summoner_id}", response_model=MatchSummoner)
@limiter.limit(2, "4/minute")
async def read_match_summoner(
        *,
        request: Request,
        session: Session = Depends(get_session),
        match_summoner_id: Decimal
):
    try:
        return match_summoner_service.get_match_summoner(session, match_summoner_id=match_summoner_id)
    except match_summoner_service.MatchSummonerNotFoundError:
        raise HTTPException(status_code=404, detail="Match Summoner not found")


# @router.put("/tft/match/summoner/update/{match_summoner_id}", response_model=MatchSummoner)
# @limiter.limit("1/minute")
# async def update_match_summoner(*, request: Request, session: Session = Depends(get_session),
#                                 match_summoner_id: Decimal, match_summoner: MatchSummonerUpdate):
#     try:
#         return match_summoner_service.update_match_summoner(session, match_summoner_id=match_summoner_id,
#                                                             match_summoner=match_summoner)
#     except match_summoner_service.MatchSummonerNotFoundError:
#         raise HTTPException(status_code=404, detail="Match Summoner not found")
#
#
# @router.delete("/tft/match/summoner/delete/{match_summoner_id}")
# @limiter.limit("5/minute")
# async def delete_match_summoner(*, request: Request, session: Session = Depends(get_session),
#                                 match_summoner_id: Decimal):
#     try:
#         return match_summoner_service.delete_match_summoner(session, match_summoner_id=match_summoner_id)
#     except match_summoner_service.MatchSummonerNotFoundError:
#         raise HTTPException(status_code=404, detail="Match Summoner not found")
