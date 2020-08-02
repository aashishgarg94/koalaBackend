from typing import List, Optional

from pydantic import BaseModel, Field

from ..core.mongo_model import OID, MongoModel


class BaseNameModel(MongoModel):
    id: OID = Field()
    name: str


class LanguageBaseNameModel(MongoModel):
    id: OID = Field()
    name: str
    language: str


class GigTypeModel(MongoModel):
    gig_types: List[BaseNameModel] = []


class OpCityModel(MongoModel):
    op_cities: List[BaseNameModel] = []


class OpAreaModel(MongoModel):
    op_areas: List[BaseNameModel] = []


class GlobalSequenceIn(BaseModel):
    _id: str


# TODO: Need to add the check in CRUD file to check if sequence is of the same collection
class GlobalSequenceOut(BaseModel):
    _id: str
    next_seq: int


class BaseRangeModel(BaseModel):
    start_range: int
    end_range: int
    range_type: Optional[str]


class BaseIsCreated(MongoModel):
    id: OID = Field()
    is_created: bool


class BaseIsDisabled(MongoModel):
    id: OID = Field()
    is_disabled: bool


class BaseIsDeleted(MongoModel):
    is_deleted: bool


class BaseIsUpdated(MongoModel):
    is_updated: bool


class BaseKeyValueModel(BaseModel):
    name: str


class JobMasterModel(MongoModel):
    benefits: List[BaseNameModel]
    documents: List[BaseNameModel]
    hiring_types: List[BaseNameModel]
    job_types: List[BaseNameModel]
    languages: List[LanguageBaseNameModel]
    qualifications: List[BaseNameModel]
    skills: List[BaseNameModel]
