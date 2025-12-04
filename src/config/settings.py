from pathlib import Path

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: Optional[str]
    MONGODB_DB_NAME: Optional[str]

    # Redis
    REDIS_URL: Optional[str]
    REDIS_PASSWORD: Optional[str]
    REDIS_MAX_CONNECTIONS: int
    # Kafka 설정
    KAFKA_BOOTSTRAP_SERVERS: Optional[str]
    KAFKA_TOPIC_CHAT: str
    KAFKA_CONSUMER_GROUP: str

    # JWT 설정
    JWT_SECRET_KEY: Optional[str]
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int
    JWT_REFRESH_TOKEN_EXPIRE_HOURS: int

    # 앱 설정
    APP_ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = f"{Path(__file__).resolve().parent.parent}.env"
        case_sensitive = True