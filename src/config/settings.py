from pathlib import Path

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: Optional[str] = None
    MONGODB_DB_NAME: Optional[str] = None

    # Redis
    REDIS_URL: Optional[str] = None
    REDIS_PASSWORD: Optional[str] = None
    REDIS_MAX_CONNECTIONS: int = None
    # Kafka 설정
    KAFKA_BOOTSTRAP_SERVERS: Optional[str] = None
    KAFKA_TOPIC_CHAT: str = None
    KAFKA_CONSUMER_GROUP: str = None

    # JWT 설정
    JWT_SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = None
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = None
    JWT_REFRESH_TOKEN_EXPIRE_HOURS: int = None

    # 앱 설정
    APP_ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = f"{Path(__file__).resolve().parent.parent}.env"
        case_sensitive = True