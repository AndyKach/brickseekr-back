import logging
import time
from datetime import datetime

import requests
import asyncio
import aiohttp
from aiolimiter import AsyncLimiter
from aiohttp.client_exceptions import TooManyRedirects
from bs4 import BeautifulSoup
from icecream import ic
from pygments.lexer import words

from application.interfaces.parser_interface import ParserInterface
from application.interfaces.website_data_source_interface import WebsiteDataSourceInterface
from application.interfaces.website_interface import WebsiteInterface
from application.repositories.legosets_repository import LegoSetsRepository
from application.repositories.prices_repository import LegoSetsPricesRepository
from domain.legoset import LegoSet
from domain.legosets_price import LegoSetsPrice
from domain.strings_tool_kit import StringsToolKit
from infrastructure.config.logs_config import log_decorator
from infrastructure.config.selenium_config import get_selenium_driver
from infrastructure.db.base import session_factory
from selenium.webdriver.common.by import By

system_logger = logging.getLogger("system_logger")

class WebsiteLegoInterface(WebsiteDataSourceInterface, StringsToolKit):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.waiting_time = 2
        self.url = 'https://www.lego.com/en-cz'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None
        self.legosets_repository: LegoSetsRepository = None
        self.legosets_prices_repository: LegoSetsPricesRepository = None
        self.website_id = 1

    async def set_repository(self, legosets_repository: LegoSetsRepository, legosets_prices_repository: LegoSetsPricesRepository):
        self.legosets_repository = legosets_repository
        self.legosets_prices_repository = legosets_prices_repository

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_price(self, legoset: LegoSet):
        url = f"{self.url}/{legoset.lego_set_id}"
        async with aiohttp.ClientSession() as session:
            return await self.__get_item_info_bs4(
                session=session, url=url, item_id=legoset.legoset_id
            )

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_prices(self, legosets: list[LegoSet]):
        async with aiohttp.ClientSession() as session:
            rate_limiter = AsyncLimiter(60, 60)
            try:
                async with rate_limiter:
                    tasks = [
                        self.__get_item_info_bs4(
                            session,
                            url=f"{self.url}/{legoset.lego_set_id}",
                            item_id=legoset.lego_set_id
                        ) for legoset in legosets
                    ]
                    # Параллельное выполнение всех задач
                    results = await asyncio.gather(*tasks)
                    return results

            except TooManyRedirects as e:
                print(e)

            return None

    async def __get_item_info_bs4(self, session, url: str, item_id: str):
        last_datetime = datetime.now()
        try:
            page = await self.fetch_page(session=session, url=url)
            # with open('test1.txt', 'w') as f:
            #     f.write(str(page))

            # ic(page)
            if page:
                system_logger.info('-------------------------------------')
                system_logger.info('Get page: ' + str(datetime.now() - last_datetime))

                soup = BeautifulSoup(page, 'lxml')
                # with open('test2.txt', 'w') as f:
                #     f.write(str(page))
                # ic(soup)
                legoset_price = soup.find('span',
                                          class_='ds-heading-lg ProductPrice_priceText__ndJDK',
                                          attrs={'data-test': 'product-price'})

                legoset_price_sale = soup.find('span',
                                          class_='ProductPrice_salePrice__L9pb9 ds-heading-lg ProductPrice_priceText__ndJDK',
                                          attrs={'data-test': 'product-price-sale'})

                legoset_minifigures_count = soup.find('span',
                                                  class_='Text__BaseText-sc-13i1y3k-0 gbjGsS ProductAttributesstyles__Value-sc-1sfk910-6 CPPEL',
                                                  attrs={'data-test': 'minifigures-value'})

                legoset_pieces_count = soup.find('span',
                                                 class_='',
                                                 attrs={'data-test': ''})

                legoset_min_age = soup.find('span',
                                                 class_='',
                                                 attrs={'data-test': ''})

                legoset_dimensions = soup.find('span',
                                                 class_='',
                                                 attrs={'data-test': ''})

                legoset_description = soup.find('span',)

                for price_element in [legoset_price, legoset_price_sale]:
                    if price_element:
                        price = price_element.get_text(strip=True)
                        system_logger.info(f'Lego set {item_id} exists, price: {price}')
                        return {"lego_set_id": item_id,
                                "price": price.replace('\xa0', ' ')}

                    else:
                        system_logger.info(f'Lego set {item_id} not found')
        except Exception as e:
            print(f"Error: {e}")


        return None
            # ic(price_element.get_text(strip=True))

    async def get_all_info_about_item_bs4(self, item_id: str):
        self.response = requests.get(self.url + item_id)
        soup = BeautifulSoup(self.response.content, 'lxml')
        price_element = soup.find('span',
                                  class_='ds-heading-lg ProductPrice_priceText__ndJDK',
                                  attrs={'data-test': 'product-price'})
        ic(soup)
        ic(price_element)
        if price_element:
            teile = soup.find('div',
                              class_='ProductAttributesstyles__ValueWrapper-sc-1sfk910-5 jNaXJo',
                              attrs={'data-test': "pieces-value"})
            ic(teile)

            element = soup.find('div', {'data-test': 'pieces-value',
                                        'class': 'ProductAttributesstyles__ValueWrapper-sc-1sfk910-5 jNaXJo'})
            ic(element)

    async def fetch_page(self, session, url, limiter_max_rate: int = 60, limiter_time_period: int = 60):
        async with session.get(url, headers=self.headers) as response:
            return await response.text()

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legoset(self, legosets_repository: LegoSetsRepository):
        pass
        # driver = await get_selenium_driver()
        # driver.get(self.url + "/75355")

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets(self, legosets_repository: LegoSetsRepository,
                             legosets_prices_repository: LegoSetsPricesRepository):
        await self.set_repository(legosets_repository, legosets_prices_repository)
        start_time_all = datetime.now()
        driver = await get_selenium_driver()
        driver.get(self.url)


        time.sleep(3)
        system_logger.info("skip_first_button start")

        skip_first_button = driver.find_element(By.CSS_SELECTOR, '#age-gate-grown-up-cta')
        skip_first_button.click()

        system_logger.info("skip_first_button click")
        time.sleep(1)

        cookies_button = driver.find_element(By.XPATH, '/html/body/div[5]/div/aside/div/div/div[3]/div[1]/button[1]')
        cookies_button.click()

        legosets = await legosets_repository.get_all()
        # print(legosets)
        k = 0
        for legoset in legosets[:-4765]:
            k += 1

            # if legoset.id != "75388":
            #     continue
            start_time_this_item = datetime.now()
            system_logger.info(f"Count: {k}")
            system_logger.info('=================================================================================')
            system_logger.info(f"Old version: {legoset}")

            if legoset.images.get('small_image1') is not None:
                system_logger.info(f'Legoset {legoset.id} already parsed')
                continue

            command = await self.parse_legoset_info_from_page(legoset=legoset, driver=driver)
            if command == "Not found":
                system_logger.error(f"Legoset {legoset.id} not found")
            else:
                system_logger.info(f"New version: {legoset}")
                await self.legosets_repository.update_set(legoset=legoset)

            system_logger.info(f'Time for parsing this item: {datetime.now()-start_time_this_item}')

            system_logger.info('=================================================================================')

            time.sleep(2)

        system_logger.info(datetime.now()-start_time_all)

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legoset_info_from_page(self, legoset: LegoSet, driver):
        driver.get(f"{self.url}/product/{legoset.id}")
        time.sleep(3)
        #возраст, количество кусочков, минифигурки, размеры, фотки
        # try:
        system_logger.info("Try to find error button")
        try:
            error_message = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div/header')
            if error_message:
                return "Not found"
        except Exception as e:
            pass

        try:
            try:
                print(1)
                price = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/div[2]/div[2]/div[2]/div/span')
            except Exception as e:
                print(2)
                price = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/div[2]/div[2]/div[2]/div[1]/span[2]')

            system_logger.info(f"price: {price.text}")
            if price.text:
                legoset_price_website_lego = await self.legosets_prices_repository.get_item_price(legoset_id=legoset.id, website_id=self.website_id)
                if legoset_price_website_lego is not None:
                    system_logger.info(f"Legoset: {legoset.id} Value PRICE OLD: {legoset_price_website_lego.price} NEW: {price.text}")
                    await self.legosets_prices_repository.save_price(legoset_id=legoset.id, price=price.text, website_id=self.website_id)
                else:
                    system_logger.info(f"Legoset: {legoset.id} Value PRICE NEW: {price.text}")
                    legoset_price = LegoSetsPrice(legoset_id=legoset.id, price=price.text, website_id=self.website_id)
                    await self.legosets_prices_repository.add_item(legosets_price=legoset_price)
        except Exception as e:
            system_logger.error(e)
            system_logger.error(f"Legoset: {legoset.id} Value PRICE not found")

        try:
            min_age = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/div[1]/section[2]/div/div[1]/div[1]/span/span')
            system_logger.info(f"min_age: {min_age.text}")
            if min_age.text:
                system_logger.info(f"Legoset: {legoset.id} Value MIN_AGE OLD: {legoset.ages_range} NEW: {min_age.text[:-1]}")
                legoset.ages_range['min'] = int(min_age.text[:-1])
                system_logger.info(legoset.ages_range)
        except Exception as e:
            # system_logger.error(e)
            system_logger.error(f"Legoset: {legoset.id} Value MIN_AGE not found")

        try:
            pieces = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/div[1]/section[2]/div/div[2]/div[1]/span/span')
            system_logger.info(f"Pieces: {pieces.text}")
            if pieces.text:
                system_logger.error(f"Legoset: {legoset.id} Value PIECES OLD: {legoset.pieces} NEW: {pieces.text}")
                legoset.pieces = int(pieces.text)
        except Exception as e:
            # system_logger.error(e)
            system_logger.error(f"Legoset: {legoset.id} Value PIECES not found")

        try:
            minifigures_count = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/div[1]/section[2]/div/div[5]/div[1]/span/span')
            system_logger.info(f"Minifigures: {minifigures_count.text}")
            if minifigures_count:
                system_logger.error(f"Legoset: {legoset.id} Value MINIFIGURES OLD: {legoset.minifigures_count} NEW: {minifigures_count.text}")
                legoset.minifigures_count = int(minifigures_count.text)
        except Exception as e:
            # system_logger.error(e)
            system_logger.error(f"Legoset: {legoset.id} Value MINIFIGURES not found")

        # try:
        #     element = driver.find_element(By.XPATH, '')
        #     if element:
        #         system_logger.error(f"Legoset: {legoset.id} Value DIMENSIONS OLD: {} NEW: {element.text}")
        #
        # except Exception as e:
        #     system_logger.error(e)
        #     system_logger.error(f"Legoset: {legoset.id} Value DIMENSIONS not found")

        try:
            description_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[4]/button/div/div/div[1]/h2')
            description_button.click()

            description = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[4]/div/div/div/div/div[1]/div/span/p[1]')
            system_logger.info(f"Description: {description.text}")
            if description.text:
                system_logger.error(f"Legoset: {legoset.id} Value DESCRIPTION OLD: {legoset.description} NEW: {description.text}")
                legoset.description = description.text

        except Exception as e:
            # system_logger.error(e)
            system_logger.error(f"Legoset: {legoset.id} Value DESCRIPTION not found")



        try:
            small_size_params = "?format=webply&fit=bounds&quality=75&width=170&height=170&dpr=1"
            big_size_params = "?format=webply&fit=bounds&quality=75&width=800&height=800&dpr=1"
            image1_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/div[1]/section[1]/ul/li[1]/button/picture/source[1]')
            image1_link = image1_element.get_attribute('srcset').split('?')[0]
            image1_small_link = image1_link + small_size_params
            image1_big_link = image1_link + big_size_params
            system_logger.info(f"Image 1: {image1_small_link}, {image1_big_link}")
            if image1_small_link:
                # system_logger.info(f"Legoset: {legoset.id} Value IMAGES OLD: {legoset.images} ADD Image1: {image1_link}")
                legoset.images['small_image1'] = image1_small_link
                legoset.images['big_image1'] = image1_big_link

            image2_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/div[1]/section[1]/ul/li[2]/button/picture/source[1]')
            image2_link = image2_element.get_attribute('srcset').split('?')[0]
            image2_small_link = image2_link + small_size_params
            image2_big_link = image2_link + big_size_params
            system_logger.info(f"Image 2: {image2_small_link}, {image2_big_link}")
            if image2_link:
                # system_logger.error(f"Legoset: {legoset.id} Value IMAGES OLD: {legoset.images} ADD Image2: {image2_link}")
                legoset.images['small_image2'] = image2_small_link
                legoset.images['big_image2'] = image2_big_link


            image3_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/div[1]/section[1]/ul/li[4]/button/picture/source[1]')
            image3_link = image3_element.get_attribute('srcset').split('?')[0]
            image3_small_link = image3_link + small_size_params
            image3_big_link = image3_link + big_size_params
            system_logger.info(f"Image 3: {image3_small_link}, {image3_big_link}")
            if image3_link:
                # system_logger.error(f"Legoset: {legoset.id} Value IMAGES OLD: {legoset.images} ADD Image3: {image3_link}")
                legoset.images['small_image3'] = image3_small_link
                legoset.images['big_image3'] = image3_big_link


            image4_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/div[1]/section[1]/ul/li[5]/button/picture/source[1]')
            image4_link = image4_element.get_attribute('srcset').split('?')[0]
            image4_small_link = image4_link + small_size_params
            image4_big_link = image4_link + big_size_params
            system_logger.info(f"Image 4: {image4_small_link}, {image4_big_link}")
            if image4_link:
                # system_logger.error(f"Legoset: {legoset.id} Value IMAGES OLD: {legoset.images} ADD Image4: {image4_link}")
                legoset.images['small_image4'] = image4_small_link
                legoset.images['big_image4'] = image4_big_link


            image5_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[1]/div/div[1]/section[1]/ul/li[6]/button/picture/source[1]')
            image5_link = image5_element.get_attribute('srcset').split('?')[0]
            image5_small_link = image5_link + small_size_params
            image5_big_link = image5_link + big_size_params
            system_logger.info(f"Image 5: {image5_small_link}, {image5_big_link}")
            if image5_link:
                # system_logger.error(f"Legoset: {legoset.id} Value IMAGES OLD: {legoset.images} ADD Image5: {image5_link}")
                legoset.images['small_image5'] = image5_small_link
                legoset.images['big_image5'] = image5_big_link

        except Exception as e:
            pass

        return legoset
            # system_logger.error(e)
            # system_logger.error(f"Legoset: {legoset.id} Value I not found")




if __name__ == '__main__':
    lego_parser = WebsiteLegoInterface()
    # asyncio.run(lego_parser.parse_item(item_id='60431'))
    asyncio.run(lego_parser.get_all_info_about_item_bs4(item_id='60431'))
    asyncio.run(lego_parser.get_all_info_about_item_bs4(item_id='61505'))



"""
https://www.lego.com/cdn/cs/set/assets/blt49f484f1e7076fd0/76328_Prod.png?format=webply&fit=bounds&quality=75&width=800&height=800&dpr=1
https://www.lego.com/cdn/cs/set/assets/blt49f484f1e7076fd0/76328_Prod.png?format=webply&fit=bounds&quality=75&width=170&height=170&dpr=1
https://www.lego.com/cdn/cs/set/assets/bltbd5767839cdd0ce2/75331_alt12.png?format=webply&fit=bounds&quality=75&width=800&height=800&dpr=1
https://www.lego.com/cdn/cs/set/assets/bltdbe9230cce3804cf/75331.png?format=webply&fit=bounds&quality=75&width=170&height=170&dpr=1
https://www.lego.com/cdn/cs/set/assets/bltdbe9230cce3804cf/75331.png?format=webply&fit=bounds&quality=75&width=800&height=800&dpr=1






"""
