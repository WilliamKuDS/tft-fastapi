import requests
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

from sqlmodel import Session, select
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.models.tft.misc.patch import Patch
from cdragon_functions import read_trait_and_add_to_database, read_champion_and_add_to_database, \
    read_item_or_augment_and_add_to_database

# Create a session with retries and connection pooling
session = requests.Session()
retry = Retry(total=3, backoff_factor=0.1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def process_patch(patch):
    patch_id = patch.patch_id

    if patch_id == '9.13':
        return '{} skipped'.format(patch_id)

    if patch.date_end is None:
        url_patch_id = 'latest'
    elif patch_id == '13.2':
        url_patch_id = '13.3'
    elif patch_id == '10.17':
        url_patch_id = '10.18'
    else:
        url_patch_id = patch_id

    set_id, midPatch = int(patch.set_id.set_id), not patch.set_id.set_id.is_integer()

    try:
        tft_patch_data_url = f"https://raw.communitydragon.org/{url_patch_id}/cdragon/tft/en_us.json"
        tft_patch_data_response = session.get(tft_patch_data_url)
        tft_patch_data_response.raise_for_status()
        tft_patch_data_json = tft_patch_data_response.json()

        if not midPatch or set_id == 3:
            mutator_ids = [f'TFTSet{set_id}', f'TFT_Set{set_id}']
        else:
            mutator_ids = [f'TFTSet{set_id}_Stage2', f'TFT_Set{set_id}_Stage2', f'TFTSet{set_id}_Act2']

        if 'setData' in tft_patch_data_json:
            champions_and_traits_data = next(
                (item for item in tft_patch_data_json['setData'] if item.get('mutator') in mutator_ids), None)
        else:
            champions_and_traits_data = tft_patch_data_json['sets'][str(set_id)]

        champion_data = champions_and_traits_data['champions']
        traits_data = champions_and_traits_data['traits']
        augments_and_items_data = tft_patch_data_json['items']

        prev_tft_item_data_json = {}
        try:
            tft_item_url = f"https://raw.communitydragon.org/{url_patch_id}/plugins/rcp-be-lol-game-data/global/default/v1/tftitems.json"
            tft_item_data_response = session.get(tft_item_url)
            tft_item_data_response.raise_for_status()
            new_tft_item_data_json = tft_item_data_response.json()
            tft_item_data_json = new_tft_item_data_json
        except:
            print('No Item JSON for this patch, using previous one')
            tft_item_data_json = prev_tft_item_data_json

        prev_tft_item_data_json = tft_item_data_json

        # Batch processing
        for trait in traits_data:
            read_trait_and_add_to_database(trait, patch_id)
        for champion in champion_data:
            read_champion_and_add_to_database(champion, patch_id)
        for data in augments_and_items_data:
            read_item_or_augment_and_add_to_database(data, patch_id, tft_item_data_json)


    except Exception as e:
        print('{} failed. Error: {}\n{}'.format(url_patch_id, e, traceback.format_exc()))


def get_all_patch_data(db_session: Session):
    patch_list = db_session.exec(select(Patch)).all()

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_patch = {executor.submit(process_patch, patch): patch for patch in patch_list}

        for future in tqdm(as_completed(future_to_patch), total=len(patch_list), desc='Processing patches'):
            patch = future_to_patch[future]
            try:
                future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (patch, exc))

