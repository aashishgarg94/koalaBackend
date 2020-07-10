import pprint

from fastapi import APIRouter, HTTPException, status

from ..authentication.jwt_handler import get_password_hash
from ..crud.user import MongoDBUserDatabase
from ..models.user import UserCreateModal, UserDB, UserModal

router = APIRouter()


@router.post(
    "/register", response_model=UserModal, status_code=status.HTTP_201_CREATED,
)
async def register(user: UserCreateModal):
    user_db = MongoDBUserDatabase(UserDB)
    existing_user = await user_db.get_by_email(user.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="REGISTER_USER_ALREADY_EXISTS",
        )

    hashed_password = get_password_hash(user.password.get_secret_value())
    db_user = UserDB(**user.dict(), hashed_password=hashed_password)
    pprint.pprint(db_user.dict())
    created_user = await user_db.create(db_user)

    return created_user
