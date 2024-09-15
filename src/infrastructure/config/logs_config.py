import logging
from dotenv import load_dotenv
import os
from functools import wraps

load_dotenv()
system_logger = logging.getLogger("system_logger")
error_logger = logging.getLogger("error_logger")
apscheduler_logger = logging.getLogger("apscheduler")


def config():
    """
    Функция первичной настройки логов

    :return: None
    """
    # Максимально подробный вывод логов
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')

    # Нормальный вывод логов
    formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s - %(message)s", datefmt="%d.%m-%H:%M"
    )

    system_handler = logging.FileHandler("logs/system_data.log")
    system_handler.setFormatter(formatter)

    error_handler = logging.FileHandler("logs/error_data.log")
    error_handler.setFormatter(formatter)

    if os.getenv("MODE") == "DEVELOPMENT":
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        system_logger.setLevel(logging.DEBUG)
        error_logger.setLevel(logging.DEBUG)

        system_logger.addHandler(console_handler)
        error_logger.addHandler(console_handler)
        apscheduler_logger.addHandler(console_handler)

    else:
        system_logger.setLevel(logging.INFO)
        error_logger.setLevel(logging.ERROR)

    system_logger.addHandler(system_handler)

    error_logger.addHandler(error_handler)

    apscheduler_logger.setLevel(logging.DEBUG)
    apscheduler_logger.addHandler(system_handler)


def log_decorator(func, log_level=logging.DEBUG):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        system_logger.log(level=log_level, msg=f"Called function: {func.__name__}. Args: {args}. Kwargs: {kwargs}")

        # Выполнение функции и получение результата
        result = await func(*args, **kwargs)

        # Запись результата выполнения функции
        # system_logger.log(level=log_level, msg=f"Result: {result}")

        return result

    return wrapper


def log_api_decorator(func, log_level=logging.INFO):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        system_logger.log(level=log_level, msg=f"API Called function: {func.__name__}")

        # Выполнение функции и получение результата
        result = await func(*args, **kwargs)

        # Запись результата выполнения функции
        system_logger.log(level=log_level, msg=f"Result: {result}")

        return result

    return wrapper

