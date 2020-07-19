from koala.config.collections import DB_NAME
from motor.motor_asyncio import AsyncIOMotorClient


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


# Need to work on it
def create_collection_connection(collection_name: str):
    return db.client[DB_NAME][collection_name]
