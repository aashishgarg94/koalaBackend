from fastapi import APIRouter, Depends
from koala.authentication.authentication import get_current_active_user
from koala.models.user import UserModel

router = APIRouter()


@router.get("/users/me/", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user
