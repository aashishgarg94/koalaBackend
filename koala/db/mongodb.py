from koala.config.collections import DB_NAME
from motor.motor_asyncio import AsyncIOMotorClient


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()

# Trying out if we can ingest this in class based on crud operation. In progress...
# async def get_database() -> AsyncIOMotorDatabase:
#     return db.client.koala_backend
#
#
# async def get_collection(db_collection: str):
#     koala_db = await get_database()
#     return koala_db[db_collection]


def get_collection(collection_name: str):
    return db.client[DB_NAME][collection_name]
