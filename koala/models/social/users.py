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


class CommentInModel(BaseModel):
    comment: Optional[str]


class BaseCommentsModel(BaseModel):
    name: BaseFullNameModel
    email: Optional[EmailStr]
    comments: Optional[CommentInModel]


class BasePostOwnerModel(BaseModel):
    name: BaseFullNameModel
    email: Optional[EmailStr]
    user_id: OID = Field()
    current_city: str
    current_company: str
    total_followers: int


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


class BaseShareModel(MongoModel):
    total_share: int = 0
    shared_by: Optional[List[OID]] = []


class BaseShare(BaseModel):
    whatsapp: BaseShareModel
    in_app_share: BaseShareModel


class BaseLikeModel(MongoModel):
    total_likes: int = 0
    liked_by: Optional[List[OID]] = []


class BasePostReportModel(MongoModel):
    total_report: int = 0
    reported_by: Optional[List[OID]] = []


class BaseFullDetailPostModel(BaseCreatePostModel):
    is_group_post: bool = False
    group_id: Optional[OID]
    owner: BasePostOwnerModel
    like: Optional[BaseLikeModel]
    comments: Optional[List[BaseCommentsModel]] = []
    shares: Optional[BaseShare]
    followers: Optional[FollowerModel]
    post_report: Optional[BasePostReportModel]


class CreatePostModelIn(BaseFullDetailPostModel):
    is_updated: Optional[bool] = False
    is_deleted: Optional[bool] = False
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    deleted_on: Optional[datetime]


class CreatePostModelOut(BaseFullDetailPostModel):
    id: OID = Field()


class CreatePostModelOutList(MongoModel):
    post_list: Optional[List[CreatePostModelOut]]


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


class ShareModel(str, Enum):
    whatsapp = "Whatsapp"
    in_app = "In App"


class BasePostMemberModel(MongoModel):
    id: OID = Field()
    full_name: BaseFullNameModel
    users_following: Optional[FollowerModel]


class BasePostMemberCountModel(BaseModel):
    id: OID = Field()
    full_name: BaseFullNameModel
    total_followers: int


class BasePostMemberCountListModel(MongoModel):
    users: Optional[List[BasePostMemberCountModel]]


class BaseCommentIsUpdated(MongoModel):
    id: OID = Field()
    is_updated: bool
    comment: BaseCommentsModel
