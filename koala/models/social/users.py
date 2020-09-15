from datetime import datetime
from enum import Enum
from typing import List, Optional

from koala.constants import GOLD, NORMAL
from koala.core.mongo_model import OID, MongoModel
from koala.models.jobs_models.master import BaseFullNameModel
from pydantic import BaseModel, EmailStr, Field


class AllowedActionModel(str, Enum):
    gold = GOLD
    normal = NORMAL


class BaseCommentsModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    comment: Optional[str]


class BasePostOwnerModel(BaseModel):
    name: BaseFullNameModel
    email: str
    user_id: OID = Field()


class BaseShareModel(BaseModel):
    whatsapp: int = 0
    in_app_share: int = 0


class BaseFollowerModel(BaseModel):
    name: Optional[str]
    email: Optional[str]


class FollowerModel(BaseModel):
    followersCount: int = 0
    followers: Optional[List[BaseFollowerModel]]


class BaseCreatePostModel(MongoModel):
    title: str
    description: str
    content: str


class BaseFullDetailPostModel(BaseCreatePostModel):
    owner: BasePostOwnerModel
    like: int = 0
    membership_type: Optional[str] = NORMAL
    comments: Optional[List[BaseCommentsModel]] = []
    shares: Optional[BaseShareModel]
    followers: Optional[FollowerModel]


class CreatePostModelIn(BaseFullDetailPostModel):
    is_updated: Optional[bool] = False
    is_deleted: Optional[bool] = False
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    deleted_on: Optional[datetime]


class CreatePostModelOut(BaseFullDetailPostModel):
    id: OID = Field()


class CreatePostModelPaginationModel(MongoModel):
    current_page: int
    total_posts: int
    posts: List[CreatePostModelOut]
