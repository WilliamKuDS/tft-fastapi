# app/models.py
# Account Models
from app.models.account.account import Account
from app.models.account.region import Region
from app.models.account.summoner import Summoner
from app.models.account.league import League
from app.models.account.summoner_league import SummonerLeague

# TFT Models
from app.models.tft.misc.companion import Companion
from app.models.tft.misc.set import Set
from app.models.tft.misc.patch import Patch
from app.models.tft.game.trait import Trait
from app.models.tft.game.trait_effect import TraitEffect
from app.models.tft.game.champion import Champion
from app.models.tft.game.champion_ability import ChampionAbility
from app.models.tft.game.champion_stats import ChampionStats
from app.models.tft.game.item import Item
from app.models.tft.game.augment import Augment
from app.models.tft.game.miscellaneous import Miscellaneous
from app.models.tft.match.match import Match
from app.models.tft.match.match_summoner import MatchSummoner

# Baseline Model
from app.models.base import SQLModel
