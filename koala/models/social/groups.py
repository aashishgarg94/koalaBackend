from datetime import datetime
from typing import List, Optional

from koala.core.mongo_model import OID, MongoModel
from pydantic import Field


class BaseSocialGroup(MongoModel):
    groupName: str
    groupDescription: str
    groupOwner: str


class SocialGroupCreateIn(BaseSocialGroup):
    is_updated: Optional[bool] = False
    is_deleted: Optional[bool] = False
    created_on: Optional[datetime]
    updated_on: Optional[datetime]
    deleted_on: Optional[datetime]


class SocialGroupCreateOut(BaseSocialGroup):
    id: OID = Field()


class GroupsWithPaginationModel(MongoModel):
    current_page: int
    total_groups: int
    groups: List[SocialGroupCreateOut]
