from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from ..core.mongo_model import OID, MongoModel
from ..models.master import BaseKeyValueModel, BaseRangeModel
from .job_user import BaseApplicantApplied
from .user import BaseFullNameModel


class BaseLanguageProficiency(BaseModel):
    english: List[BaseKeyValueModel]


class BaseJobMoreInfoModel(BaseModel):
    any_other_documents: Optional[List]
    shift: Optional[str] = None
    tags: Optional[List[BaseKeyValueModel]] = []


class BaseJobMaster(BaseModel):
    job_types: List[BaseKeyValueModel]
    qualifications: List[BaseKeyValueModel]
    languages: BaseLanguageProficiency
    skills: List[BaseKeyValueModel]
    documents: Optional[List[BaseKeyValueModel]]
    hiring_type: Optional[List[BaseKeyValueModel]]
    benefits: Optional[List[BaseKeyValueModel]]
    working_days: int
    contact_name: BaseFullNameModel
    contact_email: EmailStr
    contact_number: int


class BaseJobModel(MongoModel):
    company_id: str
    title: str
    sub_title: str
    description: str
    no_of_opening: int
    salary: BaseRangeModel
    city: str
    area: str
    gig_type: Optional[str]
    gender: Optional[str]
    other_location_info: Optional[str]
    experience: BaseRangeModel
    job_info: BaseJobMaster
    more_info: Optional[BaseJobMoreInfoModel] = None


class JobInModel(BaseJobModel):
    applicants_details: BaseApplicantApplied
    is_updated: Optional[bool] = False
    is_closed: Optional[bool] = False
    is_deleted: Optional[bool] = False
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    closed_on: Optional[datetime]
    deleted_on: Optional[datetime]


class JobOutModel(JobInModel):
    id: OID = Field()


class JobOutWithPagination(MongoModel):
    total_jobs: int
    current_page: int
    jobs: List[JobOutModel]


class JobInfo(BaseModel):
    job_info: BaseJobMaster


class JobListOutModel(MongoModel):
    id: OID = Field()
    title: str
    sub_title: str
    description: str
    status: Optional[bool] = False
    city: str
    area: str
    gig_type: Optional[str]
    gender: Optional[str]
    # applicants_details: BaseApplicantApplied
    is_updated: Optional[bool] = False
    is_closed: Optional[bool] = False
    is_deleted: Optional[bool] = False
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    closed_on: Optional[datetime]
    deleted_on: Optional[datetime]


class JobListOutWithPaginationModel(MongoModel):
    jobs: List[JobListOutModel]
    current_page: int
    total_jobs: int
