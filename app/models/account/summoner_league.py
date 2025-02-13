from app.models.base import SQLModel, Field, Optional


class SummonerLeagueBase(SQLModel):
    summoner_id: int = Field(foreign_key="summoner.id")
    region_id: str = Field(foreign_key="region.region_id")
    queue: str
    puuid: str = Field(foreign_key="account.puuid")
    league_id: int = Field(foreign_key="league.id")
    tier: str
    rank: str
    league_points: int
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    fresh_blood: bool
    hot_streak: bool


class SummonerLeague(SummonerLeagueBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class SummonerLeagueCreate(SummonerLeagueBase):
    pass


class SummonerLeagueRead(SummonerLeagueBase):
    id: int


class SummonerLeagueUpdate(SummonerLeagueBase):
    summoner_id: Optional[int] = Field(foreign_key="summoner.id")
    region_id: Optional[str] = Field(foreign_key="region.region_id")
    queue: Optional[str] = None
    puuid: Optional[str] = Field(foreign_key="account.puuid")
    league_id: Optional[int] = Field(foreign_key="league.id")
    tier: Optional[str] = None
    rank: Optional[str] = None
    league_points: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    veteran: Optional[bool] = None
    inactive: Optional[bool] = None
    fresh_blood: Optional[bool] = None
    hot_streak: Optional[bool] = None
