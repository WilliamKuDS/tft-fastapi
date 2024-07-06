from sqlmodel import Session

from app.database.tft.crud.account.region_service import create_region, RegionAlreadyExistsError, update_region
from app.models.account.region import RegionCreate, RegionUpdate

regions = [
    {"label": "NA", "region_id": "na", "server": "na1", "description": "North America"},
    {"label": "EUW", "region_id": "euw", "server": "euw1", "description": "Europe West"},
    {"label": "EUNE", "region_id": "eun", "server": "eun1", "description": "Europe Nordic & East"},
    {"label": "KR", "region_id": "kr", "server": "kr", "description": "Republic of Korea"},
    {"label": "JP", "region_id": "jp", "server": "jp1", "description": "Japan"},
    {"label": "OCE", "region_id": "oce", "server": "oc1", "description": "Oceania"},
    {"label": "TW", "region_id": "tw", "server": "tw2", "description": "Taiwan, Hong Kong, and Macao"},
    {"label": "PH", "region_id": "ph", "server": "ph2", "description": "The Philippines"},
    {"label": "SG", "region_id": "sg", "server": "sg2", "description": "Singapore, Malaysia, & Indonesia"},
    {"label": "TH", "region_id": "th", "server": "th2", "description": "Thailand"},
    {"label": "VN", "region_id": "vn", "server": "vn2", "description": "Vietnam"},
    {"label": "BR", "region_id": "br", "server": "br1", "description": "Brazil"},
    {"label": "LAN", "region_id": "lan", "server": "la1", "description": "Latin America North"},
    {"label": "LAS", "region_id": "las", "server": "la2", "description": "Latin America South"},
    {"label": "RU", "region_id": "ru", "server": "ru1", "description": "Russia"},
    {"label": "TR", "region_id": "tr", "server": "tr1", "description": "Turkey"},
]


def insert_region(session: Session):
    for region_data in regions:
        try:
            region = RegionCreate(**region_data)
            create_region(session, region)
        except RegionAlreadyExistsError:
            region_id = region_data.pop("region_id")
            region = RegionUpdate(**region_data)
            update_region(session, region_id, region)
