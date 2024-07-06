from decimal import Decimal
from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.models.tft.match.match import Match
from app.database.tft.crud.match import match_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()


# @router.post("/tft/match/create", response_model=Match)
# @limiter.limit(2, "4/minute")
# async def create_match(
#         *,
#         request: Request,
#         session: Session = Depends(get_session),
#         match: MatchCreate
# ):
#     try:
#         return match_service.create_match(session, match=match)
#     except match_service.MatchAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Match already exists")


@router.get("/tft/match/all", response_model=list[Match])
@limiter.limit(2, "4/minute")
async def read_matches(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100)
):
    return match_service.get_matches(session, offset, limit)


@router.get("/tft/match/{match_id}", response_model=Match)
@limiter.limit(2, "4/minute")
async def read_match(
        *,
        request: Request,
        session: Session = Depends(get_session),
        match_id: Decimal
):
    try:
        return match_service.get_match(session, match_id=match_id)
    except match_service.MatchNotFoundError:
        raise HTTPException(status_code=404, detail="Match not found")


# @router.put("/tft/match/update/{match_id}", response_model=Match)
# @limiter.limit(2, "4/minute")
# async def update_match(
#         *,
#         request: Request,
#         session: Session = Depends(get_session),
#         match_id: Decimal,
#         match: MatchUpdate
# ):
#     try:
#         return match_service.update_match(session, match_id=match_id, match=match)
#     except match_service.MatchNotFoundError:
#         raise HTTPException(status_code=404, detail="Match not found")


# @router.delete("/tft/match/delete/{match_id}")
# @limiter.limit(2, "4/minute")
# async def delete_match(
#         *,
#         request: Request,
#         session: Session = Depends(get_session),
#         match_id: Decimal
# ):
#     try:
#         return match_service.delete_match(session, match_id=match_id)
#     except match_service.MatchNotFoundError:
#         raise HTTPException(status_code=404, detail="Match not found")
