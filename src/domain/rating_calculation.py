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

        self.investment_potential_weight  = 0.25
        self.theme_popularity_weight      = 0.2
        self.build_complexity_weight      = 0.1
        self.price_to_piece_ratio_weight  = 0.15
        self.playability_weight           = 0.1
        self.durability_weight            = 0.05
        self.google_rating_weight         = 3

    @log_decorator(print_args=False, print_kwargs=True)
    async def calculate_rating(self,
                               final_price: float, initial_price: float, years_since_release: float, theme: str,
                               pieces_count: int, best_ratio: float, worst_ratio: float, google_rating: float,
                         ):
        # Так как этот класс может использоваться для вычисления сразу нескольких рейтингов одновременно,
        # для каждого набора создается временная переменная, которая хранит значения для вычисления общего рейтинг
        rating_values = copy.deepcopy(self.rating_values)
        system_logger.info(f"rating values: {rating_values}")

        await self.calculate_investment_potential(rating_values=rating_values, final_price=final_price, initial_price=initial_price, years_since_release=years_since_release)
        await self.calculate_theme_popularity(rating_values=rating_values, theme=theme)
        await self.calculate_build_complexity(rating_values=rating_values, pieces_count=pieces_count)
        await self.calculate_price_to_piece_ratio(rating_values=rating_values, initial_price=initial_price, best_ratio=best_ratio, worst_ratio=worst_ratio, pieces_count=pieces_count)
        await self.calculate_playability(rating_values=rating_values, theme=theme)
        await self.calculate_durability(rating_values=rating_values, theme=theme)
        await self.calculate_google_rating(rating_values=rating_values, google_rating=google_rating)

        system_logger.info(f"rating values: {rating_values}")

        result = 0
        for key in rating_values.keys():
            result += rating_values.get(key, 0)
        ic(f"result: {result}")
        return result

    async def calculate_investment_potential(self, rating_values: dict, final_price: float, initial_price: float, years_since_release: float):
        score = (1 - (final_price/initial_price)**(1/years_since_release)) * 100

        system_logger.info(f"Investment potential CAGR: {score}")
        rating_values["investment_potential"] = score * self.investment_potential_weight

    async def calculate_theme_popularity(self, rating_values: dict, theme: str):
        themes_score = {
            'star-wars': 100,
            'harry-potter': 95,
            'lego-icons': 95,
            'creator-expert': 90,
            'technic': 90,
            'marvel super-heroes': 85,
            'lego ideas': 85,
            'architecture': 85,
            'the-legend-of-zelda': 90,
            'ninjago': 85,
            'dc super-heroes': 85,
            'batman': 85,
            'jurassic world': 85,
            'pirates': 85,
            'castle': 85,
            "speed-champions": 80,
            "city": 80,
            "minecraft": 80,
            "the-simpsons": 35,  #
            "the-hobbit": 80,
            "the-lego-movie": 80,
            "sonic-the-hedgehog": 75,
            "spider-man": 75,
            "avatar": 75,
            "avatar:-the-last-airbender": 50,
            "indiana-jones": 75,
            "disney": 70,
            "friends": 70,
            "super-mario": 70,
            "wednesday": 70,
            "wicked": 70,
            "animal-crossing": 65,
            "the-angry-birds-movie": 10,
            "the-powerpuff-girls": 10,
            "classic": 65,
            "botanical-collection": 65,
            "minifigures": 60,
            "minions": 60,
            "how-to-train-your-dragon": 60,
            "overwatch": 60,
            "horizon-adventures": 60,
            "transformers": 60,
            "star-trek": 60,
            "dreamzzz": 55,
            "the-muppets": 55,
            "looney-tunes": 55,
            "despicable-me": 55,
            "stranger-things": 55,
            "jurassic-world": 55,
            "elves": 50,
            "ultra-agents": 50,
            "lego-dimensions": 50,
            "trolls-world-tour": 10,
            "the-lego-movie-2": 50,
            "monkie-kid": 45,
            "duplo": 45,
            "lego-art": 45,
            "fabuland": 45,
            "xtra": 45,
            "bricks-&-more": 45,
            "sports": 45,
            "lego-education": 45,
            "hidden-side": 40,
            "bionicle": 40,
            "pharaoh's-quest": 40,
            "time-cruisers": 40,
            "town": 40,
            "space": 40,
            "western": 40,
            "scooby-doo": 35,
            "next-knights": 35,
            "belville": 35,
            "model-team": 35,
            "vikings": 30,
            "jack-stone": 30,
            "aquazone": 30,
            "alpha-team": 30,
            "racers": 30,
            "speed-racer": 30,
            "rock-raiders": 30,
            "atlantis": 30,
            "spongebob-squarepants": 30,
            "agents": 30,
            "lego-horizon-adventures": 30,
            "lego-games": 30,
            "factory": 25,
            "make-&-create": 25,
            "discovery": 25,
            "dino-attack": 25,
            "dinosaurs": 25,
            "first-lego-league": 25,
            "freestyle": 25,
            "studios": 25,
            "bulk-bricks": 25,
            "lego-forma": 10,
            "lego-serious-play": 20,
            "lego-powered-up": 20,
            "braille-bricks": 20,
            "lego-gabby’s-dollhouse": 20,
            "unikitty!": 20,
            "4+": 20,
            "island-xtreme-stunts": 20,
            "brickheadz": 15,
            "lego-unikitty": 15,
            "one-piece": 15,
            "radio-control": 15,
            "bluey": 10,
            "lego-xtra": 5
        }

        score = themes_score.get(theme  , 0)
        system_logger.info(f"Themes score: {score}")
        rating_values["theme_popularity"] = score * self.theme_popularity_weight

    async def calculate_build_complexity(self, rating_values: dict, pieces_count: int):
        pieces_score = 0
        match pieces_count:
            case pieces_count if 0 < pieces_count <= 100:
                pieces_score = 10
            case pieces_count if 101 <= pieces_count <= 500:
                pieces_score = 30
            case pieces_count if 501 <= pieces_count <= 1000:
                pieces_score = 50
            case pieces_count if 1001 <= pieces_count <= 200:
                pieces_score = 70
            case pieces_count if 2001 < pieces_count <= 3000:
                pieces_score = 85
            case pieces_count if 3001 <= pieces_count:
                pieces_score = 100

        system_logger.info(f"Build complexity score: {pieces_score}")
        rating_values["build_complexity"] = pieces_score * self.build_complexity_weight

    async def calculate_price_to_piece_ratio(self, rating_values: dict, initial_price: float, best_ratio: float, worst_ratio: float, pieces_count: int):
        # ic(initial_price)
        # ic(best_ratio)
        # ic(worst_ratio)
        # ic(pieces_count)
        # PPR  = initial_price / pieces_count
        # BPPR = best_ratio    / pieces_count
        # WPPR = worst_ratio   / pieces_count
        # ic(PPR)
        # ic(BPPR)
        # ic(WPPR)

        PPR = initial_price / pieces_count
        score = 0
        match PPR:
            case PPR if         PPR <= 1.15:
                score = 100
            case PPR if 1.16 <= PPR <= 1.85:
                score = 80
            case PPR if 1.86 <= PPR <= 2.30:
                score = 60
            case PPR if 2.31 <= PPR <= 3.00:
                score = 40
            case PPR if 3.01 <= PPR <= 3.70:
                score = 20
            case PPR if 3.91 <= PPR:
                score = 0

        system_logger.info(f"PPR: {PPR} score: {score}")
        rating_values["price_to_piece_ratio"] = score * self.price_to_piece_ratio_weight

    async def calculate_playability(self, rating_values: dict, theme: str):
        playability_scores = {
            "town": 100,
            "technic": 100,
            "super-mario": 100,
            "radio-control": 100,
            "minecraft": 100,
            "make-&-create": 100,
            "lego-serious-play": 100,
            "lego-powered-up": 100,
            "lego-games": 100,
            "lego-education": 100,
            "jack-stone": 100,
            "friends": 100,
            "freestyle": 100,
            "first-lego-league": 100,
            "duplo": 100,
            "dreamzzz": 100,
            "classic": 100,
            "city": 100,
            "bulk-bricks": 100,
            "bricks-&-more": 100,
            "braille-bricks": 100,
            "belville": 100,
            "4+": 100,
            "western": 80,
            "vikings": 80,
            "unikitty!": 80,
            "ultra-agents": 80,
            "trolls-world-tour": 80,
            "transformers": 80,
            "time-cruisers": 80,
            "the-powerpuff-girls": 80,
            "the-muppets": 80,
            "the-lego-movie-2": 80,
            "the-lego-movie": 80,
            "studios": 80,
            "star-wars": 80,
            "sports": 80,
            "spongebob-squarepants": 80,
            "spider-man": 80,
            "speed-racer": 80,
            "space": 80,
            "sonic-the-hedgehog": 80,
            "scooby-doo": 80,
            "rock-raiders": 80,
            "racers": 80,
            "pirates": 80,
            "pharaoh's-quest": 80,
            "ninjago": 80,
            "next-knights": 80,
            "monkie-kid": 80,
            "minions": 80,
            "minifigures": 80,
            "marvel-super-heroes": 80,
            "looney-tunes": 80,
            "lego-unikitty": 80,
            "lego-gabby’s-dollhouse": 80,
            "lego-dimensions": 80,
            "jurassic-world": 80,
            "island-xtreme-stunts": 80,
            "indiana-jones": 80,
            "how-to-train-your-dragon": 80,
            "hidden-side": 80,
            "harry-potter": 80,
            "fabuland": 80,
            "elves": 80,
            "dinosaurs": 80,
            "dino-attack": 80,
            "despicable-me": 80,
            "dc-super-heroes": 80,
            "castle": 80,
            "bluey": 80,
            "bionicle": 80,
            "batman": 80,
            "atlantis": 80,
            "aquazone": 80,
            "animal-crossing": 80,
            "alpha-team": 80,
            "agents": 80,
            "xtra": 60,
            "wicked": 60,
            "wednesday": 60,
            "the-simpsons": 60,
            "the-legend-of-zelda": 60,
            "the-hobbit": 60,
            "the-angry-birds-movie": 60,
            "stranger-things": 60,
            "star-trek": 60,
            "speed-champions": 60,
            "overwatch": 60,
            "one-piece": 60,
            "lego-xtra": 60,
            "lego-ideas": 60,
            "lego-horizon-adventures": 60,
            "horizon-adventures": 60,
            "factory": 60,
            "disney": 60,
            "discovery": 60,
            "avatar:-the-last-airbender": 60,
            "avatar": 60,
            "model-team": 40,
            "lego-icons": 40,
            "lego-forma": 40,
            "creator-expert": 40,
            "architecture": 20,
            "lego-art": 10,
            "brickheadz": 10,
            "botanical-collection": 10
        }
        system_logger.info(f"Theme: {theme}")
        score = playability_scores.get(theme, 0)

        system_logger.info(f"Playability score: {score}")
        rating_values["playability"] = score * self.playability_weight

    async def calculate_durability(self, rating_values: dict, theme: str):
        durability_scores = {
            "duplo": 100,
            "freestyle": 100,
            "super-mario": 100,
            "braille-bricks": 100,
            "lego-powered-up": 100,
            "animal-crossing": 100,
            "classic": 100,
            "lego-serious-play": 100,
            "bulk-bricks": 100,
            "dreamzzz": 100,
            "4+": 100,
            "make-&-create": 100,
            "bricks-&-more": 100,
            "lego-education": 100,
            "town": 100,
            "belville": 100,
            "lego-games": 100,
            "jack-stone": 100,
            "friends": 100,
            "first-lego-league": 100,
            "minecraft": 100,
            "city": 100,
            "technic": 100,
            "radio-control": 100,
            "time-cruisers": 80,
            "pharaoh's-quest": 80,
            "bionicle": 80,
            "hidden-side": 80,
            "bluey": 80,
            "the-lego-movie": 80,
            "space": 80,
            "sports": 80,
            "trolls-world-tour": 80,
            "fabuland": 80,
            "monkie-kid": 80,
            "dino-attack": 80,
            "marvel-super-heroes": 80,
            "scooby-doo": 80,
            "western": 80,
            "sonic-the-hedgehog": 80,
            "next-knights": 80,
            "the-powerpuff-girls": 80,
            "vikings": 80,
            "the-angry-birds-movie": 80,
            "aquazone": 80,
            "alpha-team": 80,
            "racers": 80,
            "speed-racer": 80,
            "rock-raiders": 80,
            "atlantis": 80,
            "spongebob-squarepants": 80,
            "the-lego-movie-2": 80,
            "lego-dimensions": 80,
            "minions": 80,
            "spider-man": 80,
            "island-xtreme-stunts": 80,
            "unikitty!": 80,
            "indiana-jones": 80,
            "lego-gabby‚äôs-dollhouse": 80,
            "lego-unikitty": 80,
            "speed-champions": 80,
            "castle": 80,
            "pirates": 80,
            "jurassic-world": 80,
            "minifigures": 80,
            "how-to-train-your-dragon": 80,
            "ultra-agents": 80,
            "batman": 80,
            "studios": 80,
            "dc-super-heroes": 80,
            "the-muppets": 80,
            "looney-tunes": 80,
            "despicable-me": 80,
            "dinosaurs": 80,
            "elves": 80,
            "agents": 80,
            "lego-horizon-adventures": 60,
            "one-piece": 60,
            "factory": 60,
            "discovery": 60,
            "lego-xtra": 60,
            "model-team": 60,
            "wednesday": 60,
            "lego-icons": 60,
            "creator-expert": 60,
            "lego-ideas": 60,
            "the-legend-of-zelda": 60,
            "ninjago": 60,
            "the-simpsons": 60,
            "the-hobbit": 60,
            "avatar": 60,
            "avatar:-the-last-airbender": 60,
            "xtra": 60,
            "disney": 60,
            "wicked": 60,
            "overwatch": 60,
            "horizon-adventures": 60,
            "transformers": 60,
            "star-trek": 60,
            "stranger-things": 60,
            "harry-potter": 60,
            "lego-forma": 40,
            "star-wars": 40,
            "botanical-collection": 20,
            "brickheadz": 20,
            "architecture": 20,
            "lego-art": 20
        }
        score = durability_scores.get(theme, 0)
        system_logger.info(f"Durability score: {score}")
        rating_values["durability"] = score * self.durability_weight

    async def calculate_google_rating(self, rating_values: dict, google_rating: float):
        rating_values["google_rating"] = int(google_rating * self.google_rating_weight)
