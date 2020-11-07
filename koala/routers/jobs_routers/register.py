from fastapi import APIRouter, HTTPException, status
from koala.authentication.jwt_handler import get_password_hash
from koala.crud.jobs_crud.company import CompanyCollection
from koala.crud.jobs_crud.user import MongoDBUserDatabase
from koala.models.jobs_models.jobs import CompanyInPasswordModel, CompanyModelPassword
from koala.models.jobs_models.master import BaseIsCreated
from koala.models.jobs_models.user import UserBioModel, UserInModel, UserModel
from koala.models.social.users import FollowerModel

router = APIRouter()


@router.post(
    "/register/applicant",
    response_model=BaseIsCreated,
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserModel):
    user_db = MongoDBUserDatabase(UserInModel)
    user_db.username = user.mobile_number
    user_db.password = "Pragaty@123"
    # Check if user already exists
    existing_user = await user_db.find_by_mobile_number(user.mobile_number)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="REGISTER_USER_ALREADY_EXISTS",
        )

    # hashed_password = get_password_hash(user.password.get_secret_value())
    hashed_password = get_password_hash(user_db.password)
    users_following = FollowerModel()
    user_bio = UserBioModel()
    db_user = UserInModel(
        **user.dict(),
        hashed_password=hashed_password,
        users_following=users_following,
        bio=user_bio
    )
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
    try:
        company_collection = CompanyCollection()
        # Check if user already exists
        existing_user = await company_collection.find_by_email(user.contact_email)  # ok

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
    except Exception as e:
        raise e
