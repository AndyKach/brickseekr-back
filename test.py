# from html import unescape
# from bricklink_py import bricklink
import aiohttp
from icecream import ic
url = 'https://api.bricklink.com/api/store/v1'


from requests_oauthlib import OAuth1
import requests
# consumer_key=str('2EA56244361B4924B616D635C4773B17')
# consumer_secret=str('4E395498492342FD901881438CA4E10D')
# oauth_token=str('24C230F739F845FABF99CA84C14316D3')
# oauth_token_secret=str('6378711AE8924CF78C46135C5CB37D7E')
# auth = OAuth1(consumer_key, consumer_secret, oauth_token, oauth_token_secret)

get_categories_url = url + '/colors'
# print(get_categories_url)
# print(type(get_categories_url))
# response = requests.get(get_categories_url, auth=auth)

get_adidas_url = url + '/items/set/40486-1'
ic(get_adidas_url)
# response = requests.get(get_adidas_url, auth=auth)


# ic(response.json())

# async with aiohttp.ClientSession() as session:
#     async with session.get(
#             url=url + f"/canteen{canteen_id}/getDishes",
#     ) as resp:
#         pass
#
# '''
# https://api.bricklink.com/api/store/v1/orders?direction=in
# &Authorization=%7B%22
# oauth_signature%22%3A%22KVkfRqcGuEpqN7%252F57aLZVi9lS9k%3D%22%2C%22
# oauth_nonce%22%3A%22flBnl2yp3vk%22%2C%22
# oauth_version%22%3A%221.0%22%2C%22
# oauth_consumer_key%22%3A%227CCDCEF257CF43D89A74A7E39BEAA1E1%22%2C%22
# oauth_signature_method%22%3A%22HMAC-SHA1%22%2C%22oauth_token%22%3A%22AC40C8C32A1748E0AE1EFA13CCCFAC3A%22%2C%22oauth_timestamp%22%3A%221397119302%22%7D
# '''
#
# # create session object
# session = bricklink.Bricklink(
#             consumer_key='2EA56244361B4924B616D635C4773B17',
#             consumer_secret='4E395498492342FD901881438CA4E10D',
#             token='CDBADE22B34D43FEA98C2E5C4AC00FBA',
#             token_secret='373CF485FD884A8BBC9FFB4C9056164E'
#             )

# Price checker example
# set_no = '75281-1'
#
# set_item = session.catalog_item.get_item('SET', set_no)
# print(set_item)
# set_name = unescape(set_item['name'])
# set_weight = set_item['weight']
# year_released = set_item['year_released']
#
# price_guide = session.catalog_item.get_price_guide('SET', set_no,
#                                                    guide_type='sold')
# avg_price = float(price_guide['avg_price'])
# currency = price_guide['currency_code']
#
# print(f'The "{set_name}" set was released in {year_released}.')
# print(f'It weights {set_weight}gr.')
# print(f'Average sold price for last 6 months: {avg_price:.2f} {currency}')