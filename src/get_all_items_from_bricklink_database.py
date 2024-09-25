import asyncio
import aiohttp
from datetime import datetime

from oauthlib.common import always_safe
from icecream import ic

from infrastructure.config.gateways_config import bricklink_gateway
from infrastructure.config.repositories_config import lego_sets_repository
from domain.lego_set import LegoSet

async def get_set_items():
    last_datetime = datetime.now()
    log_text = ""

    for i in range(50000, 90000, 500):

        async with aiohttp.ClientSession() as session:
            tasks = [bricklink_gateway.get_item_async(session, 'set', k) for k in range(i, i+500)]
            # Параллельное выполнение всех задач
            results = await asyncio.gather(*tasks)
            # return results
        for index, result in enumerate(results):
            if index % 50 == 0:
                print(log_text[:-1])
                print(datetime.now() - last_datetime)
                print()
                last_datetime = datetime.now()
                log_text = ""

            # result = await bricklink_gateway.get_item('set', i)
            # ic(result)
            if result:
                if result.get('meta').get('code') == 200:
                    lego_set_json_info = result.get('data')
                    year_released = lego_set_json_info.get('year_released')
                    if year_released >= 2010:
                        lego_set = LegoSet(
                            lego_set_id=lego_set_json_info.get('no')[:-2],
                            # images=lego_set_json_info.get(''),
                            images={'1': lego_set_json_info.get('image_url')},
                            name=lego_set_json_info.get('name'),
                            year=lego_set_json_info.get('year_released'),
                            weigh=lego_set_json_info.get('weight'),
                            dimensions={
                                'dim_x': lego_set_json_info.get('dim_x'),
                                'dim_y': lego_set_json_info.get('dim_y'),
                                'dim_z': lego_set_json_info.get('dim_z'),
                            },
                            ages=3,
                        )
                        try:
                            await lego_sets_repository.set_set(lego_set=lego_set)
                        except Exception as e:
                            print(e)
                        log_text += str(lego_set) + '\n'
                    else:
                        # ic(f"Set {i} is to old")
                        log_text += str(f"Set {i+index} is to old. Year: {year_released}") + '\n'
                else:
                    # ic(f"Set {i} is not exist")
                    log_text += str(f"Set {i+index} is not exist. Error: {result.get('meta').get('message')}") + '\n'


async def get_minifig_items():
    for i in range(1, 10):
        item_info = await bricklink_gateway.get_item('MINIFIG', i)
        ic(item_info)


async def get_categories_list():
    result = await bricklink_gateway.get_categories_list()
    ic(result)

async def get_categories():
    result = await bricklink_gateway.get_category(category_id="1306")
    ic(result)

asyncio.run(get_set_items())
# asyncio.run(get_minifig_items())
# asyncio.run(get_categories_list())
# asyncio.run(get_categories())

