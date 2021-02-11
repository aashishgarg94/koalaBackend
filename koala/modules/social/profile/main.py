import logging

from fastapi import APIRouter, Security
from koala.authentication.authentication_user import get_current_active_user
from koala.crud.jobs_crud.user import MongoDBUserDatabase
from koala.models.jobs_models.user import UserInModel

router = APIRouter()


@router.get(
    "/social/bio",
    dependencies=[Security(get_current_active_user, scopes=["applicant:read"])],
)
async def user_social_bio_fetch(user_id: str = None):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        return await user_db.user_social_bio_fetch(user_id=user_id)
    except Exception as e:
        logging.error(f"Error while processing this request {e}")
        raise e
