import logging

from motor.motor_asyncio import AsyncIOMotorClient

from .mongodb import db

# mongodb+srv://uday:koala1mongo@cluster0.ca4yg.mongodb.net/production?retryWrites=true&w=majority
async def connect_to_mongo():
    logging.info("Connecting to mongo...")
    db.client = AsyncIOMotorClient(
        str(
            "mongodb+srv://uday:koala1mongo@cluster0.tbo7y.mongodb.net/koala-backend?retryWrites=true&w=majority"
        ),
        maxPoolSize=10,
        minPoolSize=10,
    )
    logging.info("KOALA shouts: Successfully connected :)")


async def close_mongo_connection():
    logging.info("closing db connection")
    db.client.close()
    logging.info("KOALA says: Database connection closed gracefully")
