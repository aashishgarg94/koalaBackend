import logging
from datetime import datetime

from bson import ObjectId
from koala.config.collections import SOCIAL_POSTS, USERS
from koala.crud.jobs_crud.mongo_base import MongoBase
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.social.groups import GroupsFollowed
from koala.models.social.users import CreatePostModelIn, CreatePostModelOut


class SocialUsersCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(SOCIAL_POSTS)

    async def create_post(self, post_details: CreatePostModelIn) -> any:
        try:
            post_details.created_on = datetime.now()
            result = await self.collection.insert_one(
                post_details.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )
            return BaseIsCreated(id=result, is_created=True) if result else None
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")

    async def get_count(self) -> int:
        try:
            filter_condition = {"is_deleted": False}
            count = await self.collection.count(filter_condition)
            return count if count else 0
        except Exception as e:
            logging.error(f"Error: Job count {e}")
            raise e

    async def get_user_all_posts(self, skip: int, limit: int) -> any:
        try:
            filter_condition = {"is_deleted": False}
            data = await self.collection.find(
                finder=filter_condition,
                skip=skip,
                limit=limit,
                return_doc_id=True,
                extended_class_model=CreatePostModelOut,
            )
            return data if data else None
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")

    async def get_user_post_by_id(self, post_id: str) -> any:
        try:
            post_id_obj = ObjectId(post_id)
            return await self.collection.find_one(
                {"_id": post_id_obj},
                return_doc_id=True,
                extended_class_model=CreatePostModelOut,
            )
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")

    async def get_user_followed_groups(self, user_id: str) -> GroupsFollowed:
        try:
            self.collection(USERS)
            data = await self.collection.find(
                finder={"_id": ObjectId(user_id)},
                projection={"groups_followed": 1, "_id": 0},
                return_doc_id=False,
            )
            return GroupsFollowed(
                total_groups=len(data[0]["groups_followed"]),
                group_list=data[0]["groups_followed"],
            )
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")

    async def make_user_follow_group(self, user_details: dict) -> any:
        try:
            logging.info(user_details)
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")

    async def get_user_follower(self, user_id: str) -> any:
        try:
            logging.info(user_id)
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")
