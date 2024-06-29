from app.models.base import SQLModel, Field, Optional, JSON, Column

class MiscellaneousBase(SQLModel):
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

class Miscellaneous(MiscellaneousBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ItemCreate(MiscellaneousBase):
    pass

class ItemRead(MiscellaneousBase):
    id: int

# Use the same structure for Augment and Miscellaneous, just change the class names