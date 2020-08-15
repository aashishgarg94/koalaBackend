from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import EmailStr

from koala.config.collections import COMPANIES
from koala.crud.mongo_base import MongoBase
from koala.models.jobs import CompanyOutModel, CompanyInModel
from koala.models.master import BaseIsCreated, BaseNotFound


class CompanyCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(COMPANIES)

    async def find_by_object_id(self, user_id: ObjectId) -> any:
        try:
            return await self.collection.find_one(
                {"_id": user_id}, return_doc_id=True, extended_class_model=CompanyOutModel,
            )
        except Exception as e:
            raise e

    async def find_by_email(self, email: EmailStr) -> Optional[CompanyOutModel]:
        try:
            result = await self.collection.find_one(
                {"contact_email": email}, return_doc_id=True, extended_class_model=CompanyOutModel,
            )
            return result if result else BaseNotFound()
        except Exception as e:
            raise e

    async def create_user(self, user: CompanyInModel) -> BaseIsCreated:
        try:
            user.created_on = datetime.now()
            result = await self.collection.insert_one(
                user.dict(), return_doc_id=True, extended_class_model=BaseIsCreated
            )
            return BaseIsCreated(id=result, is_created=True) if result else None
        except Exception as e:
            raise e
