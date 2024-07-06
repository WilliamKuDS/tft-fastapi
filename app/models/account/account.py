from app.models.base import SQLModel, Field, Optional


class AccountBase(SQLModel):
    game_name: str = Field(index=True)
    tag_line: str = Field(index=True)


class Account(AccountBase, table=True):
    puuid: str = Field(primary_key=True)


class AccountCreate(AccountBase):
    puuid: str


class AccountRead(AccountBase):
    puuid: str


class AccountUpdate(AccountBase):
    game_name: Optional[str] = None
    tag_line: Optional[str] = None
