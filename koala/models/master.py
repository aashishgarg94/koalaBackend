from typing import List

from pydantic import BaseModel


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
