from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from src.config.settings import Settings


class MongoDBConnection:
    _client: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect(cls) -> None:
        settings = Settings()
        if cls._client is None:
            cls._client = AsyncIOMotorClient(settings.MONGODB_URL)
            cls._db = cls._client[settings.MONGODB_DB_NAME]

    @classmethod
    async def disconnect(cls) -> None:
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._db = None

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        if cls._db is None:
            raise Exception("MongoDB가 연결되지 않았습니다. connect()를 먼저 호출하세요.")
        return cls._db

    @classmethod
    def get_collection(cls, collection_name: str):
        db = cls.get_database()
        return db[collection_name]


async def get_db() -> AsyncIOMotorDatabase:
    return MongoDBConnection.get_database()