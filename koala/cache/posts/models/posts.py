from typing import List

from pydantic import Field
from pydantic.main import BaseModel
from enum import Enum

from koala.core.mongo_model import OID


class AllowedActionModel(str, Enum):
    none = 0
    image = 1
    video = 2


class BasePostGroupModel(BaseModel):
    id: OID = Field()
    name: str
    image: str


class BasePostOwnerModel(BaseModel):
    id: OID = Field()
    name: str
    image: str


class BasePostModel(BaseModel):
    media_type: int
    media_url: str
    content: str
    tags: List[str]
    is_group_posts: bool
    group: BasePostGroupModel
    owner: BasePostOwnerModel
    total_like: int
    total_comments: int
    total_whatsapp_share: int
    total_inapp_share: int
    is_pinned: bool
