from decimal import Decimal

from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.models.tft.game.trait import Trait, TraitCreate, TraitUpdate
from app.database.tft.crud.game import trait_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()

# @router.post("/tft/trait/create", response_model=Trait)
# @limiter.limit(2, "4/minute")
# async def create_trait(*, request: Request, session: Session = Depends(get_session), trait: TraitCreate):
#     try:
#         return trait_service.create_trait(session, trait=trait)
#     except trait_service.TraitAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Trait already exists")


@router.get("/tft/trait/all", response_model=list[Trait])
@limiter.limit(5, "1/second")
async def read_traits(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100),
):
    return trait_service.get_traits(session, offset, limit)


@router.get("/tft/trait/{trait_id}", response_model=Trait)
@limiter.limit(2, "4/minute")
async def read_trait(
        *,
        request: Request,
        session: Session = Depends(get_session),
        trait_id: Decimal
):
    try:
        return trait_service.get_trait(session, trait_id=trait_id)
    except trait_service.TraitNotFoundError:
        raise HTTPException(status_code=404, detail="Trait not found")


# @router.put("/tft/trait/update/{trait_id}", response_model=Trait)
# @limiter.limit("10/minute")
# async def update_trait(*, request: Request, session: Session = Depends(get_session), trait_id: Decimal, trait: TraitUpdate):
#     try:
#         return trait_service.update_trait(session, trait_id=trait_id, trait=trait)
#     except trait_service.TraitNotFoundError:
#         raise HTTPException(status_code=404, detail="Trait not found")


# @router.delete("/tft/trait/delete/{trait_id}")
# @limiter.limit("10/minute")
# async def delete_trait(*, request: Request, session: Session = Depends(get_session), trait_id: Decimal):
#     try:
#         return trait_service.delete_trait(session, trait_id=trait_id)
#     except trait_service.TraitNotFoundError:
#         raise HTTPException(status_code=404, detail="Trait not found")
