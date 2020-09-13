import logging

from koala.config.collections import SOCIAL_GROUPS
from koala.crud.jobs_crud.mongo_base import MongoBase


class SocialGroupsCollection:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(SOCIAL_GROUPS)

    async def create_group(self, group_details: dict) -> any:
        try:
            logging.info(group_details)
        except Exception as e:
            logging.error(f"Error: Create group error {e}")

    async def get_all_groups(self, group_id: str) -> any:
        try:
            pass
        except Exception as e:
            logging.error(f"Error: Create group error {e}")

    async def get_group_by_id(self, group_id: str) -> any:
        try:
            logging.info(group_id)
        except Exception as e:
            logging.error(f"Error: Create group error {e}")

    async def get_group_users(self, group_id: str) -> any:
        try:
            pass
        except Exception as e:
            logging.error(f"Error: Create group error {e}")

    async def get_group_user_by_id(self, user_id: str) -> any:
        try:
            logging.info(user_id)
        except Exception as e:
            logging.error(f"Error: Create group error {e}")
