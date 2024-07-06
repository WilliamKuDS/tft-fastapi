from app.models.base import SQLModel, Field, Optional, datetime


class SummonerBase(SQLModel):
    summoner_id: str = Field(index=True)
    region_id: str = Field(foreign_key="region.region_id")
    puuid: str = Field(foreign_key="account.puuid")
    account_id: str
    icon: str
    level: int
    revision_date: int


class Summoner(SummonerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    last_updated: Optional[datetime] = None


class SummonerCreate(SummonerBase):
    pass


class SummonerRead(SummonerBase):
    id: int
    last_updated: Optional[datetime]


class SummonerUpdate(SummonerBase):
    region_id: Optional[str] = Field(foreign_key="region.region_id")
    puuid: Optional[str] = Field(foreign_key="account.puuid")
    account_id: Optional[str] = None
    icon: Optional[str] = None
    level: Optional[int] = None
    revision_date: Optional[int] = None
    last_updated: Optional[datetime] = datetime.now()
