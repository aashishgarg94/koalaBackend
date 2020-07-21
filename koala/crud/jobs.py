from datetime import datetime
from typing import List, Optional

from koala.db.mongodb import db
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from ..config.collections import DB_NAME, JOBS
from ..core.utils import get_seq_next_value
from ..models.jobs import JobInModel, JobOutModel


class JobsCollection:
    jobs_collection = AsyncIOMotorClient

    def __init__(self):
        self.jobs_collection = db.client[DB_NAME][JOBS]

    async def job_create(self, job_info: JobInModel) -> Optional[JobOutModel]:
        try:
            job_info.created_on = datetime.now()
            job_info_json = job_info.dict()
            job_info_json["_id"] = await get_seq_next_value(JOBS)
            result = await self.jobs_collection.insert_one(job_info_json)
            return result if result else False
        except Exception as e:
            raise e

    async def get_count(self) -> int:
        try:
            return await self.jobs_collection.count_documents({"is_deleted": False})
        except Exception as e:
            raise e

    async def get_all(self, skip: int, limit: int) -> List[JobOutModel]:
        try:
            jobs = []
            jobs_cursor = (
                self.jobs_collection.find({"is_deleted": False}).skip(skip).limit(limit)
            )
            for document in await jobs_cursor.to_list(length=limit):
                jobs.append(JobOutModel(**document, id=document.get("_id")))
            return jobs
        except Exception as e:
            raise e

    async def get_by_id(self, job_id) -> Optional[JobOutModel]:
        try:
            job = await self.jobs_collection.find_one({"_id": job_id})
            return JobOutModel(**job, id=job.get("_id")) if job else None
        except Exception as e:
            raise e

    async def find_and_update(
        self, job_id: int, job_changes: JobInModel
    ) -> Optional[JobOutModel]:
        find = {"_id": job_id}
        try:
            job_changes.is_updated = True
            job_changes.updated_on = datetime.now()
            job_changes_json = job_changes.dict(
                exclude_unset=True, exclude_defaults=True
            )

            result = await self.jobs_collection.find_one_and_update(
                find, {"$set": job_changes_json}, return_document=ReturnDocument.AFTER,
            )
            return JobOutModel(**result, id=result.get("_id")) if result else None
        except Exception as e:
            raise e

    async def delete_by_id(self, job_id: int) -> Optional[JobOutModel]:
        try:
            result = await self.jobs_collection.find_one_and_update(
                {"_id": job_id},
                {"$set": {"is_deleted": True, "deleted_on": datetime.now()}},
                return_document=ReturnDocument.AFTER,
            )
            return JobOutModel(**result, id=result.get("_id")) if result else False
        except Exception as e:
            raise e
