from app.models.base import SQLModel, Field, Optional, JSON, Column


class MatchSummonerBase(SQLModel):
    match_id: str = Field(foreign_key="match.match_id")
    puuid: str = Field(foreign_key="account.puuid")
    placement: int
    gold_left: int
    last_round: int
    level: int
    players_eliminated: int
    time_eliminated: float
    total_damage_to_players: int
    companion: dict = Field(sa_column=Column(JSON))
    missions: dict = Field(sa_column=Column(JSON))
    augments: dict = Field(sa_column=Column(JSON))
    traits: dict = Field(sa_column=Column(JSON))
    units: dict = Field(sa_column=Column(JSON))


class MatchSummoner(MatchSummonerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class MatchSummonerCreate(MatchSummonerBase):
    pass


class MatchSummonerRead(MatchSummonerBase):
    id: int


class MatchSummonerUpdate(MatchSummonerBase):
    match_id: Optional[str] = Field(foreign_key="match.match_id")
    puuid: Optional[str] = Field(foreign_key="account.puuid")
    placement: Optional[int] = None
    gold_left: Optional[int] = None
    last_round: Optional[int] = None
    level: Optional[int] = None
    players_eliminated: Optional[int] = None
    time_eliminated: Optional[float] = None
    total_damage_to_players: Optional[int] = None
    companion: Optional[dict] = Field(sa_column=Column(JSON))
    missions: Optional[dict] = Field(sa_column=Column(JSON))
    augments: Optional[dict] = Field(sa_column=Column(JSON))
    traits: Optional[dict] = Field(sa_column=Column(JSON))
    units: Optional[dict] = Field(sa_column=Column(JSON))
