import logging
from datetime import datetime
from typing import List

from bson import ObjectId

from ..config.collections import JOB_APPLICANTS, JOBS, USER_JOBS, USERS
from ..constants import EMBEDDED_COLLECTION_LIMIT
from ..models.job_user import (
    BaseIsApplied,
    JobApplicantsModel,
    UserJobsModel,
    UserJobsRelationModel,
)
from ..models.jobs import JobApplicantsRelationModel, JobOutModel
from ..models.master import BaseIsCreated, BaseIsUpdated
from ..models.user import UserInModel, UserModel, UserOutModel
from .mongo_base import MongoBase
from .user import MongoDBUserDatabase


class JobUser:
    def __init__(self):
        self.collection = MongoBase()
        self.user_collection = MongoDBUserDatabase(UserInModel)

    async def find_user_and_get_job_count(self, user_id: ObjectId):
        try:
            self.collection(USERS)
            aggregate_condition = [
                {
                    "$project": {
                        "email": 1,
                        "job": {
                            "$cond": {
                                "if": {"$isArray": "$job"},
                                "then": {"$size": "$job"},
                                "else": "NA",
                            }
                        },
                    }
                }
            ]
            result = await self.collection.aggregate(aggregate_condition)
            logging.info(result)
        except Exception as e:
            raise e

    async def update_job_with_user(
        self, job_id: ObjectId, user_id: ObjectId
    ) -> BaseIsUpdated:
        try:
            self.collection(JOBS)
            finder = {"_id": job_id}
            updater = {
                "$push": {
                    "user_applied": {
                        "$each": [
                            JobApplicantsRelationModel(
                                user_id=user_id, applied_on=datetime.now()
                            ).dict()
                        ],
                        "$sort": {"applied_on": -1},
                        "$slice": EMBEDDED_COLLECTION_LIMIT,
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
            logging.info(f"Job apply SUCCESS: While updating job with user")
            return BaseIsUpdated(id=result.id, is_updated=True) if result else None
        except Exception as e:
            logging.error(f"Job apply ERROR: While updating job with user")
            raise e

    async def update_user_with_job(
        self, user_id: ObjectId, job_id: ObjectId
    ) -> BaseIsUpdated:
        try:
            self.collection(USERS)
            finder = {"_id": user_id}
            updater = {
                "$push": {
                    "job_applied": {
                        "$each": [
                            UserJobsRelationModel(
                                job_id=job_id, applied_on=datetime.now()
                            ).dict()
                        ],
                        "$sort": {"applied_on": -1},
                        "$slice": EMBEDDED_COLLECTION_LIMIT,
                    }
                }
            }
            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_updated_document=True,
                return_doc_id=True,
                extended_class_model=UserOutModel,
            )
            logging.info(f"Job apply SUCCESS: While updating user with job")
            return BaseIsUpdated(id=result.id, is_updated=True) if result else None
        except Exception as e:
            logging.error(f"Job apply ERROR: While updating user with job")
            raise e

    async def update_user_jobs_with_jobs(
        self, user_id: ObjectId, job_id: ObjectId
    ) -> BaseIsCreated:
        try:
            self.collection(USER_JOBS)

            document = UserJobsModel(
                user_id=user_id, job_id=job_id, applied_on=datetime.now()
            )
            result = await self.collection.insert_one(
                document=document.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )
            return BaseIsCreated(id=result, is_created=True) if result else None
        except Exception as e:
            logging.error(f"Job apply ERROR: While inserting in user_jobs")
            raise e

    async def update_job_applicants_with_applicants(
        self, job_id: ObjectId, user_id: ObjectId
    ) -> BaseIsCreated:
        try:
            self.collection(JOB_APPLICANTS)

            document = JobApplicantsModel(
                job_id=job_id, user_id=user_id, applied_on=datetime.now()
            )
            result = await self.collection.insert_one(
                document=document.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )
            return BaseIsCreated(id=result, is_created=True) if result else None
        except Exception as e:
            logging.error(f"Job apply ERROR: While inserting in user_jobs")
            raise e

    async def apply_job(self, job_id: str, current_user: UserModel) -> BaseIsApplied:
        try:
            user_id = ObjectId(current_user.id)
            job_id = ObjectId(job_id)

            # Handle main collection update
            job_update = await self.update_job_with_user(job_id=job_id, user_id=user_id)
            user_update = await self.update_user_with_job(
                user_id=user_id, job_id=job_id
            )

            # Handle subset collection update
            # TODO: Procedure can be written to sync collection and subset update later
            #  for in case of any failure
            user_jobs_update = await self.update_user_jobs_with_jobs(
                user_id=user_id, job_id=job_id
            )
            job_applicants_update = await self.update_job_applicants_with_applicants(
                job_id=job_id, user_id=user_id
            )
            logging.info(user_jobs_update)
            logging.info(job_applicants_update)

            if (
                job_update
                and user_update
                and user_jobs_update
                and job_applicants_update
            ):
                logging.info(f"Job apply SUCCESS: While processing job apply")
                return BaseIsApplied(job_id=job_id, user_id=user_id, is_applied=True)
        except Exception as e:
            logging.error(f"Job apply ERROR: While processing job apply")
            raise e

    async def get_user_jobs_count(self, current_user: UserModel) -> int:
        try:
            self.collection(USER_JOBS)

            filter_condition = {"user_id": ObjectId(current_user.id)}
            return await self.collection.count(filter_condition=filter_condition)
        except Exception as e:
            logging.error(f"Error: while getting user jobs count {e}")
            raise e

    async def user_get_all_jobs(
        self, skip: int, limit: int, current_user: UserModel
    ) -> List[UserJobsRelationModel]:
        try:
            self.collection(USER_JOBS)

            filter_condition = {"user_id": ObjectId(current_user.id)}
            data = await self.collection.find(
                finder=filter_condition,
                skip=skip,
                limit=limit,
                return_doc_id=True,
                extended_class_model=UserJobsRelationModel,
            )
            return data if data else []
        except Exception as e:
            logging.error(f"Error: while getting all jobs {e}")
            raise e

    async def get_job_applicants_count(self, job_id: str) -> int:
        try:
            self.collection(JOB_APPLICANTS)

            filter_condition = {"job_id": ObjectId(job_id)}
            return await self.collection.count(filter_condition=filter_condition)
        except Exception as e:
            logging.error(f"Error: while getting job applicant count {e}")
            raise e

    async def job_get_recent_applicants(
        self, job_id: str
    ) -> List[JobApplicantsRelationModel]:
        try:
            self.collection(JOBS)

            filter_condition = {"_id": ObjectId(job_id)}
            data = await self.collection.find(
                finder=filter_condition,
                return_doc_id=True,
                extended_class_model=JobOutModel,
            )
            return data[0].user_applied if data else []
        except Exception as e:
            logging.error(f"Error: while getting recent applicants {e}")
            raise e

    async def job_get_all_applicants(
        self, skip: int, limit: int, job_id: str
    ) -> List[JobApplicantsRelationModel]:
        try:
            self.collection(JOB_APPLICANTS)

            filter_condition = {"job_id": ObjectId(job_id)}
            data = await self.collection.find(
                finder=filter_condition,
                skip=skip,
                limit=limit,
                return_doc_id=True,
                extended_class_model=JobApplicantsRelationModel,
            )
            return data if data else []
        except Exception as e:
            logging.error(f"Error: while getting all applicants {e}")
            raise e
