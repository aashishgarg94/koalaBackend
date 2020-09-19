import logging
from datetime import datetime

from bson import ObjectId
from koala.config.collections import SOCIAL_GROUPS, SOCIAL_POSTS, USERS
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
    CreatePostModelOutList,
    FollowerModel,
    UserFollowed,
)


class SocialPostsCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(SOCIAL_POSTS)

    async def create_post(
        self, post_details: CreatePostModelIn, is_group_post: bool, group_id: str
    ) -> any:
        try:
            post_details.created_on = datetime.now()
            if is_group_post is True:
                post_details.is_group_post = True
                post_details.group_id = ObjectId(group_id)
            insert_id = await self.collection.insert_one(
                post_details.dict(),
                return_doc_id=True,
                extended_class_model=BaseIsCreated,
            )

            # Update group post list with post is group post
            if is_group_post is True:
                finder = {"_id": ObjectId(group_id)}
                updater = {
                    "$inc": {"posts.total_posts": 1},
                    "$push": {
                        "posts.posts_list": {
                            "$each": [insert_id],
                            "$sort": {"applied_on": -1},
                            "$slice": EMBEDDED_COLLECTION_LIMIT,
                        }
                    },
                }

                self.collection(SOCIAL_GROUPS)
                group_result = await self.collection.find_one_and_modify(
                    find=finder,
                    update=updater,
                    return_updated_document=True,
                    return_doc_id=False,
                )

                return (
                    BaseIsCreated(id=insert_id, is_created=True)
                    if insert_id and group_result
                    else None
                )
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
            logging.error(f"Error: Get user all posts {e}")

    async def get_user_post_by_id(self, post_id: str) -> any:
        try:
            post_id_obj = ObjectId(post_id)
            return await self.collection.find_one(
                {"_id": post_id_obj},
                return_doc_id=True,
                extended_class_model=CreatePostModelOut,
            )
        except Exception as e:
            logging.error(f"Error: Get user post by id {e}")

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
            logging.error(f"Error: Get user followed groups {e}")

    async def make_user_follow_user(
        self, user_id: str, user_map=BaseFollowerModel
    ) -> BaseIsFollowed:
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
            logging.error(f"Error: Make user follow {e}")

    async def get_user_followed(
        self, user_id: ObjectId, skip: int, limit: int
    ) -> CreatePostModelOutList:
        try:
            social_data = await self.collection.find(
                finder={"owner.user_id": user_id},
                skip=skip,
                limit=limit,
                return_doc_id=True,
                extended_class_model=CreatePostModelOut,
            )
            return CreatePostModelOutList(post_list=social_data)
        except Exception as e:
            logging.error(f"Error: Get user followed {e}")

    async def get_user_following(self, user_id: str) -> FollowerModel:
        try:
            self.collection(USERS)
            data = await self.collection.find(
                finder={"_id": user_id},
                projection={"users_following": 1, "_id": 0},
                return_doc_id=False,
            )

            return FollowerModel(
                total_followers=data[0]["users_following"]["total_followers"],
                followers_list=data[0]["users_following"]["followers_list"],
            )
        except Exception as e:
            logging.error(f"Error: Get user following {e}")

    async def get_feed_count(self, is_group_post: bool = False) -> int:
        try:
            filter_condition = {"is_deleted": False, "is_group_post": is_group_post}
            count = await self.collection.count(filter_condition)
            return count if count else 0
        except Exception as e:
            logging.error(f"Error: Feed count {e}")
            raise e

    async def get_user_feed(
        self, skip: int, limit: int, group_id: str = None
    ) -> CreatePostModelOutList:
        try:
            finder = {
                "$query": {"group_id": ObjectId(group_id), "is_deleted": False},
                "$orderby": {"created_on": -1},
            }
            social_data = await self.collection.find(
                finder=finder,
                skip=skip,
                limit=limit,
                return_doc_id=True,
                extended_class_model=CreatePostModelOut,
            )
            return CreatePostModelOutList(post_list=social_data)
        except Exception as e:
            logging.error(f"Error: Get user followed {e}")
