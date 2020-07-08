from motor.motor_asyncio import AsyncIOMotorClient

# import nest_asyncio
# nest_asyncio.apply()

# Creating Client
uri = "mongodb+srv://uday:koala1mongo@cluster0.tbo7y.mongodb.net/koala-backend?retryWrites=true&w=majority"
client = AsyncIOMotorClient(uri)

# Getting a Database
db = client["koala-backend"]

# Getting a Collection
# collection = db['users']


async def find_cursor_to_list():
    """
    This method finds items from MongoDB collection and
    asynchronously converts cursor to a list with items
    :return:
    """
    collection = db["test-users"]

    filter_ = {"someField": "someValue"}
    projection_ = {"_id": False}  # don't return the _id
    cursor = collection.find()
    # Convert the cursor to a list of items right away.
    # NB! Dangerous with large result sets
    items = cursor.to_list(length=400)
    return items
