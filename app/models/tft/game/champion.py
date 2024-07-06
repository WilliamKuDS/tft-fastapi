from app.models.base import SQLModel, Field, Optional


class ChampionBase(SQLModel):
    api_name: str = Field(index=True)
    patch_id: str = Field(foreign_key="patch.patch_id")
    character_name: Optional[str] = None
    display_name: str
    cost: int
    icon: Optional[str] = None
    square_icon: Optional[str] = None
    tile_icon: Optional[str] = None


class Champion(ChampionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ChampionCreate(ChampionBase):
    pass


class ChampionRead(ChampionBase):
    id: int


class ChampionUpdate(ChampionBase):
    api_name: str = None
    patch_id: str = Field(foreign_key="patch.patch_id")
    character_name: Optional[str] = None
    display_name: Optional[str] = None
    cost: Optional[int] = None
    icon: Optional[str] = None
    square_icon: Optional[str] = None
    tile_icon: Optional[str] = None
