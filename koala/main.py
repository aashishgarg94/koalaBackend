import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from koala.cache.feed import feed
from koala.modules.otp import otp
from koala.db.mongo_adaptor import close_mongo_connection, connect_to_mongo
from koala.modules.devices import main
from koala.modules.social.posts import posts, likes, comments

from koala.website import website
from koala import healthcheck, supported_version

# from koala.routers.jobs_routers import (
#     auth,
#     company,
#     image_uploads,
#     job_user,
#     jobs,
#     master,
#     register,
#     user,
# )
# from koala.routers.learning import learning
# from koala.routers.social import users

app = FastAPI()


def config_logging(level=logging.INFO):
    # When run by 'uvicorn ...', a root handler is already
    # configured and the basicConfig below does nothing.
    # To get the desired formatting:
    logging.getLogger().handlers.clear()

    # 'uvicorn --log-config' is broken so we configure in the app.
    #   https://github.com/encode/uvicorn/issues/511
    logging.basicConfig(
        # match gunicorn format
        format="%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S %z]",
        level=level,
    )

    # When run by 'gunicorn -k uvicorn.workers.UvicornWorker ...',
    # These loggers are already configured and propogating.
    # So we have double logging with a root logger.
    # (And setting propagate = False hurts the other usage.)
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.error").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = True
    logging.getLogger("uvicorn.error").propagate = True


config_logging()

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

# HEALTH CHECK
app.include_router(healthcheck.router, tags=["HealthCheck"])

# ROUTER - DEPRECATED
# app.include_router(register.router, tags=["Register"])
# app.include_router(auth.router, tags=["Auth"])
# app.include_router(user.router, tags=["User"])
# app.include_router(
#     master.router, tags=["Master"], dependencies=[Depends(get_current_active_user)]
# )
# app.include_router(company.router, tags=["Company"])
# app.include_router(jobs.router, tags=["Jobs"])
# app.include_router(job_user.router, tags=["Users & Jobs"])
# app.include_router(users.router, prefix="/user", tags=["Social Users"])
# app.include_router(image_uploads.router, prefix="/upload", tags=["Image Upload"])

# LEARNING ROUTERS
# app.include_router(learning.router, prefix="/learning", tags=["Learning"])

app.include_router(posts.router, prefix="/group", tags=["Social Groups"])

app.include_router(supported_version.router, tags=["App Version Check"])


# otp
app.include_router(
    otp.router,
    tags=["OTP APIs"],
)

# Notifications
app.include_router(
    main.router,
    prefix="/notification",
    tags=["Notifications APIs"],
)

# Like
app.include_router(
    likes.router,
    prefix="/post",
    tags=["Cache APIs"],
)

# Comment
app.include_router(
    comments.router,
    prefix="/post",
    tags=["Cache APIs"],
)

app.include_router(
    feed.router,
    prefix="/cache",
    tags=["Cache APIs"],
)

# ================ Website API's ================
app.include_router(
    website.router,
    tags=["Website APIs"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
