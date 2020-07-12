from typing import List

from pydantic import BaseModel


class GigTypeModal(BaseModel):
    gig_types: List[str] = []


class OpCityModal(BaseModel):
    op_cities: List[str] = []


class OpAreaModal(BaseModel):
    op_areas: List[str] = []
