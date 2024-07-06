from fastapi import HTTPException, APIRouter, Depends, Query, Request
from sqlmodel import Session
from decimal import Decimal

from app.models.account.account import Account
from app.database.tft.crud.account import account_service
from app.routes.limiter import limiter
from app.routes.session import get_session
from app.utils.check_ip import check_ip

router = APIRouter(prefix="/tft/account")


# @router.post("/create", response_model=Account)
# @limiter.limit(2, "4/minute")
# async def create_account(
#         *,
#         request: Request,
#         session: Session = Depends(get_session),
#         account: AccountCreate
# ):
#     try:
#         return account_service.create_account(session, account=account)
#     except account_service.AccountAlreadyExistsError:
#         raise HTTPException(status_code=400, detail="Account already exists")


@router.get("/all", response_model=list[Account])
@limiter.limit(5, "1/second")
async def read_accounts(
        request: Request,
        ip_check: bool = Depends(check_ip),
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, le=100)
):
    return account_service.get_accounts(session, offset, limit)


@router.get("/{account_id}", response_model=Account)
@limiter.limit(2, "1/second")
async def read_account(
        *,
        request: Request,
        session: Session = Depends(get_session),
        account_id: Decimal
):
    try:
        return account_service.get_account(session, account_id=account_id)
    except account_service.AccountNotFoundError:
        raise HTTPException(status_code=404, detail="Account not found")


# @router.put("/update/{account_id}", response_model=Account)
# @limiter.limit(1, "1/minute")
# async def update_account(
#         *,
#         request: Request,
#         session: Session = Depends(get_session),
#         account_id: Decimal,
#         account: AccountUpdate
# ):
#     try:
#         return account_service.update_account(session, account_id=account_id, account=account)
#     except account_service.AccountNotFoundError:
#         raise HTTPException(status_code=404, detail="Account not found")


# @router.delete("/delete/{account_id}")
# @limiter.limit(2, "4/minute")
# async def delete_account(
#         *,
#         request: Request,
#         ip_check: bool = Depends(check_ip),
#         session: Session = Depends(get_session),
#         account_id: Decimal
# ):
#     try:
#         return account_service.delete_account(session, account_id=account_id)
#     except account_service.AccountNotFoundError:
#         raise HTTPException(status_code=404, detail="Account not found")
