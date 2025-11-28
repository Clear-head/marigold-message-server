from typing import Dict, Any
from abc import ABC, abstractmethod
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection


class BaseRepository(ABC):

    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        self.db = db
        self.collection: AsyncIOMotorCollection = db[collection_name]

    @abstractmethod
    def _to_document(self, entity) -> Dict[str, Any]:
        pass

    @abstractmethod
    def _to_entity(self, document: Dict[str, Any]):
        pass

    @abstractmethod
    def _get_entity_id(self, entity) -> Any:
        pass

    async def save(self, entity) -> None:
        document = self._to_document(entity)
        await self.collection.insert_one(document)

    async def update(self, entity) -> None:
        document = self._to_document(entity)
        entity_id = self._get_entity_id(entity)
        await self.collection.replace_one({"_id": entity_id}, document)
