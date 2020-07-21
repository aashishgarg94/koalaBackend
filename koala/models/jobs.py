from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BaseTagModel(BaseModel):
    name: str


class BaseRangeModel(BaseModel):
    start_range: int
    end_range: int
    range_type: Optional[str]


class BaseJobMoreInfoModel(BaseModel):
    shift: Optional[str] = None
    tags: Optional[List[BaseTagModel]]


class BaseJobModel(BaseModel):
    company_id: str
    title: str
    sub_title: str
    experience: BaseRangeModel
    salary: BaseRangeModel
    location: str
    description: str
    more_info: Optional[BaseJobMoreInfoModel] = None


class JobInModel(BaseJobModel):
    is_updated: Optional[bool] = False
    is_deleted: Optional[bool] = False
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    deleted_on: Optional[datetime]


class JobOutModel(JobInModel):
    id: int


class JobOutWithPagination(BaseModel):
    total_jobs: int
    current_page: int
    jobs: List[JobOutModel]


class BaseIsCreated(BaseModel):
    is_created: bool


class BaseIsDeleted(BaseModel):
    is_deleted: bool


class BaseIsUpdated(BaseModel):
    is_updated: bool
