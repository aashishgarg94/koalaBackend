from fastapi import APIRouter, Depends
from koala.authentication.authentication import get_current_active_user
from koala.crud.user import MongoDBUserDatabase
from koala.models.user import UserDB, UserModal

router = APIRouter()


"""NOTE:
Create User will be done from registration
"""


# API -  Get Current User
@router.get("/user/me/", response_model=UserModal)
async def read_user_me(current_user: UserModal = Depends(get_current_active_user)):
    return current_user


# API - Update User
@router.post(
    "/user/update/me/", response_model=UserModal, dependencies=[Depends(get_current_active_user)]
)
async def update_user_me(update_user: UserModal):
    user_db = MongoDBUserDatabase(UserDB)
    response = await user_db.find_and_modify(update_user)
    return response


# # API - Delete User
# @router.post(
#     "/user/delete/me/", response_model=UserModal, dependencies=get_current_active_user
# )
# async def delete_user_me(user: UserDB):
#     user_db = MongoDBUserDatabase(UserDB)
#     response = await user_db.find_and_modify(user)
#     return response
