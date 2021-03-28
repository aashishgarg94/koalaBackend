from fastapi import APIRouter, Depends, HTTPException, Security
from koala.authentication.authentication_user import get_current_active_user
from koala.crud.social.users import SocialPostsCollection
from koala.models.jobs_models.user import UserModel
from koala.models.social.users import FollowerModel
from koala.routers.social.users import get_user_model

router = APIRouter()


@router.get(
    "/user_following",
    response_model=FollowerModel,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_following(
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_id = get_user_model(current_user, "id")
        social_posts_collection = SocialPostsCollection()
        return await social_posts_collection.get_user_following(user_id=user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
