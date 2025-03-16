from infrastructure.db.base import Base, sync_engine
from infrastructure.db.models.legosets_orm import LegosetsOrm
from infrastructure.db.models.websites_orm import WebsitesOrm
from infrastructure.db.models.legosets_prices_orm import LegosetsPricesOrm


if __name__ == '__main__':
    Base.metadata.create_all(sync_engine)