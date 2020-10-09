import logging
from datetime import datetime
from typing import List

from bson import ObjectId
from koala.config.collections import JOB_APPLICANTS, JOBS, USER_JOBS, USERS
from koala.constants import (
    ALL,
    ALL_JOBS,
    APPLIED_JOBS,
    BOOKMARKED,
    EMBEDDED_COLLECTION_LIMIT,
    FILTERED_JOBS,
    FRESHERS_JOBS,
    REJECTED,
    SAVED_JOBS,
    SHORTLISTED,
)
from koala.models.jobs_models.job_user import (
    BaseIsApplied,
    JobApplicantInAction,
    JobApplicantsModel,
    JobApplicantsOutModel,
    JobApplicantsRelationModel,
    UserJobsModel,
    UserJobsRelationModel,
)
from koala.models.jobs_models.jobs import JobOutModel
from koala.models.jobs_models.master import BaseIsCreated, BaseIsUpdated
from koala.models.jobs_models.user import UserInModel, UserModel, UserOutModel

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
        self, job_id: ObjectId, current_user: UserModel
    ) -> BaseIsUpdated:
        try:
            self.collection(JOBS)
            finder = {"_id": job_id}
            updater = {
                "$inc": {"applicants_details.total_applicants": 1},
                "$push": {
                    "applicants_details.applicants": {
                        "$each": [
                            JobApplicantsRelationModel(
                                user_id=ObjectId(current_user.id),
                                full_name=f"{current_user.full_name.first_name} {current_user.full_name.middle_name} {current_user.full_name.last_name}",
                                preferred_city=current_user.bio.preferred_city
                                if current_user.bio
                                else None,
                                preferred_area=current_user.bio.preferred_area
                                if current_user.bio
                                else None,
                                mobile_number=current_user.mobile_number,
                                match_score=77,
                                applied_on=datetime.now(),
                            ).dict()
                        ],
                        "$sort": {"applied_on": -1},
                        "$slice": EMBEDDED_COLLECTION_LIMIT,
                    }
                },
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
        self, job_id: ObjectId, current_user: UserModel
    ) -> BaseIsCreated:
        try:
            self.collection(JOB_APPLICANTS)

            document = JobApplicantsModel(
                job_id=job_id,
                user_id=ObjectId(current_user.id),
                full_name=f"{current_user.full_name.first_name} {current_user.full_name.middle_name} {current_user.full_name.last_name}",
                preferred_city=current_user.bio.preferred_city
                if current_user.bio
                else None,
                preferred_area=current_user.bio.preferred_area
                if current_user.bio
                else None,
                mobile_number=current_user.mobile_number,
                match_score=77,
                applied_on=datetime.now(),
            )
            result = await self.collection.insert_one(
                document=document.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )
            return BaseIsCreated(id=result, is_created=True) if result else None
        except Exception as e:
            logging.error(
                f"Job apply ERROR: While inserting in job_applicants with applicants"
            )
            raise e

    async def apply_job(self, job_id: str, current_user: UserModel) -> BaseIsApplied:
        try:
            user_id = ObjectId(current_user.id)
            job_id = ObjectId(job_id)

            # Handle main collection update
            job_update = await self.update_job_with_user(
                job_id=job_id, current_user=current_user
            )
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
                job_id=job_id, current_user=current_user
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

    async def job_get_recent_applicants(self, job_id: str) -> any:
        try:
            self.collection(JOBS)

            filter_condition = {"_id": ObjectId(job_id)}
            data = await self.collection.find(
                finder=filter_condition,
                return_doc_id=True,
                extended_class_model=JobOutModel,
            )

            total_jobs = 0
            applicants = {ALL: [], BOOKMARKED: [], SHORTLISTED: [], REJECTED: []}

            for job_data in data:
                if len(job_data.applicants_details.applicants) > 0:
                    total_jobs = job_data.applicants_details.total_applicants
                    for job_applicants in job_data.applicants_details.applicants:
                        # Add to all
                        applicants.get(ALL).append(job_applicants)

                        # Add to bookmarked
                        if job_applicants.applicant_status == BOOKMARKED:
                            applicants.get(BOOKMARKED).append(job_applicants)

                        # Add to shortlisted
                        if job_applicants.applicant_status == SHORTLISTED:
                            applicants.get(SHORTLISTED).append(job_applicants)

                        # Add to rejected
                        if job_applicants.applicant_status == REJECTED:
                            applicants.get(REJECTED).append(job_applicants)

            return {"total_jobs": total_jobs, "applicants": applicants}
        except Exception as e:
            logging.error(f"Error: while getting recent applicants {e}")
            raise e

    # List[JobApplicantsRelationModel]
    async def job_get_all_applicants(self, skip: int, limit: int, job_id: str) -> any:
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

            applicants = {ALL: [], BOOKMARKED: [], SHORTLISTED: [], REJECTED: []}

            if len(data) > 0:
                for job_data in data:
                    # Add to all
                    applicants.get(ALL).append(job_data)

                    # Add to bookmarked
                    if job_data.applicant_status == BOOKMARKED:
                        applicants.get(BOOKMARKED).append(job_data)

                    # Add to shortlisted
                    if job_data.applicant_status == SHORTLISTED:
                        applicants.get(SHORTLISTED).append(job_data)

                    # Add to rejected
                    if job_data.applicant_status == REJECTED:
                        applicants.get(REJECTED).append(job_data)

            return {"total_jobs": len(applicants.get(ALL)), "applicants": applicants}

            # return data if data else []
        except Exception as e:
            logging.error(f"Error: while getting all applicants {e}")
            raise e

    async def apply_action_on_job(self, job_user_map: JobApplicantInAction) -> bool:
        try:
            self.collection(JOBS)

            finder = {"_id": ObjectId(job_user_map.job_id)}
            updater = {
                "$set": {
                    "applicants_details.applicants.$[elem].applicant_status": job_user_map.applicant_status,
                    "applicants_details.applicants.$[elem].status_change_date": datetime.now(),
                }
            }
            array_filter = [{"elem.user_id": ObjectId(job_user_map.applicant_id)}]

            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                array_filters=array_filter,
                return_updated_document=True,
                return_doc_id=True,
                extended_class_model=JobOutModel,
            )
            return True if result else False
        except Exception as e:
            logging.error(f"Error: while updating job status {e}")
            raise e

    async def apply_action_on_job_applicants(
        self, job_user_map: JobApplicantInAction
    ) -> bool:
        try:
            self.collection(JOB_APPLICANTS)

            finder = {"job_id": ObjectId(job_user_map.job_id)}
            updater = {
                "$set": {
                    "applicant_status": job_user_map.applicant_status,
                    "status_change_date": datetime.now(),
                }
            }

            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_updated_document=True,
                return_doc_id=True,
                extended_class_model=JobApplicantsOutModel,
            )
            # return BaseIsUpdated(id=result.id, is_updated=True) if result else None
            return True if result else False

        except Exception as e:
            logging.error(f"Error: while updating job status {e}")
            raise e

    async def apply_job_action(
        self, job_user_map: JobApplicantInAction
    ) -> BaseIsUpdated:
        try:
            on_job_collection_result = await self.apply_action_on_job(
                job_user_map=job_user_map
            )
            on_job_applicants_collection_result = await self.apply_action_on_job_applicants(
                job_user_map=job_user_map
            )
            logging.info(on_job_collection_result)
            logging.info(on_job_applicants_collection_result)
            return (
                BaseIsUpdated(id=job_user_map.job_id, is_updated=True)
                if on_job_collection_result and on_job_applicants_collection_result
                else None
            )
        except Exception as e:
            logging.error(f"Error while applying job action. ERROR: {e}")
            raise e

    async def get_user_action_jobs(self, user_id: str) -> any:
        try:
            self.collection(JOBS)
            filter_condition = {
                "$or": [
                    {"saved_by": {"$elemMatch": {"user_id": ObjectId(user_id)}}},
                    {
                        "applicants_details.applicants": {
                            "$elemMatch": {"user_id": ObjectId(user_id)}
                        }
                    },
                ]
            }
            jobs_data = await self.collection.find(
                finder=filter_condition,
                return_doc_id=True,
                extended_class_model=JobOutModel,
            )
            action_jobs = {APPLIED_JOBS: [], SAVED_JOBS: []}
            if len(jobs_data) > 0:
                for jobs in jobs_data:
                    for job in jobs.applicants_details.applicants:
                        if user_id == job.user_id:
                            action_jobs.get(APPLIED_JOBS).append(jobs)
                    for job in jobs.saved_by:
                        if user_id == job.user_id:
                            action_jobs.get(SAVED_JOBS).append(jobs)
                return action_jobs

            return action_jobs
        except Exception as e:
            logging.error(f"Error while applying job action. ERROR: {e}")
            raise e

    async def get_all_matched_jobs(self) -> any:
        try:
            self.collection(JOBS)
            filter_condition = {}
            jobs_data = await self.collection.find(
                finder=filter_condition,
                return_doc_id=True,
                extended_class_model=JobOutModel,
            )
            all_matched_jobs = {ALL_JOBS: [], FRESHERS_JOBS: []}
            if len(jobs_data) > 0:
                for jobs in jobs_data:
                    all_matched_jobs.get(ALL_JOBS).append(jobs)
                return all_matched_jobs

            return all_matched_jobs
        except Exception as e:
            logging.error(f"Error while applying job action. ERROR: {e}")
            raise e

    async def get_all_freshers_jobs(self) -> any:
        try:
            self.collection(JOBS)
            filter_condition = {"experience.start_range": 0, "experience.end_range": 0}
            jobs_data = await self.collection.find(
                finder=filter_condition,
                return_doc_id=True,
                extended_class_model=JobOutModel,
            )
            freshers_jobs = {FRESHERS_JOBS: []}
            if len(jobs_data) > 0:
                for jobs in jobs_data:
                    freshers_jobs.get(FRESHERS_JOBS).append(jobs)
                return freshers_jobs

            return freshers_jobs
        except Exception as e:
            logging.error(f"Error while applying job action. ERROR: {e}")
            raise e

    async def get_all_jobs_by_filter(
        self,
        city: str,
        job_type: str,
        salary_start_range: int,
        salary_end_range: int,
        area: str,
        title: str,
        company_name: str,
    ) -> any:
        try:
            self.collection(JOBS)
            if title is not None or company_name is not None:
                filter_condition = {
                    "$or": [
                        {"title": title},
                        {"job_info.company_details.company_name": company_name},
                    ]
                }
            else:
                filter_condition = {
                    "$and": [
                        {"city": city},
                        {"job_info.job_types": {"$elemMatch": {"name": job_type}}},
                        {
                            "experience.start_range": salary_start_range,
                            "experience.end_range": salary_end_range,
                        },
                        {"area": area},
                    ]
                }
            jobs_data = await self.collection.find(
                finder=filter_condition,
                return_doc_id=True,
                extended_class_model=JobOutModel,
            )
            filtered_jobs = {FILTERED_JOBS: []}
            if len(jobs_data) > 0:
                for jobs in jobs_data:
                    filtered_jobs.get(FILTERED_JOBS).append(jobs)
                return filtered_jobs

            return filtered_jobs
        except Exception as e:
            logging.error(f"Error while applying job action. ERROR: {e}")
            raise e
