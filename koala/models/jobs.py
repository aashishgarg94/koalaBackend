from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class BaseTagModal(BaseModel):
    name: str


class BaseRangeModel(BaseModel):
    start_range: int
    end_range: int
    range_type: Optional[str]


class BaseJobMoreInfoModel(BaseModel):
    shift: Optional[str] = None
    tags: Optional[List[BaseTagModal]]


class BaseJobModel(BaseModel):
    title: str
    sub_title: str
    experience: BaseRangeModel
    salary: BaseRangeModel
    location: str
    description: str
    more_info: Optional[BaseJobMoreInfoModel] = None


class BaseJobModelDB(BaseJobModel):
    posted_on: date
    company_id: str  # TODO: company id will be here

    class Config:
        orm_mode = True


class JobCreatedOut(BaseModel):
    is_created: bool
