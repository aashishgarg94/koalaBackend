import uvicorn
from fastapi import FastAPI
from koala.db.mongo_adaptor import close_mongo_connection, connect_to_mongo
from koala.routers import auth, master, register, user

app = FastAPI()

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(register.router, tags=["register"])
app.include_router(auth.router, tags=["auth"])
app.include_router(user.router, tags=["user"])
app.include_router(master.router, tags=["master"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
