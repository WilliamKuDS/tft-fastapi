from typing import Optional
from app.models.base import SQLModel, Field, Decimal


class SetBase(SQLModel):
    set_name: str


class Set(SetBase, table=True):
    set_id: Decimal = Field(primary_key=True)


class SetCreate(SetBase):
    set_id: Decimal


class SetRead(SetBase):
    set_id: Decimal


class SetUpdate(SQLModel):
    set_name: Optional[str] = None


class SetDelete(SetBase):
    set_id: Decimal
