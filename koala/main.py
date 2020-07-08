from fastapi import FastAPI
from koala.authentication import routes
from koala.db.mongo_adaptor import close_mongo_connection, connect_to_mongo

app = FastAPI()

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(routes.router)
