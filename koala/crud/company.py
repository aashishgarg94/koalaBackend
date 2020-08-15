import logging
from datetime import datetime
from typing import Optional

from bson import ObjectId
from koala.config.collections import COMPANIES
from koala.crud.mongo_base import MongoBase
from koala.models.jobs import CompanyInModel, CompanyInPasswordModel, CompanyOutModel
from koala.models.master import BaseIsCreated, BaseIsUpdated, BaseNotFound
from pydantic import EmailStr


class CompanyCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(COMPANIES)

    async def find_by_object_id(self, user_id: ObjectId) -> any:
        try:
            return await self.collection.find_one(
                {"_id": user_id},
                return_doc_id=True,
                extended_class_model=CompanyOutModel,
            )
        except Exception as e:
            raise e

    async def find_by_email(self, email: EmailStr) -> Optional[CompanyOutModel]:
        try:
            result = await self.collection.find_one(
                {"contact_email": email},
                return_doc_id=True,
                extended_class_model=CompanyOutModel,
            )
            return result if result else BaseNotFound()
        except Exception as e:
            raise e

    async def create_user(self, user: CompanyInPasswordModel) -> BaseIsCreated:
        try:
            user.created_on = datetime.now()
            result = await self.collection.insert_one(
                user.dict(), return_doc_id=True, extended_class_model=BaseIsCreated
            )
            return BaseIsCreated(id=result, is_created=True) if result else None
        except Exception as e:
            raise e

    async def find_one_and_modify(
        self, company_details: CompanyOutModel
    ) -> Optional[BaseIsUpdated]:
        try:
            logging.info(company_details)
            logging.info(company_details.id)
            company_dict = CompanyInModel(**company_details.dict())
            finder = {"_id": ObjectId(company_details.id)}
            company_dict.is_updated = True
            company_dict.updated_on = datetime.now()
            job_changes_json = company_dict.dict(
                exclude_unset=True, exclude_defaults=True
            )
            updater = {"$set": job_changes_json}
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=CompanyOutModel,
                insert_if_not_found=True,
                return_updated_document=True,
            )
            logging.info(f"Job delete by id successfully")
            return BaseIsUpdated(id=result.id, is_updated=True) if result else None
        except Exception as e:
            logging.error(f"Error: Delete by id {e}")
            raise e
