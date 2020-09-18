from datetime import datetime
from typing import List, Optional

from koala.core.mongo_model import OID, MongoModel
from koala.models.social.users import (
    BaseCommentsModel,
    BasePostOwnerModel,
    BaseShareModel,
    FollowerModel,
)
from pydantic import BaseModel, Field


class BaseSocialGroup(MongoModel):
    groupName: str
    groupDescription: str


class BaseFullDetailGroupModel(BaseSocialGroup):
    owner: BasePostOwnerModel
    like: int = 0
    comments: Optional[List[BaseCommentsModel]] = []
    shares: Optional[BaseShareModel]
    followers: Optional[FollowerModel]


class BasePostListModel(BaseModel):
    owner: BasePostOwnerModel
    like: int = 0
    comments: Optional[List[BaseCommentsModel]] = []
    shares: Optional[BaseShareModel]


class BaseSocialPostModel(BaseModel):
    total_posts: int = 0
    posts_list: Optional[List[BasePostListModel]] = []


class SocialGroupCreateIn(BaseSocialGroup):
    owner: BasePostOwnerModel
    posts: Optional[BaseSocialPostModel]
    followers: Optional[FollowerModel]
    is_updated: Optional[bool] = False
    is_deleted: Optional[bool] = False
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    deleted_on: Optional[datetime]


class SocialGroupCreateOut(SocialGroupCreateIn):
    id: OID = Field()


class GroupsWithPaginationModel(MongoModel):
    current_page: int
    total_groups: int
    groups: List[SocialGroupCreateOut]


class GroupsFollowed(MongoModel):
    total_groups: int = 0
    group_list: Optional[List[OID]] = []
