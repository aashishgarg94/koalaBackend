from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..core.mongo_model import OID, MongoModel
from ..models.master import BaseKeyValueModel, BaseRangeModel


class BaseLanguageProficiency(BaseModel):
    english: List[BaseKeyValueModel]


class BaseJobMoreInfoModel(BaseModel):
    any_other_documents: Optional[List]
    shift: Optional[str] = None
    tags: Optional[List[BaseKeyValueModel]] = []
    user_applied: Optional[List[str]] = None


class BaseJobMaster(BaseModel):
    job_types: List[BaseKeyValueModel]
    qualifications: List[BaseKeyValueModel]
    languages: BaseLanguageProficiency
    skills: List[BaseKeyValueModel]
    documents: Optional[List[BaseKeyValueModel]]
    hiring_type: Optional[List[BaseKeyValueModel]]
    benefits: Optional[List[BaseKeyValueModel]]


class BaseJobModel(MongoModel):
    company_id: str
    title: str
    sub_title: str
    description: str
    no_of_opening: int
    salary: BaseRangeModel
    city: str
    area: str
    other_location_info: Optional[str]
    experience: BaseRangeModel
    job_info: BaseJobMaster
    more_info: Optional[BaseJobMoreInfoModel] = None


class JobInModel(BaseJobModel):
    is_updated: Optional[bool] = False
    is_deleted: Optional[bool] = False
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    deleted_on: Optional[datetime]


class JobOutModel(JobInModel):
    id: OID = Field()


class JobOutWithPagination(MongoModel):
    total_jobs: int
    current_page: int
    jobs: List[JobOutModel]


class JobInfo(BaseModel):
    job_info: BaseJobMaster
