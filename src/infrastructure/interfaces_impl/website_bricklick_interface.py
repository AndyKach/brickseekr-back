import requests
from requests import Request
from application.interfaces.bricklink_gateway import BrickLinkGateway
from application.interfaces.website_interface import WebsiteInterface
from infrastructure.config.api_config.bricklink_api_config import bricklink_auth

from icecream import ic

class WebsiteBricklinkInterface(WebsiteInterface):
    def __init__(self):
        self.url = "https://api.bricklink.com/api/store/v1"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9'
        }

    async def parse_legosets_price(self, legoset: str):
        url = self.url + f"/items/set/{legoset}-1"
        response = requests.get(auth=bricklink_auth, url=url)
        # ic(response.json())
        return response.json()

    async def parse_legosets_prices(self, legosets: list):
        results = []
        for item_id in legosets:
            url = self.url + f"/items/set/{item_id}-1"
            response = requests.get(auth=bricklink_auth, url=url)
            # ic(response.json())
            results.append(response.json())

        return results


    async def get_categories_list(self):
        url = self.url + "/categories"
        response = requests.get(auth=bricklink_auth, url=url)
        return response.json()

    async def get_category(self, category_id: str):
        url = self.url + f"/categories/{category_id}"
        response = requests.get(auth=bricklink_auth, url=url)
        return response.json()

    async def get_item_async(self, session, item_type: str, item_id: str):
        url = self.url + f"/items/{item_type}/{item_id}-1"
        headers = self.headers.copy()
        headers['Authorization'] = create_oauth_headers(url, bricklink_auth)

        try:
            async with session.get(url, headers=headers) as response:
                result = await response.json()
                print(result)
                return result
        except Exception as e:
            print(e)


def create_oauth_headers(url, oauth):
    req = Request('GET', url, auth=oauth)
    prepped = req.prepare()
    headers = prepped.headers['Authorization']
    # Возвращаем заголовок Authorization
    return headers.decode('utf-8')

