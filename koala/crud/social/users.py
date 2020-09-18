import logging
from datetime import datetime

from bson import ObjectId
from koala.config.collections import SOCIAL_POSTS, USERS
from koala.constants import EMBEDDED_COLLECTION_LIMIT
from koala.crud.jobs_crud.mongo_base import MongoBase
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.jobs_models.user import UserUpdateOutModel
from koala.models.social.groups import GroupsFollowed
from koala.models.social.users import (
    BaseFollowerModel,
    BaseIsFollowed,
    CreatePostModelIn,
    CreatePostModelOut,
)


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

    async def make_user_follow_user(
        self, user_id: str, user_map=BaseFollowerModel
    ) -> any:
        try:
            # Updating User collection for user followers
            user_map.followed_on = datetime.now()
            user_id_obj = ObjectId(user_id)

            finder = {"_id": user_id_obj}
            updater = {
                "$inc": {"users_following.total_followers": 1},
                "$push": {
                    "users_following.followers_list": {
                        "$each": [user_map.dict()],
                        "$sort": {"applied_on": -1},
                        "$slice": EMBEDDED_COLLECTION_LIMIT,
                    }
                },
            }

            self.collection(USERS)
            user_following = await self.collection.find_one_and_modify(
                find=finder,
                update=updater,
                return_updated_document=True,
                return_doc_id=True,
                extended_class_model=UserUpdateOutModel,
            )

            # Updating User collection to follower
            if user_following.id:
                finder = {"_id": user_map.user_id}
                updater = {
                    "$push": {"users_followed": {"$each": [user_id_obj],}},
                }

                self.collection(USERS)
                user_follower = await self.collection.find_one_and_modify(
                    find=finder,
                    update=updater,
                    return_updated_document=True,
                    return_doc_id=True,
                    extended_class_model=UserUpdateOutModel,
                )

                return (
                    BaseIsFollowed(id=user_id, is_followed=True)
                    if user_following and user_follower
                    else None
                )

        except Exception as e:
            logging.info(e)
            logging.error(f"Error: Create social users error {e}")

    async def get_user_follower(self, user_id: str) -> any:
        try:
            logging.info(user_id)
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")
