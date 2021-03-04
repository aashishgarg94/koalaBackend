from koala.config.collections import USERS
from koala.dao.mongo_base import MongoBase


class Common:
    def __init__(self):
        self.collection = MongoBase()
        self.collection(USERS)

    async def find_by_username(self, username: str) -> any:
        try:
            return await self.collection.find_one(
                finder={"username": username}, projection={"_id": 1}
            )
        except Exception as e:
            raise e
