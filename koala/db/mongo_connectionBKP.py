from motor.motor_asyncio import AsyncIOMotorClient

# Creating Client
uri = "mongodb+srv://uday:koala1mongo@cluster0.tbo7y.mongodb.net/koala-backend?retryWrites=true&w=majority"
client = AsyncIOMotorClient(uri)

# Getting a Database
db = client["koala-backend"]

user_collection = db['test-users']
