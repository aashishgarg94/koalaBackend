from fastapi import FastAPI, Depends
from koala.authentication import routes
from koala.authentication.authentication import get_current_active_user
from koala.db.mongo_adaptor import close_mongo_connection, connect_to_mongo
from koala.routers import register

app = FastAPI()

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(routes.router, tags=['auth'])
app.include_router(register.router, tags=['register'])
