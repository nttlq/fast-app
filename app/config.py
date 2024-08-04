from functools import lru_cache
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Literal["DEV", "TEST", "PROD"] = "DEV"

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class GlobalConfig(BaseConfig):
    # DATABASE_URL: Optional[str] = None
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_FORCE_ROLL_BACK: bool = False
    LOGTAIL_API_KEY: Optional[str] = None

    @property
    def DATABASE_URL(self): ...


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"  # noqa: E501


class TestConfig(GlobalConfig):
    # DATABASE_URL: str = "sqlite://test.db"
    DB_FORCE_ROLL_BACK: bool = True

    model_config = SettingsConfigDict(env_prefix="TEST_")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"  # noqa: E501


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"  # noqa: E501


@lru_cache()
def get_config(env_state: str):
    configs = {"DEV": DevConfig, "PROD": ProdConfig, "TEST": TestConfig}
    return configs[env_state]()


config: DevConfig | TestConfig | ProdConfig = get_config(BaseConfig().ENV_STATE)
