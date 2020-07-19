from fastapi.encoders import jsonable_encoder
from koala.db.mongodb import db
from motor.motor_asyncio import AsyncIOMotorClient

from ..models.jobs import BaseJobModelDB, JobCreatedOut
from ..core.utils import get_seq_next_value
from ..config.collections import JOBS, DB_NAME


class JobsCollection:
    jobs_collection = AsyncIOMotorClient

    def __init__(self):
        self.jobs_collection = db.client[DB_NAME][JOBS]

    async def job_create(self, job_info: BaseJobModelDB) -> bool:
        try:
            job_info_json = jsonable_encoder(job_info)
            job_info_json["_id"] = await get_seq_next_value(JOBS)
            job_obj = await self.jobs_collection.insert_one(
                job_info_json
            )
            return True if job_obj.inserted_id else False
        except Exception as e:
            raise e
