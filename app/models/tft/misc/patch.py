from app.models.base import SQLModel, Field, Optional, date, Decimal


class PatchBase(SQLModel):
    set_id: Decimal = Field(foreign_key="set.set_id")
    date_start: date
    date_end: Optional[date] = None
    highlights: str
    patch_url: str


class Patch(PatchBase, table=True):
    patch_id: str = Field(primary_key=True)


class PatchCreate(PatchBase):
    patch_id: str


class PatchRead(PatchBase):
    patch_id: str


class PatchUpdate(SQLModel):
    set_id: Optional[Decimal] = Field(foreign_key="set.set_id")
    date_start: Optional[date] = None
    date_end: Optional[date] = None
    highlights: Optional[str] = None
    patch_url: Optional[str] = None
