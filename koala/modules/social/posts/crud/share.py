import logging

from bson import ObjectId
from koala.config.collections import SOCIAL_POSTS
from koala.dao.mongo_base import MongoBase


class Share:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(SOCIAL_POSTS)

    async def share_post(self, post_id: str) -> any:
        try:
            find = {"_id": ObjectId(post_id)}
            updater = {"$inc": {"total_share": 1}}
            projection = {"_id": 1}
            return await self.collection.find_one_and_modify(
                find, update=updater, projection=projection
            )
        except Exception as e:
            logging.error(f"Error: While deleting post {e}")
            raise e
