import logging
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from koala.config.collections import SOCIAL_GROUPS, USERS
from koala.constants import EMBEDDED_COLLECTION_LIMIT
from koala.crud.jobs_crud.mongo_base import MongoBase
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.jobs_models.user import UserUpdateOutModel
from koala.models.social.groups import (
    BaseGroupMemberCountListModel,
    BaseGroupMemberCountModel,
    BaseGroupMemberModel,
    BaseSocialGroup,
    SocialGroupCreateIn,
    SocialGroupCreateOut,
)
from koala.models.social.users import BaseFollowerModel, BaseIsFollowed, FollowerModel


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
            logging.error(f"Error: Get Count {e}")
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
            logging.error(f"Error: Get all groups {e}")

    async def get_group_by_id(self, group_id: str) -> any:
        group_id_obj = ObjectId(group_id)
        try:
            return await self.collection.find_one(
                {"_id": group_id_obj},
                return_doc_id=True,
                extended_class_model=SocialGroupCreateOut,
            )
        except Exception as e:
            logging.error(f"Error: Get group by id {e}")

    async def followGroup(
        self, group_id: str, user_map=BaseFollowerModel
    ) -> BaseIsFollowed:
        try:
            # Updating Social group collection
            user_map.followed_on = datetime.now()
            group_id_obj = ObjectId(group_id)

            finder = {"_id": group_id_obj}
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

            group_result = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_updated_document=True,
                return_doc_id=True,
                extended_class_model=SocialGroupCreateOut,
            )

            # Updating User collection
            if group_result.id:
                finder = {"_id": user_map.user_id}
                updater = {
                    "$push": {
                        "groups_followed": {
                            "$each": [group_id_obj],
                        }
                    },
                }

                self.collection(USERS)
                user_result = await self.collection.find_one_and_modify(
                    find=finder,
                    update=updater,
                    return_updated_document=True,
                    return_doc_id=True,
                    extended_class_model=UserUpdateOutModel,
                )

                return (
                    BaseIsFollowed(id=group_id, is_followed=True)
                    if group_result and user_result
                    else None
                )
        except Exception as e:
            logging.error(f"Error: Follow group {e}")

    async def get_group_users(self, group_id: str) -> FollowerModel:
        try:
            data = await self.collection.find(
                finder={"_id": ObjectId(group_id)},
                projection={"followers": 1, "_id": 0},
                return_doc_id=False,
            )

            return FollowerModel(
                total_followers=data[0]["followers"]["total_followers"],
                followers_list=data[0]["followers"]["followers_list"],
            )
        except Exception as e:
            logging.error(f"Error: Get group users {e}")

    async def get_groups_by_user_id(
        self,
        user_id: str,
    ) -> any:
        try:
            filter_condition = {"_id": ObjectId(user_id)}

            self.collection(USERS)
            return await self.collection.find(
                finder=filter_condition,
                return_doc_id=False,
                projection={"groups_followed": 1, "_id": 0},
            )
        except Exception as e:
            logging.error(f"Error: Get group count by user_id {e}")

    async def get_group_details(
        self, groups_list: list
    ) -> BaseGroupMemberCountListModel:
        try:
            filter_condition = {"_id": {"$in": groups_list}}
            self.collection(SOCIAL_GROUPS)

            user_group_list = await self.collection.find(
                finder=filter_condition,
                projection={"groupName": 1, "followers": 1},
                return_doc_id=True,
                extended_class_model=BaseGroupMemberModel,
            )
            user_group_data = []
            if len(user_group_list) > 0:
                for group in user_group_list:
                    user_group_data.append(
                        BaseGroupMemberCountModel(
                            id=group.id,
                            group_name=group.groupName,
                            total_followers=group.followers.total_followers,
                        )
                    )

            return BaseGroupMemberCountListModel(user_groups=user_group_data)
        except Exception as e:
            logging.error(f"Error: Get group count by user_id {e}")
