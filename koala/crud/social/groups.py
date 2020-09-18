import logging
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from koala.config.collections import SOCIAL_GROUPS
from koala.constants import EMBEDDED_COLLECTION_LIMIT
from koala.crud.jobs_crud.mongo_base import MongoBase
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.social.groups import (
    BaseFullDetailGroupModel,
    BasePostListModel,
    BaseSocialGroup,
    SocialGroupCreateIn,
    SocialGroupCreateOut,
)
from koala.models.social.users import BasePostOwnerModel, BaseFollowerModel, BaseIsFollowed


class SocialGroupsCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(SOCIAL_GROUPS)

    async def create_group(self, group_details: SocialGroupCreateIn) -> any:
        try:
            group_details.created_on = datetime.now()
            result = await self.collection.insert_one(
                group_details.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )
            return BaseIsCreated(id=result, is_created=True) if result else None
        except Exception as e:
            logging.error(f"Error: Create group error {e}")

    async def get_count(self) -> int:
        try:
            filter_condition = {"is_deleted": False}
            count = await self.collection.count(filter_condition)
            return count if count else 0
        except Exception as e:
            logging.error(f"Error: Job count {e}")
            raise e

    async def get_all_groups(
        self, skip: int, limit: int
    ) -> Optional[List[BaseSocialGroup]]:
        try:
            filter_condition = {"is_deleted": False}
            data = await self.collection.find(
                finder=filter_condition,
                skip=skip,
                limit=limit,
                return_doc_id=True,
                extended_class_model=SocialGroupCreateOut,
            )
            return data if data else None
        except Exception as e:
            logging.error(f"Error: Create group error {e}")

    async def get_group_by_id(self, group_id: str) -> any:
        group_id_obj = ObjectId(group_id)
        try:
            return await self.collection.find_one(
                {"_id": group_id_obj},
                return_doc_id=True,
                extended_class_model=SocialGroupCreateOut,
            )
        except Exception as e:
            raise e

    async def followGroup(self, group_id: str, user_map=BaseFollowerModel) -> any:
        try:
            user_map.followed_on = datetime.now()

            finder = {"_id": ObjectId(group_id)}
            updater = {
                "$inc": {"followers.total_followers": 1},
                "$push": {
                    "followers.followers_list": {
                        "$each": [user_map.dict()],
                        "$sort": {"applied_on": -1},
                        "$slice": EMBEDDED_COLLECTION_LIMIT,
                    }
                },
            }

            result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_updated_document=True,
                return_doc_id=True,
                extended_class_model=SocialGroupCreateOut,
            )

            return BaseIsFollowed(id=result.id, is_followed=True) if result else None
        except Exception as e:
            raise e

    async def get_group_users(self, group_id: ObjectId) -> any:
        try:
            pass
        except Exception as e:
            logging.error(f"Error: Create group error {e}")

    async def get_group_user_by_id(self, user_id: str) -> any:
        try:
            logging.info(user_id)
        except Exception as e:
            logging.error(f"Error: Create group error {e}")
