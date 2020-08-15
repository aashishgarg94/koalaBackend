import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware
from koala.authentication.authentication import get_current_active_user
from koala.db.mongo_adaptor import close_mongo_connection, connect_to_mongo
from koala.routers import auth, job_user, jobs, master, register, user, website, company

app = FastAPI()

origins = [
    "https://koala.bharatworks.co",
    "https://site.bharatworks.co",
    "https://www.pragaty.in",
    "http://localhost:*",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS", "DELETE", "PUT"],
    allow_headers=[
        "x-requested-with",
        "Content-Type",
        "origin",
        "authorization",
        "accept",
        "client-security-token",
    ],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(register.router, tags=["Register"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(user.router, tags=["User"])
app.include_router(
    master.router, tags=["Master"], dependencies=[Depends(get_current_active_user)]
)
app.include_router(company.router, tags=["Company"])
app.include_router(
    jobs.router, tags=["Jobs"], dependencies=[Depends(get_current_active_user)]
)
app.include_router(
    job_user.router,
    tags=["Users & Jobs"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    website.router, tags=["Website APIs"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
