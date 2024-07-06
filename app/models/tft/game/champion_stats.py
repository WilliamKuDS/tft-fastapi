from app.models.base import SQLModel, Field, Optional


class ChampionStatsBase(SQLModel):
    champion_id: int = Field(foreign_key="champion.id")
    armor: Optional[int] = None
    attack_speed: Optional[float] = None
    crit_chance: Optional[float] = None
    crit_multiplier: Optional[float] = None
    damage: Optional[int] = None
    hp: Optional[int] = None
    initial_mana: Optional[int] = None
    mana: Optional[int] = None
    magic_resist: Optional[int] = None
    range: Optional[int] = None


class ChampionStats(ChampionStatsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ChampionStatsCreate(ChampionStatsBase):
    pass


class ChampionStatsRead(ChampionStatsBase):
    id: int


class ChampionStatsUpdate(ChampionStatsBase):
    champion_id: int = Field(foreign_key="champion.id")
    armor: Optional[int] = None
    attack_speed: Optional[float] = None
    crit_chance: Optional[float] = None
    crit_multiplier: Optional[float] = None
    damage: Optional[int] = None
    hp: Optional[int] = None
    initial_mana: Optional[int] = None
    mana: Optional[int] = None
    magic_resist: Optional[int] = None
    range: Optional[int] = None
