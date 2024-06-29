from app.models.base import SQLModel, Field

class RegionBase(SQLModel):
    label: str
    server: str
    description: str

class Region(RegionBase, table=True):
    region_id: str = Field(primary_key=True)

class RegionCreate(RegionBase):
    region_id: str

class RegionRead(RegionBase):
    region_id: str