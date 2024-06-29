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