from typing import Optional, Type

from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import UUID4

from ..db.mongodb import db
from ..models.user import UD


class MongoDBUserDatabase:
    collection: AsyncIOMotorCollection

    def __init__(self, user_db_model: Type[UD]):
        self.user_db_model = user_db_model
        self.collection = db.client["koala-backend"]["test-users"]

    async def get(self, id: UUID4) -> Optional[UD]:
        user = await self.collection.find_one({"id": id})
        return self.user_db_model(**user) if user else None

    async def get_by_email(self, email: str) -> Optional[UD]:
        user = await self.collection.find_one({"email": email})
        return self.user_db_model(**user) if user else None

    async def create(self, user: UD) -> UD:
        await self.collection.insert_one(user.dict())
        return user

    async def update(self, user: UD) -> UD:
        await self.collection.replace_one({"id": user.id}, user.dict())
        return user

    async def delete(self, user: UD) -> None:
        await self.collection.delete_one({"id": user.id})
