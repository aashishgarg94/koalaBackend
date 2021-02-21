from datetime import datetime
from enum import Enum
from typing import List, Optional

from koala.constants import GOLD, NORMAL
from koala.core.mongo_model import OID, MongoModel
from koala.models.jobs_models.master import BaseFullNameModel
from pydantic import BaseModel, Field


class AllowedActionModel(str, Enum):
    gold = GOLD
    normal = NORMAL


class CommentInModel(BaseModel):
    comment: Optional[str]


class BaseCommentsModel(BaseModel):
    name: BaseFullNameModel
    username: str
    comments: Optional[CommentInModel]
    profile_image: Optional[str]
    user_id: Optional[OID]


class BasePostOwnerModel(BaseModel):
    name: BaseFullNameModel
    username: str
    user_id: OID = Field()
    current_city: str
    current_company: str
    total_followers: int
    profile_pic: Optional[str] = None


class BaseFollowerModel(BaseModel):
    name: BaseFullNameModel
    username: str
    user_id: OID = Field()
    followed_on: datetime = None


class FollowerModel(MongoModel):
    total_followers: int = 0
    followers_list: Optional[List[BaseFollowerModel]] = []


class BaseCreatePostModel(MongoModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class BaseCreateAdditionalFeedModel(MongoModel):
    position: int =  0
    element_type: str = ""
    banner1url: Optional[str] = None
    banner1name: Optional[str] = None
    banner1categoryid: Optional[str] = None
    banner1categorytitle: Optional[str] = None
    banner2url: Optional[str] = None
    banner2name: Optional[str] = None
    banner2categoryid: Optional[str] = None
    banner2categorytitle: Optional[str] = None
    videoTitle: Optional[str] = None
    videocategoryid: Optional[str] = None
    videocategorytitle: Optional[str] = None
    videoid: Optional[str] = None

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
    post_image: Optional[str] = None
    group_name: Optional[str] = ""


class CreatePostModelIn(BaseFullDetailPostModel):
    is_updated: Optional[bool] = False
    is_deleted: Optional[bool] = False
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    deleted_on: Optional[datetime]


class CreatePostModelOut(BaseFullDetailPostModel):
    id: OID = Field()

class CreateAdditionalFeedModelOut(BaseCreateAdditionalFeedModel):
    id: OID = Field()

class CreatePostModelOutList(MongoModel):
    # current_page: int
    # total_posts: int
    # request_limit: int
    # posts: List[CreatePostModelOut]
    more_pages: Optional[bool] = False
    post_list: List[CreatePostModelOut]


class CreatePostModelPaginationModel(MongoModel):
    # current_page: int
    # total_posts: int
    # request_limit: int
    more_pages: bool
    post_list: List[CreatePostModelOut]
    additional_feed: Optional[List[CreateAdditionalFeedModelOut]]


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


class PostUserBioModel(BaseModel):
    current_company: str = None


class BasePostMemberModel(MongoModel):
    id: OID = Field()
    profile_image: Optional[str] = None
    full_name: Optional[BaseFullNameModel] = None
    users_following: Optional[FollowerModel]
    bio: Optional[PostUserBioModel] = None


class BasePostMemberCountModel(BaseModel):
    id: OID = Field()
    profile_image: Optional[str] = None
    full_name: Optional[BaseFullNameModel] = None
    total_followers: int
    current_company: Optional[str] = None


class BasePostMemberCountListModel(MongoModel):
    users: Optional[List[BasePostMemberCountModel]]


class BaseCommentIsUpdated(MongoModel):
    id: OID = Field()
    is_updated: bool
    comment: BaseCommentsModel


class PostByTagInModel(BaseModel):
    tags: List
