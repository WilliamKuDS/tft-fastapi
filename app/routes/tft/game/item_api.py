from decimal import Decimal

from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from app.models.tft.game.item import Item, ItemCreate, ItemUpdate
from app.database.tft.crud.game import item_service
from app.routes.limiter import limiter
from app.routes.session import get_session

router = APIRouter()

# @router.post("/tft/item/create", response_model=Item)
# @limiter.limit(2, "4/minute")
# async def create_item(*, request: Request, session: Session = Depends(get_session), item: ItemCreate):
#     try:
#         return item_service.create_item(session, item=item)
#     except item_service.ItemAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Item already exists")


@router.get("/tft/item/all", response_model=list[Item])
@limiter.limit(5, "1/second")
async def read_items(
        request: Request,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100),
):
    return item_service.get_items(session, offset, limit)


@router.get("/tft/item/{item_id}", response_model=Item)
@limiter.limit(2, "4/minute")
async def read_item(
        *,
        request: Request,
        session: Session = Depends(get_session),
        item_id: Decimal
):
    try:
        return item_service.get_item(session, item_id=item_id)
    except item_service.ItemNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")


# @router.put("/tft/item/update/{item_id}", response_model=Item)
# @limiter.limit("10/minute")
# async def update_item(*, request: Request, session: Session = Depends(get_session), item_id: Decimal, item: ItemUpdate):
#     try:
#         return item_service.update_item(session, item_id=item_id, item=item)
#     except item_service.ItemNotFoundError:
#         raise HTTPException(status_code=404, detail="Item not found")


# @router.delete("/tft/item/delete/{item_id}")
# @limiter.limit("10/minute")
# async def delete_item(*, request: Request, session: Session = Depends(get_session), item_id: Decimal):
#     try:
#         return item_service.delete_item(session, item_id=item_id)
#     except item_service.ItemNotFoundError:
#         raise HTTPException(status_code=404, detail="Item not found")
