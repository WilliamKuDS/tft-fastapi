from decimal import Decimal
from sqlmodel import Session, select
from app.models.account.account import Account, AccountCreate, AccountUpdate


class AccountNotFoundError(Exception):
    pass


class AccountAlreadyExistsError(Exception):
    pass


def create_account(session: Session, account: AccountCreate):
    existing_account = session.get(Account, account.account_id)
    if existing_account:
        raise AccountAlreadyExistsError("Account already exists")

    db_account = Account.model_validate(account)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


def get_account(session: Session, account_id: Decimal):
    db_account = session.get(Account, account_id)
    if not db_account:
        raise AccountNotFoundError("Account not found")
    return db_account


def get_accounts(session: Session, offset: int, limit: int):
    return session.exec(select(Account).offset(offset).limit(limit)).all()


def update_account(session: Session, account_id: Decimal, account: AccountUpdate):
    db_account = session.get(Account, account_id)
    if not db_account:
        raise AccountNotFoundError("Account not found")
    account_data = account.model_dump(exclude_unset=True)
    for key, value in account_data.items():
        setattr(db_account, key, value)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


def delete_account(session: Session, account_id: Decimal):
    account_db = session.get(Account, account_id)
    if not account_db:
        raise AccountNotFoundError("Account not found")
    session.delete(account_db)
    session.commit()
    return {"ok": True}
