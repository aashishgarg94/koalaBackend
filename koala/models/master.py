from typing import List

from pydantic import BaseModel


class GigTypeModal(BaseModel):
    names: List[str] = []
