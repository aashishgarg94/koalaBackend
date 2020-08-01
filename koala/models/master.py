from typing import List, Optional

from pydantic import BaseModel, Field

from ..core.mongo_model import OID, MongoModel


class GigTypeModel(BaseModel):
    gig_types: List[str] = []


class OpCityModel(BaseModel):
    op_cities: List[str] = []


class OpAreaModel(BaseModel):
    op_areas: List[str] = []


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
