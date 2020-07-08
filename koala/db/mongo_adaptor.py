import logging
import pprint

from motor.motor_asyncio import AsyncIOMotorClient

from .mongodb import db


async def connect_to_mongo():
    logging.info("Connecting to mongo...")
    db.client = AsyncIOMotorClient(
        str("mongodb+srv://uday:koala1mongo@cluster0.tbo7y.mongodb.net"),
        maxPoolSize=10,
        minPoolSize=10,
    )
    pprint.pprint(db.client.test)
    logging.info("Successfully connected to db")


async def close_mongo_connection():
    logging.info("closing db connection")
    db.client.close()
    logging.info("Database connection closed")
