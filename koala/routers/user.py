from fastapi import APIRouter, Depends
from koala.authentication.authentication import get_current_active_user
from koala.crud.user import MongoDBUserDatabase

from ..models.user import (
    UserBioModel,
    UserDB,
    UserModel,
    UserUpdateCls,
    UserUpdateModel,
)

router = APIRouter()


"""NOTE:
Create User will be done from registration
"""


# API -  Get Current User
@router.get("/user/me/", response_model=UserModel)
async def read_user_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user


# API - Update User
@router.post("/user/update/me/", response_model=UserModel)
async def update_user_me(
    update_user: UserUpdateModel,
    current_user: UserModel = Depends(get_current_active_user),
):
    user_db = MongoDBUserDatabase(UserDB)
    user = UserUpdateCls(
        **update_user.dict(exclude_unset=True), username=current_user.username
    )
    response = await user_db.find_and_modify(user)
    return response


# API - Delete User
@router.get("/user/delete/me/", response_model=UserModel)
async def delete_user_me(current_user: UserModel = Depends(get_current_active_user)):
    user_db = MongoDBUserDatabase(UserDB)
    response = await user_db.delete(current_user.email)
    return response


# Update user bio for creating it's profile
@router.post("/user/bio/update/", response_model=UserBioModel)
async def user_bio_update(
    user_bio: UserBioModel, current_user: UserModel = Depends(get_current_active_user)
):
    user_db = MongoDBUserDatabase(UserDB)
    response = await user_db.user_bio_update(current_user.email, user_bio)
    return response


# Get user bio
@router.get("/user/bio/", response_model=UserBioModel)
async def user_bio_fetch(current_user: UserModel = Depends(get_current_active_user)):
    user_db = MongoDBUserDatabase(UserDB)
    response = await user_db.user_bio_fetch(current_user.email)
    return response
