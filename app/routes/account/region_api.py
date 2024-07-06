from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.models.account.region import Region
from app.database.tft.crud.account import region_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()


# @router.post("/tft/region/create", response_model=Region)
# @limiter.limit("10/minute")
# async def create_region(*, request: Request, session: Session = Depends(get_session), region: RegionCreate):
#     try:
#         return region_service.create_region(session, region=region)
#     except region_service.RegionAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Region already exists")


@router.get("/tft/region/all", response_model=list[Region])
@limiter.limit(2, "4/minute")
async def read_regions(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100)
):
    return region_service.get_regions(session, offset, limit)


@router.get("/tft/region/{region_id}", response_model=Region)
@limiter.limit("100/minute")
async def read_region(
        *,
        request: Request,
        session: Session = Depends(get_session),
        region_id: str
):
    try:
        return region_service.get_region(session, region_id=region_id)
    except region_service.RegionNotFoundError:
        raise HTTPException(status_code=404, detail="Region not found")


# @router.put("/tft/region/update/{region_id}", response_model=Region)
# @limiter.limit("1/minute")
# async def update_region(*, request: Request, session: Session = Depends(get_session), region_id: Decimal,
#                         region: RegionUpdate):
#     try:
#         return region_service.update_region(session, region_id=region_id, region=region)
#     except region_service.RegionNotFoundError:
#         raise HTTPException(status_code=404, detail="Region not found")
#
#
# @router.delete("/tft/region/delete/{region_id}")
# @limiter.limit("5/minute")
# async def delete_region(*, request: Request, session: Session = Depends(get_session), region_id: Decimal):
#     try:
#         return region_service.delete_region(session, region_id=region_id)
#     except region_service.RegionNotFoundError:
#         raise HTTPException(status_code=404, detail="Region not found")
