import logging
from datetime import datetime

from koala.config.collections import WEBSITE_APPLICANT, WEBSITE_PROVIDER
from koala.models.jobs_models.master import BaseIsCreated

from koala.crud.jobs_crud.mongo_base import MongoBase


class WebsiteCollections:
    def __init__(self):
        self.collection = MongoBase()

    async def insert_applicant(self, applicant_details: dict) -> any:
        try:
            self.collection(WEBSITE_APPLICANT)
            applicant_details["created_on"] = datetime.now()
            result = await self.collection.insert_one(
                applicant_details,
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )
            data = BaseIsCreated(id=result, is_created=True) if result else None
            return data
        except Exception as e:
            logging.error(f"Error: Applicant record creation {e}")
            raise e

    async def insert_provider(self, applicant_details: dict) -> any:
        try:
            self.collection(WEBSITE_PROVIDER)
            applicant_details["created_on"] = datetime.now()
            result = await self.collection.insert_one(
                applicant_details,
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )
            data = BaseIsCreated(id=result, is_created=True) if result else None
            return data
        except Exception as e:
            logging.error(f"Error: Provider record creation {e}")
            raise e
