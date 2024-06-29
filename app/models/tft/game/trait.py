from app.models.base import SQLModel, Field, Optional

class TraitBase(SQLModel):
    api_name: str = Field(index=True)
    patch_id: str = Field(foreign_key="patch.patch_id")
    display_name: str
    icon: str
    description: str

class Trait(TraitBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class TraitCreate(TraitBase):
    pass

class TraitRead(TraitBase):
    id: int