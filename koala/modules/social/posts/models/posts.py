from datetime import datetime
from typing import List, Optional

from pydantic import Field
from pydantic.main import BaseModel
from enum import Enum

from koala.constants import SCHEMA_VERSION
from koala.core.mongo_model import OID, MongoModel


class BaseMediaTypeModel(str, Enum):
    only_content = "only_content"
    image = "image"
    video = "video"


class BasePostModel(BaseModel):
    media_type: BaseMediaTypeModel
    media_url: Optional[str] = None
    content: str
    tags: List[str]
    owner: OID = Field()
    is_group_post: Optional[bool] = False
    group_id: Optional[OID] = None


class BasePostInModel(BasePostModel):
    total_likes: Optional[int] = 0
    total_comments: Optional[int] = 0
    total_shares: Optional[int] = 0
    is_pinned: Optional[bool] = False
    is_reported: Optional[bool] = False
    is_deleted: Optional[bool] = False
    version: Optional[int] = SCHEMA_VERSION
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    reported_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class CreatePostOutModel(MongoModel):
    id: OID = Field()


class BasePostUpdateModel(BaseModel):
    media_type: BaseMediaTypeModel
    media_url: Optional[str] = None
    content: str
    tags: List[str]
    owner: OID = Field()
    updated_at: Optional[datetime] = None


# ================ Report Post Models ================


class BaseReportOwnerModel(BaseModel):
    user_id: OID = Field()
    reported_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class BaseReportPostModel(BaseModel):
    post_id: OID = Field()
    total_reports: Optional[int] = 0
    reported_by: Optional[List[BaseReportOwnerModel]] = []


# ===================================================
