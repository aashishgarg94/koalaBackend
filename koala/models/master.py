from typing import List

from pydantic import BaseModel


class GigTypeModal(BaseModel):
    gig_types: List[str] = []


class OpCityModal(BaseModel):
    op_cities: List[str] = []


class OpAreaModal(BaseModel):
    op_areas: List[str] = []


class GlobalSequenceIn(BaseModel):
    _id: str


class GlobalSequenceOut(BaseModel):
    _id: str
    next_seq: int
