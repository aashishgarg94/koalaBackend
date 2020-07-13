from typing import Optional, Type

from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import UUID4, EmailStr
from pymongo import ReturnDocument

from ..config.collections import USERS
from ..db.mongodb import db
from ..models.user import UD, UserBioModal, UserUpdateCls


class MongoDBUserDatabase:
    collection: AsyncIOMotorCollection

    def __init__(self, user_db_model: Type[UD]):
        self.user_db_model = user_db_model
        self.collection = db.client["koala-backend"][USERS]

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

    async def find_and_modify(self, user_update: UserUpdateCls) -> any:
        find = {"username": user_update.username}
        update = user_update.dict(exclude_unset=True, exclude={"username"})
        user = await self.collection.find_one_and_update(
            find, {"$set": update}, return_document=ReturnDocument.AFTER
        )
        return self.user_db_model(**user) if user else None

    async def delete(self, email: EmailStr) -> None:
        user = await self.collection.find_one_and_update(
            {"email": email},
            {"$set": {"disabled": True}},
            return_document=ReturnDocument.AFTER,
        )
        return self.user_db_model(**user) if user else None

    async def user_bio_update(self, email: EmailStr, bio: UserBioModal) -> UserBioModal:
        user = await self.collection.find_one_and_update(
            {"email": email}, {"$set": {"bio": bio.dict()}}
        )
        return UserBioModal(**user["bio"]) if user else None

    async def user_bio_fetch(self, email: EmailStr) -> UserBioModal:
        user = await self.collection.find_one({"email": email})
        return UserBioModal(**user["bio"]) if user else None
