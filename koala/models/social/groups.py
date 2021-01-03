from datetime import datetime
from typing import List, Optional

from koala.core.mongo_model import OID, MongoModel
from koala.models.social.users import BasePostOwnerModel, FollowerModel
from pydantic import BaseModel, Field


class BaseSocialGroup(MongoModel):
    groupName: str
    groupDescription: str
    group_image: Optional[str] = None


class BaseSocialPostModel(BaseModel):
    total_posts: int = 0
    posts_list: Optional[List[OID]] = []


class SocialGroupCreateIn(BaseSocialGroup):
    owner: Optional[BasePostOwnerModel]
    posts: Optional[BaseSocialPostModel]
    followers: Optional[FollowerModel]
    is_updated: Optional[bool] = False
    is_deleted: Optional[bool] = False
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    deleted_on: Optional[datetime]


class SocialGroupCreateOut(SocialGroupCreateIn):
    id: OID = Field()


class SocialGroupInfo(BaseSocialGroup):
    owner: Optional[BasePostOwnerModel]
    followers: Optional[FollowerModel]


class SocialGroupListOut(SocialGroupInfo):
    id: OID = Field()


class GroupsWithPaginationModel(MongoModel):
    current_page: int
    total_groups: int
    groups: List[SocialGroupListOut]


class GroupsFollowed(MongoModel):
    total_groups: int = 0
    group_list: Optional[List[OID]] = []


class UsersFollowed(MongoModel):
    total_users: int = 0
    user_list: Optional[List[OID]] = []


class BaseGroupMemberModel(MongoModel):
    id: OID = Field()
    groupName: str
    group_image: Optional[str] = None
    followers: Optional[FollowerModel]


class BaseGroupMemberCountModel(BaseModel):
    id: OID = Field()
    group_name: str
    group_image: Optional[str] = None
    total_followers: int


class BaseGroupMemberCountListModel(MongoModel):
    user_groups: Optional[List[BaseGroupMemberCountModel]]
