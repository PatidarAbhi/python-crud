from pydantic_settings import BaseSettings
from loguru import logger


class Settings(BaseSettings):
    ENV: str
    DATABASE_URL: str

    class Config:
        env_file = ".env.local"


settings = Settings()

logger.info(f"Active profile : {settings.ENV}")
