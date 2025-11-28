from pathlib import Path

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    MONGODB_URL: Optional[str]
    MONGODB_DB_NAME: Optional[str]

    APP_ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = f"{Path(__file__).resolve().parent.parent}.env"
        case_sensitive = True