from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os


class DBSettings(BaseSettings):
    # model_config = SettingsConfigDict(env_file="../.env", extra="ignore")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

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

