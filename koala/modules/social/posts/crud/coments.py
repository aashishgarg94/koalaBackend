import logging

from bson import ObjectId

from koala.config.collections import POSTS_COMMENTS
from koala.dao.mongo_base import MongoBase
from koala.modules.social.posts.models.coments import BasePostCommentsModel


class Comments:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(POSTS_COMMENTS)

    async def comment_post(
        self, post_id: str, comment_details: BasePostCommentsModel
    ) -> any:
        try:
            find = {"_id": ObjectId(post_id)}
            updater = {"$push": {"comments": comment_details.dict()}}
            # updater = {
            #     "$inc": {"total_comments": 1},
            #     "$set": {"comments": comment_details.dict()},
            # }
            projection = {"_id": 1}
            return await self.collection.find_one_and_modify(
                find,
                update=updater,
                projection=projection,
                upsert=True,
            )
        except Exception as e:
            logging.error(f"Error: While deleting post {e}")
            raise e
