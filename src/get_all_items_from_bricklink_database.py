import asyncio
import time

import aiohttp
from datetime import datetime

from oauthlib.common import always_safe
from icecream import ic
from sqlalchemy.exc import IntegrityError

from infrastructure.config.gateways_config import bricklink_gateway
from infrastructure.config.repositories_config import legosets_repository
from domain.legoset import Legoset

async def get_category_name(category_id: int):
    try:
        result = await bricklink_gateway.get_category(category_id=category_id)
        return result.get('data').get('category_name').replace(' ', '-').lower()
    except:
        return "error_category"

async def get_set_items():
    last_datetime = datetime.now()
    log_text = ""
    for i in range(12000, 100000, 500):
        time.sleep(2)

        async with aiohttp.ClientSession() as session:
            tasks = [bricklink_gateway.get_item_async(session, 'set', k) for k in range(i, i+500)]
            # Параллельное выполнение всех задач
            results = await asyncio.gather(*tasks)
            # return results
        for index, result in enumerate(results):
            if index % 50 == 0:
                print(f"log_text: {log_text[:-1]}")
                print(datetime.now() - last_datetime)
                print()
                last_datetime = datetime.now()
                log_text = ""

            # result = await bricklink_gateway.get_item('set', i)
            # ic(result)
            if result:
                # print(f"Result: {result}")
                if result.get('meta').get('code') == 200:
                    lego_set_json_info = result.get('data')
                    year_released = lego_set_json_info.get('year_released')
                    if year_released >= 2010:
                        lego_set = Legoset(
                            lego_set_id=lego_set_json_info.get('no')[:-2],
                            # images=lego_set_json_info.get(''),
                            images={'1': lego_set_json_info.get('image_url')},
                            name=lego_set_json_info.get('name'),
                            category_name=await get_category_name(lego_set_json_info.get('category_id')),
                            year=lego_set_json_info.get('year_released'),
                            weigh=lego_set_json_info.get('weight'),
                            dimensions={
                                'dim_x': lego_set_json_info.get('dim_x'),
                                'dim_y': lego_set_json_info.get('dim_y'),
                                'dim_z': lego_set_json_info.get('dim_z'),
                            },
                            ages=3,
                        )
                        # print('!!!!!!!!!')
                        # print(lego_set)
                        # print('!!!!!!!!!')
                        try:
                            if await legosets_repository.get_set(set_id=lego_set.lego_set_id) is None:
                                await legosets_repository.set_set(legoset=lego_set)
                            else:
                                await legosets_repository.delete_set(legoset_id=lego_set.lego_set_id)
                                await legosets_repository.set_set(legoset=lego_set)
                        # except IntegrityError as e:
                        except Exception as e:
                            print(f"ERROR: {str(e)[str(e).find('\n')+1:str(e).find('\n', str(e).find('\n')+1)]}")
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
    result = await bricklink_gateway.get_category(category_id="65")
    ic(result)





if __name__ == '__main__':
    start_datetime = datetime.now()

    asyncio.run(get_set_items())

    # asyncio.run(get_minifig_items())
    # asyncio.run(get_categories_list())
    # asyncio.run(get_categories())

    print(f"Time taken: {datetime.now() - start_datetime}")
