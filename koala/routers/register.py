from fastapi import APIRouter, HTTPException, status

from ..authentication.jwt_handler import get_password_hash
from ..crud.company import CompanyCollection
from ..crud.user import MongoDBUserDatabase
from ..models.jobs import CompanyInPasswordModel, CompanyModelPassword
from ..models.master import BaseIsCreated
from ..models.user import UserInModel, UserRegisterModel

router = APIRouter()


@router.post(
    "/register/applicant",
    response_model=BaseIsCreated,
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserRegisterModel):
    user_db = MongoDBUserDatabase(UserInModel)
    # Check if user already exists
    existing_user = await user_db.find_by_email(user.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="REGISTER_USER_ALREADY_EXISTS",
        )

    hashed_password = get_password_hash(user.password.get_secret_value())
    db_user = UserInModel(**user.dict(), hashed_password=hashed_password)
    result = await user_db.create_user(db_user)
    if result is False:
        raise HTTPException(status_code=400, detail="Not able to process")
    return result


@router.post(
    "/register/company",
    response_model=BaseIsCreated,
    status_code=status.HTTP_201_CREATED,
)
async def register(user: CompanyModelPassword):
    company_collection = CompanyCollection()
    # Check if user already exists
    existing_user = await company_collection.find_by_email(user.contact_email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="REGISTER_USER_ALREADY_EXISTS",
        )

    hashed_password = get_password_hash(user.password.get_secret_value())
    db_user = CompanyInPasswordModel(**user.dict(), hashed_password=hashed_password)
    result = await company_collection.create_user(db_user)
    if result is False:
        raise HTTPException(status_code=400, detail="Not able to process")
    return result
