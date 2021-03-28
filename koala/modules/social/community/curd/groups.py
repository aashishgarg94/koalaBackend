import logging
from datetime import datetime

from bson import ObjectId

from koala.config.collections import USER_SOCIAL
from koala.dao.mongo_base import MongoBase


class UserSocial:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(USER_SOCIAL)

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
