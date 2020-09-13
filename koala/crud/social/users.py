import logging

from koala.config.collections import SOCIAL_USERS
from koala.crud.jobs_crud.mongo_base import MongoBase


class SocialUsersCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(SOCIAL_USERS)

    async def create_group(self, post_details: dict) -> any:
        try:
            logging.info(post_details)
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")

    async def get_user_all_posts(self, user_id: str) -> any:
        try:
            pass
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")

    async def get_user_post_by_id(self, post_id: str) -> any:
        try:
            logging.info(post_id)
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")

    async def make_user_follow_group(self, user_details: dict) -> any:
        try:
            logging.info(user_details)
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")

    async def get_user_followed_groups(self, user_id: str) -> any:
        try:
            logging.info(user_id)
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")

    async def get_user_follower(self, user_id: str) -> any:
        try:
            logging.info(user_id)
        except Exception as e:
            logging.error(f"Error: Create social users error {e}")
