from fastapi import FastAPI
from koala.authentication import routes

app = FastAPI()

app.include_router(routes.router)
