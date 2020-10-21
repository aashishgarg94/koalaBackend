from typing import List, Optional

from koala.core.mongo_model import OID, MongoModel
from pydantic import BaseModel, Field


class GpsModel(BaseModel):
    latitude: float
    longitude: float


class BaseFullNameModel(BaseModel):
    first_name: str
    middle_name: Optional[str] = ""
    last_name: Optional[str] = ""


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


class SocialTagsModel(MongoModel):
    tags: List[BaseNameModel] = []


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
    id: OID = Field()
    is_deleted: bool


class BaseIsJobClosed(MongoModel):
    id: OID = Field()
    is_closed: bool


class BaseIsUpdated(MongoModel):
    id: OID = Field()
    is_updated: bool


class BaseIsSaved(MongoModel):
    id: OID = Field()
    is_saved: bool


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


class BaseAddress(BaseModel):
    building_number: Optional[str]
    street: Optional[str]
    area: Optional[str]
    city: Optional[str]
    landmark: Optional[str]
    location_coordinates: Optional[GpsModel]


class BaseNotFound(BaseModel):
    status_code: int = 404
    message: str = "Record not found"
