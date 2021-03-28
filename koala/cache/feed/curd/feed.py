import logging

from bson import ObjectId
from koala.config.collections import USERS, CACHE_FEED_POSTS
from koala.dao.mongo_base import MongoBase


class CacheFeedPosts:
    def __init__(self):
        self.collection = MongoBase()

    async def find_user_followers(self, user_id: str) -> any:
        try:
            self.collection(USERS)
            find = {"_id": ObjectId(user_id)}
            projection = {"users_following": 1, "_id": 0}
            data = await self.collection.find_one(finder=find, projection=projection)
            followers_list = []
            for data in data.get("users_following").get("followers_list"):
                followers_list.append(data.get("user_id"))
            return followers_list
        except Exception as e:
            raise e

    # Union(it should be up to date) - post - like, unlike, action
    async def upsert_cache_feed_posts(self, post_id: str, followers_list: list) -> any:
        try:
            self.collection(CACHE_FEED_POSTS)

            # 1. Update followers posts in `CACHE FEED POSTS` collection
            for follower in followers_list:
                find = {"user_id": follower}
                updater = {
                    "$push": {
                        "posts": {
                            "post_id": ObjectId(post_id),
                            "is_liked": False,
                        }
                    }
                }
                await self.collection.find_one_and_modify(
                    finder=find,
                    update=updater,
                    upsert=True,
                )

            return True
        except Exception as e:
            logging.error(f"Error: While creating user feed posts")
            raise e

    async def update_cache_feed_post(
        self, user_id: str, post_id: str, is_liked: bool
    ) -> any:
        try:
            find = {"user_id": ObjectId(user_id), "posts.post_id": ObjectId(post_id)}
            updater = {"$set": {"posts.$.is_liked": is_liked}}

            self.collection(CACHE_FEED_POSTS)
            data = await self.collection.update_one(finder=find, update=updater)

            if data.matched_count == 0:
                find = {"user_id": ObjectId(user_id)}
                updater = {
                    "$push": {
                        "posts": {
                            "post_id": ObjectId(post_id),
                            "is_liked": is_liked,
                        }
                    }
                }
                await self.collection.find_one_and_modify(
                    finder=find,
                    update=updater,
                    upsert=True,
                )
            return True
        except Exception as e:
            logging.error(f"Error: While creating user feed posts")
            raise e

    async def upsert_cache_trending_posts(
        self, user_id, post_id, following_list
    ) -> any:
        try:
            # Just dump the post in trending for now
            pass
        except Exception as e:
            logging.error(f"Error: While creating user feed posts")
            raise e
