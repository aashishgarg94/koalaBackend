import logging

from bson import ObjectId
from fastapi import HTTPException
from koala.config.collections import CACHE_USER_POSTS
from koala.dao.mongo_base import MongoBase


class CacheUserPosts:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(CACHE_USER_POSTS)

    async def upsert_cache_user_posts(self, user_id, post_id) -> any:
        try:
            find = {"_id": ObjectId(user_id)}
            updater = {"$addToSet": {"post_id": post_id}}
            projection = {"_id": 1}
            return await self.collection.find_one_and_modify(
                find,
                update=updater,
                projection=projection,
                upsert=True,
            )
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")
            raise HTTPException(status_code=500, detail="Something went wrong")
