from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..core.mongo_model import OID, MongoModel


class UserJobsRelationModel(MongoModel):
    job_id: OID = Field()
    applied_on: Optional[datetime]


class JobApplicantsRelationModel(MongoModel):
    user_id: OID = Field()
    applied_on: Optional[datetime]


class BaseIsApplied(MongoModel):
    job_id: OID = Field()
    is_applied: bool = False


class UserJobsModel(UserJobsRelationModel):
    user_id: OID = Field()


class UserJobsOutModel(UserJobsRelationModel):
    id: OID = Field()


class UserJobsOutWithPagination(MongoModel):
    total_jobs: int
    current_page: int
    jobs: List[UserJobsRelationModel]


class JobApplicantsModel(JobApplicantsRelationModel):
    job_id: OID = Field()


class BaseJobApplicant(BaseModel):
    job_id: str
    page_no: int


class JobApplicantOutWithPagination(MongoModel):
    total_applicants: int
    current_page: int
    applicants: List[JobApplicantsRelationModel]


class BaseJobCount(BaseModel):
    total_jobs: int


class BaseApplicantCount(BaseModel):
    total_applicants: int
