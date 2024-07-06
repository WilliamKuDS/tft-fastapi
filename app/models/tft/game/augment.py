from app.models.base import SQLModel, Field, Optional, JSON, Column


class AugmentBase(SQLModel):
    api_name: str = Field(index=True)
    patch_id: str = Field(foreign_key="patch.patch_id")
    display_name: Optional[str] = None
    description: Optional[str] = None
    icon: str
    unique: Optional[bool] = None
    effects: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    associated_traits: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    incompatible_traits: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    composition: Optional[dict] = Field(default=None, sa_column=Column(JSON))


class Augment(AugmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class AugmentCreate(AugmentBase):
    id: int


class AugmentRead(AugmentBase):
    id: int


class AugmentUpdate(AugmentBase):
    api_name: str = None
    patch_id: str = Field(foreign_key="patch.patch_id")
    display_name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    unique: Optional[bool] = None
    effects: Optional[dict] = None
    associated_traits: Optional[dict] = None
    incompatible_traits: Optional[dict] = None
    composition: Optional[dict] = None
