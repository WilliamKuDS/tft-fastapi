from app.models.base import SQLModel, Field, Optional

class LeagueBase(SQLModel):
    league_id: str = Field(index=True)
    region_id: str = Field(foreign_key="region.region_id")
    tier: str
    name: str
    queue: str

class League(LeagueBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class LeagueCreate(LeagueBase):
    pass

class LeagueRead(LeagueBase):
    id: int