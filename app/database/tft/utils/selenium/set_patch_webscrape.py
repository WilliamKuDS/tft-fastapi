from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
import re

from app.database.tft.crud.patch_service import create_patch, update_patch, PatchAlreadyExistsError
from app.database.tft.crud.set_service import create_set, update_set, SetAlreadyExistsError
from app.database.tft.utils.selenium.browser import load_headless_browser
from app.models.tft.misc.patch import PatchCreate, PatchUpdate
from app.models.tft.misc.set import SetCreate, SetUpdate
from sqlmodel import Session

def webscrape_patch_set(session: Session):
    set_url = 'https://leagueoflegends.fandom.com/wiki/Template:TFT_release_history'
    browser = load_headless_browser()
    browser.get(set_url)
    set_list = webscrape_set_data(browser, session)
    iterate_thru_patches_urls_from_set_ids(set_list, browser, session)


def webscrape_set_data(browser, session: Session):
    wait = WebDriverWait(browser, timeout=5)
    expand_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mw-parser-output')))
    expand_box.find_element(By.TAG_NAME, 'a').click()

    container = browser.find_element(By.CSS_SELECTOR, "table.navbox.hlist")
    set_table = container.find_elements(By.XPATH, './tbody/child::*')
    set_id_list = []

    for curr_set in set_table:
        set_text = curr_set.text.splitlines()[0]

        if 'Upcoming' in set_text:
            continue

        set_info = set_text.split(':', 1)
        set_id = float(set_info[0].strip(' Set '))
        set_name = set_info[1].strip()

        try:
            set_create = SetCreate(set_id=set_id, set_name=set_name)
            create_set(session, set_create)
        except SetAlreadyExistsError:
            set_update = SetUpdate(set_id=set_id, set_name=set_name)
            update_set(session, Decimal(set_id), set_update)
        set_id_list.append(set_id)

    return sorted(set_id_list, reverse=True)


def iterate_thru_patches_urls_from_set_ids(set_id_list, browser, session: Session):
    final_patch_list = []
    for set_id in set_id_list:
        if set_id == Decimal('5.5'):
            continue

        set_id_url = convert_decimal_to_int(set_id)
        browser.get(f"https://leagueoflegends.fandom.com/wiki/Category:Set_{set_id_url}_patch_notes")
        patch_elements = browser.find_elements(By.CSS_SELECTOR, 'a.category-page__member-link')
        patch_urls = [element.get_attribute('href') for element in patch_elements]

        patch_data_list = []
        for patch in patch_urls:
            patch_data = webscrape_patch_data(patch, set_id, browser)
            if patch_data:
                patch_data_list.append(patch_data)

        # Sort patches by date_start
        patch_data_list.sort(key=lambda x: x['date_start'], reverse=True)
        final_patch_list.extend(patch_data_list)

        # Calculate date_end and save patches
    for i, patch_data in enumerate(final_patch_list):
        if i == 0:
            patch_data['date_end'] = None
        else:
            patch_data['date_end'] = final_patch_list[i-1]['date_start'] - timedelta(days=1)

        save_patch_to_db(patch_data, session)


def webscrape_patch_data(patch_page_url, set_id, browser):
    browser.get(patch_page_url)
    patch_dict = {'set_id': set_id}

    patch_info_container = browser.find_element(By.TAG_NAME, 'aside')
    patch_id = patch_info_container.find_element(By.TAG_NAME, 'h2').text.split(' ')[0].strip('V')

    if 'b' in patch_id:
        return None

    if set_id == Decimal('5.0'):
        patch_dict['set_id'] = special_case_for_set_five_because_people_who_manage_websites_hate_us(patch_id)

    patch_dict['patch_id'] = patch_id
    patch_info = patch_info_container.find_elements(By.TAG_NAME, 'section')

    patch_date_unformatted = patch_info[0].text.splitlines()[1]
    match = re.match(r'(\w+)\s(\d+)[a-z]{2},\s(\d{4})', patch_date_unformatted)

    if not match:
        raise ValueError("Date string format is incorrect")

    month, day, year = match.groups()
    patch_dict['date_start'] = datetime.strptime(f"{month} {day}, {year}", "%B %d, %Y").date()
    patch_dict['highlights'] = str(patch_info[1].text.splitlines()[1:])
    patch_dict['patch_url'] = patch_info[2].find_element(By.TAG_NAME, 'a').get_attribute('href')

    return patch_dict


def save_patch_to_db(patch_data, session: Session):
    try:
        patch_create = PatchCreate(
            patch_id=patch_data['patch_id'],
            set_id=patch_data['set_id'],
            date_start=patch_data['date_start'],
            date_end=patch_data['date_end'],
            highlights=patch_data['highlights'],
            patch_url=patch_data['patch_url']
        )
        create_patch(session, patch_create)
    except PatchAlreadyExistsError:
        patch_update = PatchUpdate(
            patch_id=patch_data['patch_id'],
            set_id=patch_data['set_id'],
            date_start=patch_data['date_start'],
            date_end=patch_data['date_end'],
            highlights=patch_data['highlights'],
            patch_url=patch_data['patch_url']
        )
        update_patch(session, patch_data['patch_id'], patch_update)


def convert_decimal_to_int(value):
    return int(value) if value.is_integer() else value


def patch_key(version):
    return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', version)]


def special_case_for_set_five_because_people_who_manage_websites_hate_us(patch_id):
    return Decimal('5.5') if float(patch_id) in [11.15, 11.16, 11.17, 11.18, 11.19, 11.20, 11.21] else Decimal('5.0')
