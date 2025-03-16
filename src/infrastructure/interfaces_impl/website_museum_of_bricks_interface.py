import time
import logging
from datetime import datetime
from application.interfaces.website_interface import WebsiteInterface
from domain.legoset import Legoset
from infrastructure.config.logs_config import log_decorator
from infrastructure.config.repositories_config import lego_sets_repository
from infrastructure.config.selenium_config import get_selenium_driver
import asyncio
import aiohttp
from aiolimiter import AsyncLimiter
from aiohttp.client_exceptions import TooManyRedirects
from bs4 import BeautifulSoup
from icecream import ic


from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

system_logger = logging.getLogger('system_logger')

class WebsiteMuseumOfBricksInterface(WebsiteInterface):

    def __init__(self):
        super().__init__()
        self.driver = None
        self.waiting_time = 0
        self.url = 'https://eshop.museumofbricks.cz'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
        self.response = None

    @log_decorator(print_args=False, print_kwargs=True)
    async def parse_legosets_url(self, legoset_id: str) -> dict | None:
        """
        Функция открывает драйвер браузера, закрывает кукис и вызывает функцию, которая спарсит нужную страницу

        После получения данных, они сохраняются, драйвер закрывается и данные возвращаются

        :return: {"id": str, "url": str, "category": str, "status": int} or None
        """
        result = {}
        start_time = datetime.now()
        driver = None
        try:
            driver = await get_selenium_driver()
            driver.get(self.url)
            await self.__close_cookies(driver=driver)
            result = await self.__parse_legoset_url(legoset_id=legoset_id, driver=driver)

        except Exception as e:
            system_logger.error(e)

        finally:
            driver.close()

        system_logger.info(datetime.now()-start_time)

        return result

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_urls(self, legosets: list[Legoset]) -> list[dict] | None:
        """
        Функция открывает драйвер браузера, закрывает кукис, после чего проходится по каждому лего набору и парсит его url
        Результат сохранятся в отдельный список и потом возвращается

        После получения данных, они сохраняются, драйвер закрывается и данные возвращаются

        :return: list[{"id": str, "url": str, "category": str, "status": int}] or None
        """
        result = []
        start_time_all = datetime.now()
        driver = None
        system_logger.info('Start parsing')
        try:
            driver = await get_selenium_driver()
            driver.get(self.url)
            await self.__close_cookies(driver=driver)
            for legoset in legosets:
                start_time = datetime.now()
                try:
                    result.append(await self.__parse_legoset_url(legoset_id=legoset.id, driver=driver))
                except Exception as e:
                    if "Unable to locate element:" not in str(e):
                        system_logger.error(e)
                system_logger.info(f"One lego set time: {datetime.now() - start_time}")
                system_logger.info('=======================')

        except Exception as e:
            system_logger.error(e)

        finally:
            driver.close()

        system_logger.info(f"All parse time: {datetime.now() - start_time_all}")

        return result



    @log_decorator(print_args=False, print_kwargs=False)
    async def __parse_legoset_url(self, legoset_id: str, driver) -> dict | None:
        """
        Драйвер браузера открывается с главной страницы, потом нажимает на кнопку поиска на странице, вбивает в нее номер
        набора, нажимает кнопку поиска, переходит по первому товару (товар должен быть на странице единственный, так
        как этот ID набора лего уникальный), после открытия страницы, драйвер копирует текущий url страницы, находит
        на нем url_name на чешском и category после чего сохраняет это все в словарь и возвращает обратно

        :return: {"id": str, "url": str, "category": str, "status": int}
        """

        system_logger.info("Start searching for lego sets")
        time.sleep(2)
        system_logger.info(f'current url {driver.current_url}')
        search_element = driver.find_element(By.CSS_SELECTOR, "input[data-testid='searchInput']")


        search_element.clear()
        search_element.send_keys(str(legoset_id))

        search_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='searchBtn']")
        search_button.click()
        try:
            legoset_button = driver.find_element(By.CSS_SELECTOR, "span[data-testid='productCardName']")
            legoset_button.click()
            legoset_url = driver.current_url
            system_logger.info(f"\nLego set: {legoset_id}\nCurent url: {legoset_url}\n===============")
            return {
                "id": legoset_id,
                "url": legoset_url[legoset_url.find(legoset_id) + 6:-1],
                "category": legoset_url[legoset_url.find('lego') + 5 : legoset_url.find(legoset_id) - 1],
                "status": 200,
            }
        except Exception as e:
            system_logger.error(e)
            system_logger.info(f"\nLego set: {legoset_id}\nSet not found\n===============")
            return {
                "id": legoset_id,
                "url": "-",
                "category": "-",
                "status": 404
            }

    @log_decorator(print_args=False, print_kwargs=False)
    async def __close_cookies(self, driver):
        try:
            cookies_button = driver.find_element(
                By.CSS_SELECTOR,
                'button.siteCookies__button.js-cookiesConsentSubmit[data-testid="buttonCookiesAccept"]'
            )
            cookies_button.click()
        except Exception as e:
            print(e)

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_price(self, legoset: Legoset) -> dict | None:
        """
        Функция создает новую сессию в браузере и передает ее в парсер

        После чего возвращает полученную новую цену если она есть

        :return: {"legoset_id": str, "price": str} or None
        """
        async with aiohttp.ClientSession() as session:
            return await self.__get_legosets_price(session=session, legoset=legoset)

    @log_decorator(print_args=False, print_kwargs=False)
    async def parse_legosets_prices(self, legosets: list[Legoset]) -> list[dict] | None:
        """
        Функция создает новую сессию в браузере и передает ее в парсер с дополнительным ограничением в 60 штук,
        чтобы сайт не заподозрил скрипт в DDOS

        После чего возвращает полученные новые цены если они есть в формате списка

        :return: list[{"legoset_id": str, "price": str}] or None
        """
        async with aiohttp.ClientSession() as session:
            rate_limiter = AsyncLimiter(60, 60)
            try:
                async with rate_limiter:
                    tasks = [
                        self.__get_legosets_price(session=session, legoset=legoset) for legoset in legosets
                    ]
                    results = await asyncio.gather(*tasks)
                    return results

            except TooManyRedirects as e:
                print(e)

            return None


    @log_decorator(print_args=False, print_kwargs=False)
    async def __get_legosets_price(self, session: aiohttp.ClientSession, legoset: Legoset) -> dict | None:
        """
        Функция запрашивает у сессии html код определенной страницы, после чего ищет на ней цену,
        сохраняет ее в словарь и возвращает

        :return: {"legoset_id": str, "price": str} or None
        """
        start_time = datetime.now()
        urls = self.__format_legoset_url(legoset=legoset)
        try:
            async for url in urls:
                page = await self.fetch_page(session=session, url=url)

                if page:
                    system_logger.info('-------------------------------------')
                    system_logger.info('Get page: ' + str(datetime.now() - start_time))

                    soup = BeautifulSoup(page, 'lxml')
                    price_element = soup.find('span', class_="price-final-holder")
                    if price_element:
                        price = price_element.get_text(strip=True)
                        system_logger.info(f'Lego set {url[url.rfind("/") + 1:]} exists, price: {price}')
                        return {
                            "legoset_id": legoset.id,
                            "price": price.replace('\xa0', ' ')
                        }
            system_logger.info(f'Legoset {legoset.id} price not found')
        except Exception as e:
            system_logger.error(e)

    async def __format_legoset_url(self, legoset: Legoset):
        """
        Функция возвращает всевозможные комбинации темы, ID и имени наборов для сайта

        yield нужен для того, чтобы при каждом новом запросе к функции возвращалось следующее значение
        """
        legoset_theme = legoset.extendedData.get('cz_category_name')
        if legoset_theme == "None":
            legoset_theme = legoset.theme.lower().replace(' ', '-')
        legoset_url_name = legoset.extendedData.get('cz_url_name')
        if legoset_url_name == "None":
            legoset_url_name = legoset.name.lower().replace(' ', '-').replace('.', '-').replace(':', '-').replace("'", "-")
        if legoset.theme == 'disney':
            yield f"{self.url}/lego---{legoset_theme}-{legoset.id}-{legoset_url_name}"
            yield f"{self.url}/lego---{legoset_theme}-princess-{legoset.id}-{legoset_url_name}"
        yield f"{self.url}/lego-{legoset_theme}-{legoset.id}-{legoset_url_name}"
        yield f"{self.url}/lego-{legoset_theme}--{legoset.id}-{legoset_url_name}"
        yield f"{self.url}/lego-{legoset_theme}-{legoset.id}-{legoset_url_name}"
        yield f"{self.url}/lego--{legoset_theme}--{legoset.id}-{legoset_url_name}"
        yield f"{self.url}/lego-{legoset.id}-{legoset_url_name}"
