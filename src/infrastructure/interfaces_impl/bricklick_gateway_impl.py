import requests
from application.interfaces.bricklink_gateway import BrickLinkGateway
from infrastructure.config.api_config.bricklink_api_config import bricklink_auth

from icecream import ic

class BrickLinkGatewayImpl(BrickLinkGateway):
    def __init__(self):
        self.url = "https://api.bricklink.com/api/store/v1"

    async def get_item(self, item_type: str, item_id: str):
        url = self.url + f"/items/{item_type}/{item_id}-1"
        response = requests.get(auth=bricklink_auth, url=url)
        # ic(response.json())
        return response.json()


    async def get_categories_list(self):
        url = self.url + "/categories"
        response = requests.get(auth=bricklink_auth, url=url)
        return response.json()

    async def get_category(self, category_id: str):
        url = self.url + f"/categories/{category_id}"
        response = requests.get(auth=bricklink_auth, url=url)
        return response.json()
