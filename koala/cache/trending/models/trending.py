from typing import List, Optional

from pydantic import Field
from pydantic.main import BaseModel

from koala.core.mongo_model import OID


class BasePostIdListModel(BaseModel):
    post_id: OID = Field()
    is_liked: bool


class BaseDeviceModel(BaseModel):
    user_id: OID = Field()
    total_posts: Optional[int] = 0
    posts: Optional[List[BasePostIdListModel]] = []
