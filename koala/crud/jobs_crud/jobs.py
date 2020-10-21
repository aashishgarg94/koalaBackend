import logging
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from koala.config.collections import JOBS
from koala.models.jobs_models.jobs import (
    JobInModel,
    JobListOutModel,
    JobOutModel,
    SavedByObjectId,
)
from koala.models.jobs_models.master import BaseIsCreated

from .company import CompanyCollection
from .mongo_base import MongoBase


class JobCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(JOBS)

    async def create(self, job_detail: JobInModel) -> Optional[JobOutModel]:
        try:
            job_detail.created_on = datetime.now()
            result = await self.collection.insert_one(
                job_detail.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )
            data = BaseIsCreated(id=result, is_created=True) if result else None
            logging.info(f"Job created fetched successfully")

            # Updating company details
            company_details = job_detail.job_info.company_details
            company_collection = CompanyCollection()
            update_company = await company_collection.find_one_and_modify(
                company_details=company_details
            )
            if update_company.is_updated is not True:
                logging.info(
                    f"Not able to update company details while creating the job"
                )
            return data
        except Exception as e:
            logging.error(f"Error: Job creation {e}")
            raise e

    async def get_count(self) -> int:
        try:
            filter_condition = {"is_deleted": False}
            count = await self.collection.count(filter_condition)
            return count if count else 0
        except Exception as e:
            logging.error(f"Error: Job count {e}")
            raise e

    async def get_all_with_full_details(
        self, skip: int, limit: int
    ) -> Optional[List[JobOutModel]]:
        try:
            filter_condition = {"is_deleted": False}
            data = await self.collection.find(
                finder=filter_condition,
                skip=skip,
                limit=limit,
                return_doc_id=True,
                extended_class_model=JobOutModel,
            )
            return data if data else None
        except Exception as e:
            logging.error(f"Error: Get all {e}")
            raise e

    async def get_all(self, skip: int, limit: int) -> Optional[List[JobListOutModel]]:
        try:
            filter_condition = {"is_deleted": False}
            data = await self.collection.find(
                finder=filter_condition,
                skip=skip,
                limit=limit,
                return_doc_id=True,
                extended_class_model=JobListOutModel,
            )
            return data if data else []
        except Exception as e:
            logging.error(f"Error: Get all {e}")
            raise e

    async def get_by_id(self, job_id: str) -> Optional[JobOutModel]:
        try:
            finder = {"_id": ObjectId(job_id)}
            job = await self.collection.find_one(
                finder=finder, return_doc_id=True, extended_class_model=JobOutModel
            )
            return job if job else None
        except Exception as e:
            logging.error(f"Error: Get by id {e}")
            raise e

    async def find_one_and_modify(
        self, job_id: str, job_changes: JobInModel
    ) -> Optional[JobOutModel]:
        finder = {"_id": ObjectId(job_id)}
        try:
            job_changes.is_updated = True
            job_changes.updated_on = datetime.now()
            job_changes_json = job_changes.dict(
                exclude_unset=True, exclude_defaults=True
            )
            updater = {"$set": job_changes_json}

            updated_job = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=JobOutModel,
                return_updated_document=True,
            )
            return updated_job if updated_job else None
        except Exception as e:
            logging.error(f"Error: Find one and modify {e}")
            raise e

    async def job_close_by_id(self, job_id: str) -> Optional[JobOutModel]:
        try:
            finder = {"_id": ObjectId(job_id)}
            updater = {"$set": {"is_closed": True, "closed_on": datetime.now()}}
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=JobOutModel,
                return_updated_document=True,
            )
            return result if result else None
        except Exception as e:
            logging.error(f"Error: Closed by id {e}")
            raise e

    async def delete_by_id(self, job_id: str) -> Optional[JobOutModel]:
        try:
            finder = {"_id": ObjectId(job_id)}
            updater = {"$set": {"is_deleted": True, "deleted_on": datetime.now()}}
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_doc_id=True,
                extended_class_model=JobOutModel,
                return_updated_document=True,
            )
            return result if result else None
        except Exception as e:
            logging.error(f"Error: Delete by id {e}")
            raise e

    async def save_job_by_id(self, job_id: str, user_id: str) -> Optional[JobOutModel]:
        try:
            finder = {"_id": ObjectId(job_id)}
            updater = {
                "$push": {
                    "saved_by": {
                        "$each": [SavedByObjectId(user_id=ObjectId(user_id)).dict()],
                    }
                }
            }
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_updated_document=True,
                return_doc_id=True,
                extended_class_model=JobOutModel,
            )
            return result if result else None
        except Exception as e:
            logging.error(f"Error: Delete by id {e}")
            raise e
