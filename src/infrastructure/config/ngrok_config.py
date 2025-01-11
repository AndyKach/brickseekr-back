import logging
import requests

import os

system_logger = logging.getLogger('system_logger')


async def config():
    system_logger.info("Start webhook configuration")

    system_logger.info("После установки webhook")
