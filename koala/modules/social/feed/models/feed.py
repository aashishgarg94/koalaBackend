from datetime import datetime
from typing import List, Optional

from pydantic import Field
from pydantic.main import BaseModel
from enum import Enum

from koala.core.mongo_model import OID


class BaseMediaTypeModel(str, Enum):
    only_content = "only_content"
    image = "image"
    video = "video"


class BasePostModel(BaseModel):
    media_type: BaseMediaTypeModel
    media_url: str
    content: str
    tags: List[str]
    owner: OID = Field()
    is_group_post: bool
    group_id: OID = Field()
    total_like: int
    total_comments: int
    total_share: int
    is_pinned: bool
    is_post_reported: bool


class BasePostInModel(BasePostModel):
    version: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
