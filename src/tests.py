# import asyncio
#
# from domain.lego_sets_prices import LegoSetsPrices
# from infrastructure.config.services_config import get_lego_sets_service
# from infrastructure.db.models.prices_orm import LegoSetsPricesOrm
#
# lego_sets_service = get_lego_sets_service()
#
# from infrastructure.config.repositories_config import lego_sets_prices_repository
#
# if __name__ == '__main__':
#     # new_item = LegoSetsPricesOrm(
#     #     lego_set_id="LEGO-1234",
#     #     prices={
#     #         "website_1": 179.99,
#     #         "website_2": 185.50,
#     #         "website_3": 190.00
#     #     }
#     # )
#     # asyncio.run(prices_repository.add_item(new_item))
#     # asyncio.run(prices_repository.add_item(new_item))
#
#     new_price = 14341
#     website_id = 'website_1'
#
#     asyncio.run(lego_sets_prices_repository.save_price(item_id='LEGO-1234', price=new_price, website_id=website_id))


print(123, '213', ('eqw', 123), [123, 'das'])
x = ['dasd', 123]

len(x)

y = "sdfsdfs"

print(y.upper())
print(y.lower())
print(str(x), len(str(x)))
print(str({"1": 15, "2":40}), len(str({"1": 15, "2":40})))
print(str([1, '3', (2.5, 18)]), len(str([1, '3', (2.5, 18)])))