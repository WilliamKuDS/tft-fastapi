from app.models.base import SQLModel, Field, JSON, Column, Optional


class CompanionBase(SQLModel):
    item_id: int
    name: str
    loadout_icon: str
    description: str
    level: int
    species_name: str
    species_id: int
    rarity: str
    rarity_value: int
    is_default: bool
    upgrades: dict = Field(sa_column=Column(JSON))
    tft_only: bool


class Companion(CompanionBase, table=True):
    content_id: str = Field(primary_key=True)


class CompanionCreate(CompanionBase):
    content_id: str


class CompanionRead(CompanionBase):
    content_id: str


class CompanionUpdate(CompanionBase):
    item_id: Optional[int] = None
    name: Optional[str] = None
    loadout_icon: Optional[str] = None
    description: Optional[str] = None
    level: Optional[int] = None
    species_name: Optional[str] = None
    species_id: Optional[int] = None
    rarity: Optional[str] = None
    rarity_value: Optional[int] = None
    is_default: Optional[bool] = None
    upgrades: Optional[dict] = Field(sa_column=Column(JSON))
    tft_only: Optional[bool] = None
