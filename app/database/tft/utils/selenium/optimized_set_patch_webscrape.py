from decimal import Decimal
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, \
    StaleElementReferenceException, NoSuchElementException
from datetime import datetime, timedelta
import re
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import time
from app.database.tft.crud.patch_service import create_patch, update_patch, PatchAlreadyExistsError
from app.database.tft.crud.set_service import create_set, update_set, SetAlreadyExistsError
from app.database.tft.utils.selenium.browser import optimized_browser
from app.models.tft.misc.patch import PatchCreate, PatchUpdate
from app.models.tft.misc.set import SetCreate, SetUpdate
from sqlmodel import Session


def custom_wait(browser, locator, timeout=10, poll_frequency=0.5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = browser.find_element(*locator)
            if element.is_displayed():
                return element
        except (TimeoutException, StaleElementReferenceException):
            pass
        time.sleep(poll_frequency)
        poll_frequency *= 1.5  # Exponential backoff
    raise TimeoutException(f"Element {locator} not found within {timeout} seconds")


def webscrape_patch_set(session: Session):
    set_url = 'https://leagueoflegends.fandom.com/wiki/Template:TFT_release_history'
    with optimized_browser() as browser:
        browser.get(set_url)
        set_list = webscrape_set_data(browser, session)
        iterate_thru_patches_urls_from_set_ids(set_list, browser, session)


def webscrape_set_data(browser, session: Session):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Wait for the expand box to be present
            expand_box = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mw-parser-output'))
            )

            # Find the 'a' element and wait for it to be clickable
            expand_link = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.mw-parser-output a'))
            )

            # Try to click the element
            try:
                expand_link.click()
            except ElementClickInterceptedException:
                # If normal click fails, try JavaScript click
                browser.execute_script("arguments[0].click();", expand_link)

            # Wait for the table to be visible after expanding
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "table.navbox.hlist"))
            )

            container = custom_wait(browser, (By.CSS_SELECTOR, "table.navbox.hlist"))
            set_rows = container.find_elements(By.XPATH, './tbody/tr')
            set_id_list = []

            for row in set_rows:
                set_text = row.text.strip()
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

        except (ElementClickInterceptedException, TimeoutException) as e:
            if attempt == max_retries - 1:
                raise  # Re-raise the last exception if all retries failed
            else:
                print(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(2)  # Wait for 2 seconds before retrying
                browser.refresh()  # Refresh the page before retrying


def iterate_thru_patches_urls_from_set_ids(set_id_list, browser, session: Session):
    patch_data_list = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for set_id in set_id_list:
            if set_id == Decimal('5.5'):
                continue
            set_id_url = convert_decimal_to_int(set_id)
            url = f"https://leagueoflegends.fandom.com/wiki/Category:Set_{set_id_url}_patch_notes"
            futures.append(executor.submit(scrape_patches_for_set, url, set_id, browser))

        for future in futures:
            patch_data_list.extend(future.result())

    patch_data_list.sort(key=lambda x: x['date_start'], reverse=True)

    patches_to_save = []
    for i, patch_data in enumerate(patch_data_list):
        if i == 0:
            patch_data['date_end'] = None
        else:
            patch_data['date_end'] = patch_data_list[i - 1]['date_start'] - timedelta(days=1)
        patches_to_save.append(patch_data)

    save_patches_to_db(patches_to_save, session)


def scrape_patches_for_set(url, set_id, browser):
    browser.get(url)
    patch_data_list = []
    try:
        # Wait for the container of patch links to be present
        patch_container = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mw-category-group'))
        )

        # Find all patch links within the container
        patch_elements = patch_container.find_elements(By.CSS_SELECTOR, 'a.category-page__member-link')

        if not patch_elements:
            print(f"No patch elements found for set {set_id}")
            return patch_data_list

        patch_urls = [element.get_attribute('href') for element in patch_elements]

        for patch_url in patch_urls:
            patch_data = webscrape_patch_data(patch_url, set_id, browser)
            if patch_data:
                patch_data_list.append(patch_data)

    except TimeoutException:
        print(f"Timeout while loading patch elements for set {set_id}")
    except NoSuchElementException:
        print(f"Could not find patch elements container for set {set_id}")
    except Exception as e:
        print(f"An error occurred while scraping patches for set {set_id}: {str(e)}")

    return patch_data_list


@lru_cache(maxsize=128)
def webscrape_patch_data(patch_page_url, set_id, browser):
    try:
        browser.get(patch_page_url)
        # Wait for the main content to load
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'aside'))
        )

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

    except Exception as e:
        print(f"Error scraping patch data from {patch_page_url}: {str(e)}")
        return None


def save_patches_to_db(patches, session: Session):
    for patch_data in patches:
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
    session.commit()


def convert_decimal_to_int(value):
    return int(value) if value.is_integer() else value


def special_case_for_set_five_because_people_who_manage_websites_hate_us(patch_id):
    return Decimal('5.5') if float(patch_id) in [11.15, 11.16, 11.17, 11.18, 11.19, 11.20, 11.21] else Decimal('5.0')