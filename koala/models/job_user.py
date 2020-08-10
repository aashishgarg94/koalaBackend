from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from ..constants import BOOKMARKED, REJECTED, SHORTLISTED
from ..core.mongo_model import OID, MongoModel


class UserJobsRelationModel(MongoModel):
    job_id: OID = Field()
    applied_on: Optional[datetime]


class JobApplicantsRelationModel(MongoModel):
    user_id: OID = Field()
    full_name: str
    preferred_city: Optional[str] = None
    preferred_area: Optional[str] = None
    mobile_number: int
    match_score: int = 0
    applied_on: Optional[datetime]
    applicant_status: Optional[str] = None
    status_change_date: Optional[datetime]


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


class JobApplicantsOutModel(JobApplicantsRelationModel):
    id: OID = Field()


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


class BaseApplicantApplied(MongoModel):
    total_applicants: Optional[int] = 0
    applicants_with_documents: Optional[int] = 0
    applicants: Optional[List[JobApplicantsRelationModel]] = []


class AllowedActionModel(str, Enum):
    bookmark = BOOKMARKED
    shortlist = SHORTLISTED
    reject = REJECTED


class JobApplicantAction(BaseModel):
    job_id: str
    applicant_id: str


class JobApplicantInAction(JobApplicantAction):
    applicant_status: str
    status_change_date: Optional[datetime]


class JobApplicantActionOutModel(MongoModel):
    id: OID = Field()
    updated_status: str
    updated_date: datetime
