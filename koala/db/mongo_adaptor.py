import logging

from motor.motor_asyncio import AsyncIOMotorClient
from .mongodb import db
import pprint


async def connect_to_mongo():
    logging.info("Connecting to mongo...")
    # db.client = AsyncIOMotorClient(str('mongodb://localhost:27017'),

    # client = pymongo.MongoClient(
    #     "mongodb+srv://uday:<password>@cluster0.tbo7y.mongodb.net/<dbname>?retryWrites=true&w=majority")
    # db = client.test

    db.client = AsyncIOMotorClient(str("mongodb+srv://uday:koala1mongo@cluster0.tbo7y.mongodb.net"),
                                   maxPoolSize=10,
                                   minPoolSize=10)
    pprint.pprint(db.client.test)
    logging.info("Successfully connected to db")


async def close_mongo_connection():
    logging.info("closing db connection")
    db.client.close()
    logging.info("Database connection closed")
