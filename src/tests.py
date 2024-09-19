import asyncio

from infrastructure.config.services_config import get_lego_sets_service

lego_sets_service = get_lego_sets_service()

if __name__ == '__main__':

    asyncio.run(lego_sets_service.parse_all_sets())
