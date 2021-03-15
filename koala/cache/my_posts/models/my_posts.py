from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel

from koala.core.mongo_model import OID


class BaseDeviceModel(BaseModel):
    user_id: OID = Field()
    total_posts: Optional[int] = 0
    posts: Optional[list] = []
