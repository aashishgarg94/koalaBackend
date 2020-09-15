import logging
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from koala.config.collections import SOCIAL_GROUPS
from koala.crud.jobs_crud.mongo_base import MongoBase
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.social.groups import (
    BaseSocialGroup,
    SocialGroupCreateIn,
    SocialGroupCreateOut,
)


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
