from app.models.base import SQLModel, Field, Optional, Column, JSON


class ChampionAbilityBase(SQLModel):
    champion_id: int = Field(foreign_key="champion.id")
    name: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    variables: dict = Field(sa_column=Column(JSON))


class ChampionAbility(ChampionAbilityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ChampionAbilityCreate(ChampionAbilityBase):
    pass


class ChampionAbilityRead(ChampionAbilityBase):
    id: int


class ChampionAbilityUpdate(ChampionAbilityBase):
    champion_id: int = Field(foreign_key="champion.id")
    name: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    variables: Optional[dict] = None
