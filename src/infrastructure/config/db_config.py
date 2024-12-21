from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os
from pathlib import Path

from infrastructure.config.logs_config import error_logger, system_logger


def find_src_folder(start_path: Path) -> Path:
    """Рекурсивно ищет директорию 'src' начиная с указанного пути и поднимаясь вверх."""
    current_path = start_path.resolve()
    while current_path != current_path.parent:  # Пока не достигнем корня файловой системы
        src_path = current_path / "src"
        if src_path.is_dir():  # Проверяем, существует ли папка src
            return src_path
        current_path = current_path.parent
    raise FileNotFoundError("Папка 'src' не найдена в иерархии директорий.")

def get_env_path():
    env_path = ".env"
    try:
        # Найти папку src и путь к .env
        src_folder = find_src_folder(Path(__file__).parent)
        env_path = src_folder / ".env"
    except Exception as e:
        system_logger.error(f"env_path: {env_path}")
        error_logger.error(f"env_path: {env_path}")

    return env_path

class DBSettings(BaseSettings):
    # model_config = SettingsConfigDict(env_file="../.env", extra="ignore")
    # model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    # current_path = os.getcwd()
    # print(f"Текущая рабочая директория: {current_path}")


    model_config = SettingsConfigDict(
        env_file=get_env_path(),
        extra="ignore")

    MODE: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"



db_settings = DBSettings()

