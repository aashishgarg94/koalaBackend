import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security
from koala.authentication.authentication_user import get_current_active_user
from koala.crud.social.users import SocialPostsCollection
from koala.models.jobs_models.user import UserModel

router = APIRouter()


@router.post(
    "/followed_groups",
    response_model=GroupsFollowed,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_followed_groups(user_id: str):
    try:
        social_posts_collection = SocialPostsCollection()
        return await social_posts_collection.get_user_followed_groups(user_id=user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/follow_user",
    response_model=BaseIsFollowed,
    dependencies=[Security(get_current_active_user, scopes=["social:write"])],
)
async def make_user_follow_group(
    user_id: str,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_map = get_user_model(current_user, "follower")

        social_posts_collection = SocialPostsCollection()
        data = await social_posts_collection.make_user_follow_user(
            user_id=user_id, user_map=user_map
        )
        return data
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/user_followed",
    response_model=UsersFollowed,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_followed(
    page_no: Optional[int] = 1,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_id = get_user_model(current_user, "id")
        user_db = MongoDBUserDatabase(UserInModel)
        user_count = await user_db.get_follower_count(user_id)

        if user_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT

            social_posts_collection = SocialPostsCollection()
            return await social_posts_collection.get_user_followed(
                user_id=user_id, skip=skip, limit=REQUEST_LIMIT
            )
        else:
            return UsersFollowed(post_list=[])
    except Exception as e:
        logging.info(e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/same_company_users",
    response_model=BasePostMemberCountListModel,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_user_following(
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        social_posts_collection = SocialPostsCollection()
        return await social_posts_collection.get_users_in_same_company(
            current_company=current_user.bio.current_company, user_id=current_user.id
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/users_to_follow",
    response_model=BasePostMemberCountListModel,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def get_users_to_follow(
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        user_db = MongoDBUserDatabase(UserInModel)
        current_user_followed_list = await user_db.find_user_followed_by_username(
            current_user.username
        )
        current_followed_users = current_user_followed_list[0]["users_followed"]
        current_followed_users.append(current_user.id)

        social_posts_collection = SocialPostsCollection()
        data = await social_posts_collection.get_users_to_follow(
            current_followed_users=current_user_followed_list[0]["users_followed"]
        )
        return data
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
