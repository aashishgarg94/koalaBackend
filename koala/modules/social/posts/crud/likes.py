import logging
from datetime import datetime

from bson import ObjectId
from koala.config.collections import SOCIAL_POSTS, POSTS_LIKES
from koala.dao.mongo_base import MongoBase


class Likes:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(SOCIAL_POSTS)

    async def like_post(self, post_id: str, user_id: ObjectId) -> any:
        try:
            find = {"_id": ObjectId(post_id)}
            updater = {"$inc": {"total_likes": 1}}
            projection = {"_id": 1}
            update_post_resp = await self.collection.find_one_and_modify(
                find, update=updater, projection=projection
            )

            # Update `POSTS_LIKE` COLLECTION
            self.collection(POSTS_LIKES)
            find = {"_id": ObjectId(post_id)}
            updater = {
                "$push": {
                    "liked_by": {"user_id": user_id, "liked_at": datetime.utcnow()}
                }
            }
            update_like_resp = await self.collection.find_one_and_modify(
                find,
                update=updater,
                projection=projection,
                upsert=True,
            )

            return post_id if update_post_resp and update_like_resp else None

        except Exception as e:
            logging.error(f"Error: While deleting post {e}")
            raise e

    async def get_by_post_id_and_user_id(self, post_id: str, user_id: str) -> any:
        try:
            self.collection(POSTS_LIKES)
            find = {"_id": ObjectId(post_id), "liked_by.user_id": ObjectId(user_id)}
            return await self.collection.find_one(
                finder=find,
            )

        except Exception as e:
            logging.error(f"Error: While deleting post {e}")
            raise e
