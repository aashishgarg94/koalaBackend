import logging
import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Security
from koala.authentication.authentication_user import get_current_active_user
from koala.constants import REQUEST_LIMIT
from koala.crud.social.users import SocialPostsCollection
from koala.models.jobs_models.user import UserModel
from koala.models.social.users import CreatePostModelOutList

router = APIRouter()


@router.post(
    "/feed",
    response_model=CreatePostModelOutList,
    dependencies=[Security(get_current_active_user, scopes=["social:read"])],
)
async def user_feed_by_groups_and_users_following(
    page_no: Optional[int] = 1,
    current_user: UserModel = Depends(get_current_active_user),
):
    try:
        social_posts_collection = SocialPostsCollection()
        post_count = await social_posts_collection.get_feed_count()

        groups_followed_list = current_user.groups_followed

        user_followed_list = []
        for user_dict in current_user.users_following.followers_list:
            user_followed_list.append(user_dict.user_id)

        more_pages = True
        post_list = []
        if post_count > 0:
            adjusted_page_number = page_no - 1
            skip = adjusted_page_number * REQUEST_LIMIT
            post_list = await social_posts_collection.get_user_feed_by_groups_and_users_following(
                skip=skip,
                limit=REQUEST_LIMIT,
                groups_followed_list=groups_followed_list,
                user_followed_list=user_followed_list,
            )

            if page_no == math.ceil(post_count / REQUEST_LIMIT):
                more_pages = False

        return CreatePostModelOutList(more_pages=more_pages, post_list=post_list)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Something went wrong")
