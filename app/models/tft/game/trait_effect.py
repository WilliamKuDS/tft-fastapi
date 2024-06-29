from app.models.base import SQLModel, Field, Optional, JSON, Column

class TraitEffectBase(SQLModel):
    trait_id: int = Field(foreign_key="trait.id")
    style: Optional[int] = None
    min_units: int
    max_units: int
    variables: dict = Field(sa_column=Column(JSON))

class TraitEffect(TraitEffectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class TraitEffectCreate(TraitEffectBase):
    pass

class TraitEffectRead(TraitEffectBase):
    id: int