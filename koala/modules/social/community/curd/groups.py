import logging

from bson import ObjectId

from koala.config.collections import SOCIAL_GROUPS
from koala.dao.mongo_base import MongoBase


class SocialGroups:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(SOCIAL_GROUPS)

    async def check_group_exists(self, group_id: str):
        try:
            finder = {"_id": ObjectId(group_id)}
            find_result = await self.collection.find_one(
                finder=finder, projection={"_id": 1}
            )

            return True if find_result is not None else False
        except Exception as e:
            logging.error(f"Error: While checking if group exists. Error {e}")
            raise e

    async def upsert_post_details(
        self,
        group_id: str,
        post_id: str,
    ) -> any:
        try:
            finder = {"_id": ObjectId(group_id)}
            updater = {
                "$inc": {"posts.total_posts": 1},
                "$push": {
                    "posts.posts_list": {
                        "$each": [ObjectId(post_id)],
                    }
                },
            }

            return await self.collection.find_one_and_modify(
                finder=finder, update=updater, projection={"_id": 1}
            )
        except Exception as e:
            logging.error(f"Error: While creating social group. Error {e}")
            raise e
