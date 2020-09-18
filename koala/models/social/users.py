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
    email: Optional[EmailStr]
    user_id: OID = Field()


class BaseShareModel(BaseModel):
    whatsapp: int = 0
    in_app_share: int = 0


class BaseFollowerModel(BaseModel):
    name: BaseFullNameModel
    email: Optional[EmailStr]
    user_id: OID = Field()
    followed_on: datetime = None


class FollowerModel(MongoModel):
    total_followers: int = 0
    followers_list: Optional[List[BaseFollowerModel]] = []


class BaseCreatePostModel(MongoModel):
    title: str
    description: str
    content: str


class BaseFullDetailPostModel(BaseCreatePostModel):
    is_group_post: bool = False
    group_id: Optional[OID]
    owner: BasePostOwnerModel
    like: int = 0
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


class BaseFollowedIdRef(BaseModel):
    id: OID = Field()


class BaseIsFollowed(MongoModel):
    id: OID = Field()
    is_followed: bool


class UserFollowed(MongoModel):
    users_followed: Optional[List[OID]] = []


class UsersFollowing(MongoModel):
    total_groups: int = 0
    users_following: Optional[List[OID]] = []
