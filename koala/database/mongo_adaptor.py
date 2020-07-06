import logging

from motor.motor_asyncio import AsyncIOMotorClient
from .mongodb import db


async def connect_to_mongo():
    logging.info("Connecting to mongo...")
    db.client = AsyncIOMotorClient(str('mongodb://localhost:27017'),
                                   maxPoolSize=10,
                                   minPoolSize=10)
    logging.info("Successfully connected to database")


async def close_mongo_connection():
    logging.info("closing database connection")
    db.client.close()
    logging.info("Database connection closed")
