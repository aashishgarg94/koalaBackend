import logging

from fastapi import APIRouter, Security
from koala.authentication.authentication_user import get_current_active_user
from koala.crud.jobs_crud.user import MongoDBUserDatabase
from koala.models.jobs_models.master import BaseIsDisabled, BaseIsUpdated
from koala.models.jobs_models.user import (
    BioUpdateInModel,
    BioUpdateOutModel,
    BioUpdateWithUserDetailOutModel,
    UserBioModel,
    UserCreateBioModel,
    UserInModel,
    UserModel,
    UserUpdateCls,
    UserUpdateModel,
    UserUpdateOutModel,
)

router = APIRouter()


"""NOTE:
Create User will be done from registration
"""


# API -  Get Current User
@router.get(
    "/user/me",
    response_model=UserModel,
    dependencies=[Security(get_current_active_user, scopes=["applicant:read"])],
)
async def read_user_me(
    current_user: UserModel = Security(
        get_current_active_user,
        scopes=["applicant:read"],
    )
):
    try:
        return current_user
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e


# API - Update User
@router.post(
    "/user/update/me",
    response_model=UserUpdateOutModel,
    dependencies=[Security(get_current_active_user, scopes=["applicant:write"])],
)
async def update_user_me(
    update_user: UserUpdateModel,
    current_user: UserModel = Security(
        get_current_active_user,
        scopes=["applicant:write"],
    ),
):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        user_updates = UserUpdateCls(**update_user.dict(exclude_unset=True))
        return await user_db.find_and_modify(user_updates, current_user)
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e


# API - Delete User
@router.get(
    "/user/disable/me",
    response_model=BaseIsDisabled,
    dependencies=[Security(get_current_active_user, scopes=["applicant:write"])],
)
async def disable_user_me(
    current_user: UserModel = Security(
        get_current_active_user,
        scopes=["applicant:write"],
    )
):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        # user = UserUpdateCls(**current_user.dict(exclude_unset=True))
        response = await user_db.disable_one(current_user.username)
        return response
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e


@router.get(
    "/user/disable_by_id",
    response_model=BaseIsDisabled,
    dependencies=[Security(get_current_active_user, scopes=["applicant:write"])],
)
async def user_disable_by_id(
        user_id: str,
        current_user: UserModel = Security(
            get_current_active_user,
            scopes=["applicant:write"],
            )
):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        response = await user_db.disable_user_by_id(user_id)
        return response
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e


# Get user bio
@router.get(
    "/user/bio",
    response_model=BioUpdateWithUserDetailOutModel,
    dependencies=[Security(get_current_active_user, scopes=["applicant:read"])],
)
async def user_bio_fetch(
    current_user: UserModel = Security(
        get_current_active_user,
        scopes=["applicant:read"],
    )
):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        return await user_db.user_bio_fetch(current_user.username)
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e


# Update user bio for creating it's profile
@router.post(
    "/user/bio/update",
    response_model=BioUpdateOutModel,
    dependencies=[Security(get_current_active_user, scopes=["applicant:write"])],
)
async def user_bio_update(
    user_bio_updates: UserBioModel,
    current_user: UserModel = Security(
        get_current_active_user,
        scopes=["applicant:write"],
    ),
):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        bio_updates = BioUpdateInModel(**user_bio_updates.dict(exclude_unset=True))
        return await user_db.user_bio_update(bio_updates, current_user)
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e


# Update user bio for creating it's profile
@router.post(
    "/user/create_profile",
    response_model=BaseIsUpdated,
)
async def create_profile(user_profile_details: UserCreateBioModel):
    try:

        user_db = MongoDBUserDatabase(UserInModel)
        # bio_updates = BioUpdateInModel(**user_bio_updates.dict(exclude_unset=True))
        data = await user_db.update_create_user_profile_details(
            profile_details=user_profile_details
        )
        return data
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e
