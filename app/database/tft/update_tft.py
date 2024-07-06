from sqlmodel import Session

from app.database.tft.utils.others.regions import insert_region
from app.database.tft.utils.selenium.set_patch_webscrape import webscrape_patch_set


def fetch_and_process_tft_data(session: Session):
    # Web scrapes League Wiki for all Sets and Patches, and add/updates them
    webscrape_patch_set(session)
    # Hardcoded region codes added/updates to database **MAY CHANGE TO WEB SCRAPE**
    insert_region(session)
