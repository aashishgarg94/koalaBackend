import logging

from bson import ObjectId
from fastapi import HTTPException
from koala.config.collections import (
    CACHE_USER_POSTS,
    SOCIAL_POSTS,
    SOCIAL_GROUPS,
    CACHE_POSTS,
    CACHE_COLLECTION_LIMIT,
)
from koala.dao.mongo_base import MongoBase


class CacheUserPosts:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(CACHE_USER_POSTS)

    async def upsert_cache_user_posts(self, user_id: str, post_id: str) -> any:
        try:
            find = {"user_id": ObjectId(user_id)}
            # updater = {"$addToSet": {"post_id": ObjectId(post_id)}}
            updater = {
                "$push": {
                    "posts": {
                        "$each": [ObjectId(post_id)],
                        "$position": 0,
                        "$slice": CACHE_COLLECTION_LIMIT,
                    }
                }
            }
            data = await self.collection.update_one(
                finder=find, update=updater, upsert=True
            )
            return data
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")
            raise HTTPException(status_code=500, detail="Something went wrong")

    async def upsert_cache_posts(self, post_id: str, post_detail: dict) -> any:
        try:
            self.collection(CACHE_POSTS)
            find = {"_id": ObjectId(post_id)}
            replacement = post_detail
            projection = {"_id": 1}
            return await self.collection.find_one_and_replace(
                find,
                replacement=replacement,
                projection=projection,
                upsert=True,
            )
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")
            raise HTTPException(status_code=500, detail="Something went wrong")

    # ================= New Post Collection based on refactoring. Later will move to Post collection =================
    async def get_post_by_post_id(self, post_id: str) -> any:
        try:
            self.collection(SOCIAL_POSTS)
            data = await self.collection.find_one(
                finder={"_id": ObjectId(post_id)}, projection={"_id": 0}
            )

            if data.get("group_id") is not None:
                self.collection(SOCIAL_GROUPS)
                group_name = await self.collection.find(
                    finder={"_id": data.group_id}, projection={"groupName": 1, "_id": 0}
                )

                data.group_name = group_name[0].get("groupName")
            return data
        except Exception as e:
            logging.error(f"Error: Get user post by id {e}")
