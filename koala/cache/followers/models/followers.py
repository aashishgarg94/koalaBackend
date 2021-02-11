from typing import List, Optional

from pydantic import Field
from pydantic.main import BaseModel

from koala.core.mongo_model import OID


class BaseDeviceModel(BaseModel):
    user_id: OID = Field()
    total_followers: Optional[int] = 0
    followers: Optional[List[str]] = []
