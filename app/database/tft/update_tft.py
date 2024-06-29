from sqlmodel import Session
from app.database.tft.utils.selenium.set_patch_webscrape import webscrape_patch_set


def fetch_and_process_tft_data(session: Session):
    webscrape_patch_set(session)