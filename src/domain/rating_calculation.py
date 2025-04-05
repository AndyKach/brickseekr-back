import logging
import copy
from icecream import ic

from infrastructure.config.logs_config import log_decorator

system_logger = logging.getLogger("system_logger")

class RatingCalculation:
    def __init__(self):
        self.rating_values = {
            "investment_potential": 0,
            "theme_popularity": 0,
            "build_complexity": 0,
            "price_to_piece_ratio": 0,
            "playability": 0,
            "durability": 0,
            "google_rating": 0,
        }

        self.buying_opportunity_weight    = 30
        self.theme_popularity_weight      = 25
        self.price_to_piece_ratio_weight  = 0.2
        self.google_rating_weight         = 5

    @log_decorator(print_args=False, print_kwargs=True)
    async def calculate_rating(
        self, final_price: float, initial_price: float, second_initial_price: float, theme: str, pieces_count: int, google_rating: float, is_legoset_in_few_stores: bool,
        ):
        """
        Основная функция подсчета рейтинга, котоая получает всю нужную информацию о наборе и вызывает все подфункции
        подсчета рейтинга
        """
        # Так как этот класс может использоваться для вычисления сразу нескольких рейтингов одновременно,
        # для каждого набора создается временная переменная, которая хранит значения для вычисления общего рейтинг
        rating_values = copy.deepcopy(self.rating_values)

        if initial_price == 0.0 and second_initial_price == 0.0 and final_price == 0.0:
            return 0.0

        await self.calculate_buying_opportunity_score(rating_values=rating_values, final_price=final_price, initial_price=initial_price, second_initial_price=second_initial_price, is_legoset_in_few_stores=is_legoset_in_few_stores)
        await self.calculate_theme_price_annually_growth(rating_values=rating_values, theme=theme)
        await self.calculate_price_to_piece_ratio(rating_values=rating_values, initial_price=initial_price, pieces_count=pieces_count, second_initial_price=second_initial_price)
        await self.calculate_google_rating(rating_values=rating_values, google_rating=google_rating)

        system_logger.info(f"rating values: {rating_values}")

        result = 0
        for key in rating_values.keys():
            result += rating_values.get(key, 0)
        result = round(result, 2)
        result = result if result <= 100 else 100
        return result

    async def calculate_buying_opportunity_score(self, rating_values: dict, final_price: float, initial_price: float, second_initial_price: float, is_legoset_in_few_stores: bool):
        buying_opportunity_score = 0
        if initial_price == 0.0 and final_price == 0.0:
            buying_opportunity_score = self.buying_opportunity_weight
        elif initial_price != 0.0 and final_price == 0.0:
            buying_opportunity_score = 0.833 * self.buying_opportunity_weight
        elif initial_price == 0.0 and final_price != 0.0 and is_legoset_in_few_stores is False:
            buying_opportunity_score = 0.633 * self.buying_opportunity_weight
        else:
            if initial_price == 0.0 and final_price != 0.0 and is_legoset_in_few_stores is True:
                initial_price = second_initial_price

            buying_opportunity_score = final_price/initial_price * 100
            if buying_opportunity_score <= 0:
                buying_opportunity_score = 0
                system_logger.info(f"Investment potential score: 0")
            else:
                buying_opportunity_score = (buying_opportunity_score/100) * self.buying_opportunity_weight
                system_logger.info(f"Investment potential score: {buying_opportunity_score}")

        rating_values["investment_potential"] = buying_opportunity_score

    async def calculate_theme_price_annually_growth(self, rating_values: dict, theme: str):
        themes_score = {
          "the-legend-of-zelda": 26.66,
          "animal-crossing": 19.2,
          "stranger-things": 18.1,
          "fortnite": 16.6,
          "despicable-me-4": 16.25,
          "lego-forma": 13.3,
          "overwatch": 11.7,
          "vidiyo": 11.4,
          "the-lord-of-the-rings": 10.6,
          "teenage-mutant-ninja-turtles": 10.2,
          "the-hobbit": 10.0,
          "spongebob-squarepants": 9.86,
          "hero-factory": 9.64,
          "scooby-doo": 9.57,
          "spider-man": 9.16,
          "indiana-jones": 9.06,
          "batman": 9.04,
          "mixels": 9.02,
          "bionicle": 8.7,
          "architecture": 8.49,
          "super-mario": 8.46,
          "ghostbusters": 8.39,
          "brickheadz": 8.11,
          "rock-raiders": 7.9,
          "pirates": 7.73,
          "western": 7.68,
          "power-miners": 7.43,
          "castle": 7.35,
          "vikings": 7.3,
          "the-angry-birds-movie": 7.25,
          "advanced-models-(creator-expert)": 7.19,
          "speed-champions": 7.19,
          "ideas": 6.98,
          "pirates-of-the-caribbean": 6.97,
          "adventurers": 6.91,
          "brick-sketches": 6.89,
          "pharaoh's-quest": 6.85,
          "lego-originals": 6.84,
          "exclusive": 6.73,
          "exo-force": 6.71,
          "space": 6.69,
          "monkie-kid": 6.68,
          "star-wars": 6.62,
          "promotional": 6.61,
          "ninjago": 6.55,
          "dreamzzz": 6.51,
          "marvel-super-heroes": 6.49,
          "monster-fighters": 6.38,
          "minions": 6.37,
          "elves": 6.33,
          "dino-2010": 6.29,
          "lego-art": 6.28,
          "ben-10": 6.21,
          "cars": 6.19,
          "minecraft": 6.15,
          "legoland": 6.13,
          "dc-comics-super-heroes": 6.1,
          "classic": 6.08,
          "minifigures": 6.06,
          "aquazone": 6.06,
          "the-lego-ninjago-movie": 6.05,
          "homemaker": 6.02,
          "world-city": 6.01,
          "building-set-with-people": 5.99,
          "fabuland": 5.95,
          "icons": 5.95,
          "dinosaurs": 5.93,
          "the-lone-ranger": 5.92,
          "harry-potter": 5.7,
          "seasonal": 5.65,
          "dino-attack": 5.63,
          "dots": 5.63,
          "xtra": 5.62,
          "the-lego-batman-movie": 5.55,
          "power-functions": 5.5,
          "the-lego-movie": 5.4,
          "duplo": 5.34,
          "the-lego-movie-2-the-second-part": 5.31,
          "aqua-raiders": 5.29,
          "town": 5.23,
          "nexo-knights": 5.2,
          "hobby-set": 5.19,
          "jurassic-world": 5.18,
          "trains": 5.1,
          "boats": 4.97,
          "atlantis": 4.94,
          "serious-play": 4.92,
          "galidor": 4.9,
          "dino": 4.89,
          "mickey-mouse": 4.88,
          "4-juniors": 4.88,
          "juniors": 4.85,
          "primo": 4.76,
          "toy-story": 4.75,
          "agents": 4.75,
          "disney": 4.78,
          "city": 4.62,
          "wicked": 4.6,
          "botanical-collection": 4.6,
          "technic": 4.13,
          "friends": 3.92,
          "sonic-the-hedgehog": 2.92,
          "wednesday": 2.21
        }
        score = themes_score.get(theme  , 0)
        system_logger.info(f"Themes score: {score}")
        rating_values["theme_popularity"] = (score/26.66) * self.theme_popularity_weight

    async def calculate_price_to_piece_ratio(self, rating_values: dict, initial_price: float, pieces_count: int, second_initial_price: float):
        price = 0.0
        if initial_price != 0.0:
            price = initial_price
        elif second_initial_price != 0.0:
            price = second_initial_price

        if price != 0.0:
            PPR = price / pieces_count
            score = 0
            match PPR:
                case PPR if PPR <= 1.38:
                    score = 100
                case PPR if 1.39 <= PPR <= 3.22:
                    score = 75
                case PPR if 3.23 <= PPR <= 4.37:
                    score = 50
                case PPR if 4.38 <= PPR:
                    score = 25
        else:
            score = 0

        system_logger.info(f"PPR: {PPR} score: {score}")
        rating_values["price_to_piece_ratio"] = score * self.price_to_piece_ratio_weight

    async def calculate_google_rating(self, rating_values: dict, google_rating: float):
        rating_values["google_rating"] = int(google_rating * self.google_rating_weight)
