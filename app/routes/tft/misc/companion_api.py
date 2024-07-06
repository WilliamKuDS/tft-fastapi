# from decimal import Decimal
# from fastapi import HTTPException, APIRouter, Depends, Query, Request
# from sqlmodel import Session
#
# from app.models.tft.misc.companion import Companion, CompanionCreate, CompanionUpdate
# from app.database.tft.crud import companion_service
# from app.routes.limiter import limiter
# from app.routes.session import get_session
# from app.utils.check_ip import check_ip
#
# router = APIRouter()
#
#
# @router.post("/tft/companion/create", response_model=Companion)
# @limiter.limit_tier(2, "4/minute", 10)
# async def create_companion(
#         *,
#         request: Request,
#         ip_check: bool = Depends(check_ip),
#         session: Session = Depends(get_session),
#         companion: CompanionCreate
# ):
#     try:
#         return companion_service.create_companion(session, companion=companion)
#     except companion_service.CompanionAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Companion already exists")
#
#
# @router.get("/tft/companion/all", response_model=list[Companion])
# @limiter.limit_tier(2, "4/minute", 10)
# async def read_companions(
#         request: Request,
#         ip_check: bool = Depends(check_ip),
#         session: Session = Depends(get_session),
#         offset: int = 0,
#         limit: int = Query(default=100, le=100)
# ):
#     return companion_service.get_companions(session, offset, limit)
#
#
# @router.get("/tft/companion/{companion_id}", response_model=Companion)
# @limiter.limit_tier(2, "4/minute", 10)
# async def read_companion(
#         *,
#         request: Request,
#         ip_check: bool = Depends(check_ip),
#         session: Session = Depends(get_session),
#         companion_id: Decimal
# ):
#     try:
#         return companion_service.get_companion(session, companion_id=companion_id)
#     except companion_service.CompanionNotFoundError:
#         raise HTTPException(status_code=404, detail="Companion not found")
#
#
# @router.put("/tft/companion/update/{companion_id}", response_model=Companion)
# @limiter.limit_tier(2, "4/minute", 10)
# async def update_companion(
#         *,
#         request: Request,
#         ip_check: bool = Depends(check_ip),
#         session: Session = Depends(get_session),
#         companion_id: Decimal,
#         companion: CompanionUpdate
# ):
#     try:
#         return companion_service.update_companion(session, companion_id=companion_id, companion=companion)
#     except companion_service.CompanionNotFoundError:
#         raise HTTPException(status_code=404, detail="Companion not found")
#
#
# @router.delete("/tft/companion/delete/{companion_id}")
# @limiter.limit_tier(2, "4/minute", 10)
# async def delete_companion(
#         *,
#         request: Request,
#         ip_check: bool = Depends(check_ip),
#         session: Session = Depends(get_session),
#         companion_id: Decimal
# ):
#     try:
#         return companion_service.delete_companion(session, companion_id=companion_id)
#     except companion_service.CompanionNotFoundError:
#         raise HTTPException(status_code=404, detail="Companion not found")
