from datetime import datetime
from typing import Optional, Type

from bson import ObjectId
from fastapi import HTTPException
from pydantic import EmailStr

from ..config.collections import USERS
from ..models.master import BaseIsCreated, BaseIsDisabled
from ..models.user import (
    UD,
    BioUpdateInModel,
    BioUpdateOutModel,
    UserInModel,
    UserModel,
    UserOutModel,
    UserUpdateCls,
    UserUpdateOutModel,
)
from .mongo_base import MongoBase, return_id_transformation


class MongoDBUserDatabase:
    def __init__(self, user_db_model: Type[UD]):
        self.user_db_model = user_db_model
        self.collection = MongoBase()
        self.collection(USERS)

    async def find_by_object_id(self, user_id: ObjectId) -> Optional[UD]:
        try:
            return await self.collection.find_one(
                {"_id": user_id}, return_doc_id=True, extended_class_model=UserOutModel,
            )
        except Exception as e:
            raise e

    async def find_by_email(self, email: str) -> Optional[UD]:
        try:
            return await self.collection.find_one(
                {"email": email}, return_doc_id=True, extended_class_model=UserOutModel,
            )
        except Exception as e:
            raise e

    async def create_user(self, user: UserInModel) -> BaseIsCreated:
        try:
            user.created_on = datetime.now()
            result = await self.collection.insert_one(
                user.dict(), return_doc_id=True, extended_class_model=BaseIsCreated
            )
            return BaseIsCreated(id=result, is_created=True) if result else None
        except Exception as e:
            raise e

    async def find_and_modify(
        self, user_update: UserUpdateCls, current_user: UserModel
    ) -> UserUpdateOutModel:
        try:
            find = {"email": current_user.email}
            user_update.is_updated = True
            user_update.updated_on = datetime.now()
            user = await self.collection.find_one_and_modify(
                find,
                {"$set": user_update.dict(exclude_unset=True)},
                return_doc_id=True,
                extended_class_model=UserUpdateOutModel,
            )
            return user if user else None
        except Exception as e:
            raise e

    async def disable_one(self, user: UserUpdateCls) -> BaseIsDisabled:
        try:
            find = {"email": user.email}
            user.is_disabled = True
            user.disabled_on = datetime.now()
            result = await self.collection.find_one_and_modify(
                find,
                {"$set": user.dict(exclude_unset=True)},
                return_doc_id=True,
                extended_class_model=BaseIsDisabled,
            )
            data = result if result else None
            return data
        except Exception as e:
            raise e

    async def user_bio_update(
        self, bio_updates: BioUpdateInModel, current_user: UserModel
    ) -> BioUpdateOutModel:
        try:
            find = {"email": current_user.email}
            bio_updates.updated_on = datetime.now()
            result = await self.collection.find_one_and_modify(
                find, {"$set": {"bio": bio_updates.dict(exclude_unset=True)}},
            )

            custom_bio_dict = result.get("bio")
            custom_bio_dict["_id"] = result.get("_id")
            result_transformation = return_id_transformation(
                extended_class_model=BioUpdateOutModel, result=custom_bio_dict
            )

            return result_transformation if result else None
        except Exception as e:
            raise e

    async def user_bio_fetch(self, email: EmailStr) -> Optional[BioUpdateOutModel]:
        try:
            result = await self.collection.find_one({"email": email})

            if result.get("bio"):
                custom_bio_dict = result.get("bio")
                custom_bio_dict["_id"] = result.get("_id")
                result_transformation = return_id_transformation(
                    extended_class_model=BioUpdateOutModel, result=custom_bio_dict
                )
                return result_transformation

            raise HTTPException(status_code=200, detail="Bio not available")
        except Exception as e:
            raise e
