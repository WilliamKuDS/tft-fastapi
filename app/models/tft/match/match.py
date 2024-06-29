from app.models.base import SQLModel, Field

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