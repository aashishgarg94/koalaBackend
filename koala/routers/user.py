import logging

from fastapi import APIRouter, Depends
from koala.authentication.authentication import get_current_active_user
from koala.crud.user import MongoDBUserDatabase

from ..models.master import BaseIsDisabled
from ..models.user import (
    BioUpdateInModel,
    BioUpdateOutModel,
    UserBioModel,
    UserInModel,
    UserModel,
    UserOutModel,
    UserUpdateCls,
    UserUpdateModel,
    UserUpdateOutModel,
)

router = APIRouter()


"""NOTE:
Create User will be done from registration
"""


# API -  Get Current User
@router.get("/user/me", response_model=UserModel)
async def read_user_me(current_user: UserModel = Depends(get_current_active_user)):
    try:
        return current_user
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e


# API - Update User
@router.post("/user/update/me", response_model=UserUpdateOutModel)
async def update_user_me(
    update_user: UserUpdateModel,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        user_updates = UserUpdateCls(**update_user.dict(exclude_unset=True))
        return await user_db.find_and_modify(user_updates, current_user)
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e


# API - Delete User
@router.get("/user/disable/me", response_model=BaseIsDisabled)
async def disable_user_me(current_user: UserModel = Depends(get_current_active_user)):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        user = UserUpdateCls(**current_user.dict(exclude_unset=True))
        response = await user_db.disable_one(user)
        return response
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e


# Get user bio
@router.get("/user/bio", response_model=BioUpdateOutModel)
async def user_bio_fetch(current_user: UserModel = Depends(get_current_active_user)):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        return await user_db.user_bio_fetch(current_user.email)
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e


# Update user bio for creating it's profile
@router.post("/user/bio/update", response_model=BioUpdateOutModel)
async def user_bio_update(
    user_bio_updates: UserBioModel,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        bio_updates = BioUpdateInModel(**user_bio_updates.dict(exclude_unset=True))
        return await user_db.user_bio_update(bio_updates, current_user)
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e
