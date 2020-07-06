from motor.motor_asyncio import AsyncIOMotorClient
import pprint
import asyncio
# import nest_asyncio
# nest_asyncio.apply()

# Creating Client
uri = "mongodb://localhost:27017"
client = AsyncIOMotorClient(uri)

# Getting a Database
db = client['koala-backend']

# Getting a Collection
# collection = db['users']


async def find_cursor_to_list():
    """
    This method finds items from MongoDB collection and
    asynchronously converts cursor to a list with items
    :return:
    """
    collection = db['users']

    filter_ = {
        "someField": "someValue"
    }
    projection_ = {
        "_id": False  # don't return the _id
    }
    cursor = collection.find()
    # Convert the cursor to a list of items right away.
    # NB! Dangerous with large result sets
    items = cursor.to_list(length=400)
    return items
