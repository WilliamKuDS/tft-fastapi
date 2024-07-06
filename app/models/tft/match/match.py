from app.models.base import SQLModel, Field, Optional


class MatchBase(SQLModel):
    game_id: int
    region: str
    game_result: str
    data_version: str
    game_creation: int
    game_datetime: int
    game_length: float
    game_version: str
    map_id: int
    queue_id: int
    game_type: str
    set_core_name: str
    set: int
    patch: str


class Match(MatchBase, table=True):
    match_id: str = Field(primary_key=True)


class MatchCreate(MatchBase):
    match_id: str


class MatchRead(MatchBase):
    match_id: str


class MatchUpdate(MatchBase):
    game_id: Optional[int] = None
    region: Optional[str] = None
    game_result: Optional[str] = None
    data_version: Optional[str] = None
    game_creation: Optional[int] = None
    game_datetime: Optional[int] = None
    game_length: Optional[float] = None
    game_version: Optional[str] = None
    map_id: Optional[int] = None
    queue_id: Optional[int] = None
    game_type: Optional[str] = None
    set_core_name: Optional[str] = None
    set: Optional[int] = None
    patch: Optional[str] = None
