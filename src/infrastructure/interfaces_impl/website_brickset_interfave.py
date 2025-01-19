from datetime import datetime
import time
import os
import aiohttp
import asyncio
import json
from icecream import ic
from dotenv import load_dotenv

from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.interfaces.website_interface import WebsiteInterface
from domain.strings_tool_kit import StringsToolKit
from infrastructure.config.logs_config import log_decorator
from domain.lego_set import LegoSet

load_dotenv()

class WebsiteBricksetInterface(WebsiteDataSourceInterface, StringsToolKit):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.waiting_time = 2
        self.url = "https://brickset.com"
        self.url_api = "https://brickset.com/api/v3.asmx"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_all_legosets(self):
        last_datetime = datetime.now()
        log_text = ""

        results = []
        for i in range(40000, 40005, 10):
            time.sleep(2)

            async with aiohttp.ClientSession() as session:
                tasks = [self.request_get_legoset(session=session, legoset_id=k) for k in range(i, i + 1)]
                # Параллельное выполнение всех задач
                results = await asyncio.gather(*tasks)

            for index, result in enumerate(results):
                legoset_json = result.get('sets')[0]
                legoset = LegoSet(
                    lego_set_id=legoset_json['number'],
                    images=legoset_json['image'],
                    name=legoset_json['name'],
                    # category_name=legoset_json[]
                )
                print(legoset)
                if index % 50 == 0:
                    print(f"log_text: {log_text[:-1]}")
                    print(datetime.now() - last_datetime)
                    print()
                    last_datetime = datetime.now()
                    log_text = ""
                if result:
                    print(f"Result Success: {result}")
                else:
                    print(f"Result Error: {result}")

            break


    @log_decorator(print_args=False, print_kwargs=False)
    async def request_get_legoset(self, session: aiohttp.ClientSession, legoset_id):
        url = f"{self.url_api}/getSets"
        params = {
            'apiKey': os.getenv("BRICKSET_API_TOKEN"),
            'userHash': os.getenv("BRICKSET_USER_HASH"),
            'params': json.dumps({'setNumber': f"{legoset_id}-1"})
        }
        print(params, "!!!!")
        # try:
        async with session.get(url=url, headers=self.headers, params=params) as response:
            # result = await response.json()
            # print(response.json())
            response_text = await response.text()
            print(response_text)
            response_json = json.loads(response_text)
            # print(response_json)
            return response_json
            # print(result)
            # return result
        # except Exception as e:
        #     print(e)
